
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2015 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# obd.py                                                               #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

import time

from .__version__ import __version__
from .elm327 import ELM327
from .commands import commands
from .utils import scanSerial, Response
from .debug import debug



class OBD(object):
    """
        Class representing an OBD-II connection with it's assorted commands/sensors
    """

    def __init__(self, portstr=None, baudrate=38400):
        self.port = None
        self.supported_commands = []

        debug("========================== python-OBD (v%s) ==========================" % __version__)
        self.__connect(portstr, baudrate) # initialize by connecting and loading sensors
        debug("=========================================================================")


    def __connect(self, portstr=None, baudrate=38400):
        """
            Attempts to instantiate an ELM327 connection object.
            Upon success, __load_commands() is called
        """

        if portstr is None:
            debug("Using scanSerial to select port")
            portnames = scanSerial()
            debug("Available ports: " + str(portnames))

            for port in portnames:
                debug("Attempting to use port: " + str(port))
                self.port = ELM327(port, baudrate=baudrate)

                if self.port.is_connected():
                    # success! stop searching for serial
                    break
        else:
            debug("Explicit port defined")
            self.port = ELM327(portstr, baudrate=baudrate)

        # if a connection was made, query for commands
        if self.is_connected():
            self.__load_commands()
        else:
            debug("Failed to connect")


    def close(self):
        """ Closes the connection """
        if self.is_connected():
            debug("Closing connection")
            self.port.close()
            self.port = None
            self.supported_commands = []


    def is_connected(self):
        """ Returns a boolean for whether a successful serial connection was made """
        return (self.port is not None) and self.port.is_connected()


    def get_port_name(self):
        """ Returns the name of the currently connected port """
        if self.is_connected():
            return self.port.get_port_name()
        else:
            return "Not connected to any port"


    def __load_commands(self):
        """
            Queries for available PIDs, sets their support status,
            and compiles a list of command objects.
        """

        debug("querying for supported PIDs (commands)...")

        self.supported_commands = []

        pid_getters = commands.pid_getters()

        for get in pid_getters:
            # PID listing commands should sequentialy become supported
            # Mode 1 PID 0 is assumed to always be supported
            if not self.supports(get):
                continue

            response = self.__send(get) # ask nicely

            if response.is_null():
                continue
            
            supported = response.value # string of binary 01010101010101

            # loop through PIDs binary
            for i in range(len(supported)):
                if supported[i] == "1":

                    mode = get.get_mode_int()
                    pid  = get.get_pid_int() + i + 1

                    if commands.has_pid(mode, pid):
                        c = commands[mode][pid]
                        c.supported = True

                        # don't add PID getters to the command list
                        if c not in pid_getters:
                            self.supported_commands.append(c)

        debug("finished querying with %d commands supported" % len(self.supported_commands))


    def print_commands(self):
        """
            Utility function meant for working in interactive mode.
            Prints all commands supported by the car.
        """
        for c in self.supported_commands:
            print(str(c))


    def supports(self, c):
        """ Returns a boolean for whether the car supports the given command """
        return commands.has_command(c) and c.supported


    def __send(self, c):
        """
            Back-end implementation of query()
            sends the given command, retrieves and parses the response
        """

        if not self.is_connected():
            debug("Query failed, no connection available", True)
            return Response() # return empty response

        debug("Sending command: %s" % str(c))

        # send command and retrieve message
        m = self.port.send_and_parse(c.get_command())

        if m is None:
            return Response() # return empty response
        else:
            return c(m) # compute a response object


    def query(self, c, force=False):
        """
            primary API function. Sends commands to the car, and
            protects against sending unsupported commands.
        """

        # check that the command is supported
        if self.supports(c) or force:
            return self.__send(c)
        else:
            debug("'%s' is not supported" % str(c), True)
            return Response() # return empty response
