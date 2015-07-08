
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
from .OBDResponse import OBDResponse
from .utils import scanSerial, SerialStatus
from .debug import debug



class OBD(object):
    """
        Class representing an OBD-II connection
        with it's assorted commands/sensors.
    """

    def __init__(self, portstr=None, baudrate=38400):
        self.port = None
        self.supported_commands = []

        debug("========================== python-OBD (v%s) ==========================" % __version__)
        self.__connect(portstr, baudrate) # initialize by connecting and loading sensors
        self.__load_commands()            # try to load the car's supported commands
        debug("=========================================================================")


    def __connect(self, portstr, baudrate):
        """
            Attempts to instantiate an ELM327 connection object.
        """

        if portstr is None:
            debug("Using scanSerial to select port")
            portnames = scanSerial()
            debug("Available ports: " + str(portnames))

            for port in portnames:
                debug("Attempting to use port: " + str(port))
                self.port = ELM327(port, baudrate)

                if self.port.status >= SerialStatus.ELM_CONNECTED:
                    break # success! stop searching for serial
        else:
            debug("Explicit port defined")
            self.port = ELM327(portstr, baudrate)

        # if the connection failed, close it
        if self.port.status == SerialStatus.NOT_CONNECTED:
            debug("Failed to connect")
            self.close()


    def __load_commands(self):
        """
            Queries for available PIDs, sets their support status,
            and compiles a list of command objects.
        """

        if self.status != SerialStatus.CAR_CONNECTED:
            debug("Cannot load commands: No connection to car", True)
            return

        debug("querying for supported PIDs (commands)...")
        pid_getters = commands.pid_getters()
        for get in pid_getters:
            # PID listing commands should sequentialy become supported
            # Mode 1 PID 0 is assumed to always be supported
            if not self.supports(get):
                continue

            # when querying, only use the blocking OBD.query()
            # prevents problems when query is redefined in a subclass
            response = OBD.query(self, get, force=True) # ask nicely

            if response.is_null():
                continue
            
            supported = response.value # string of binary 01010101010101

            # loop through PIDs binary
            for i in range(len(supported)):
                if supported[i] == "1":

                    mode = get.mode_int
                    pid  = get.pid_int + i + 1

                    if commands.has_pid(mode, pid):
                        c = commands[mode][pid]
                        c.supported = True

                        # don't add PID getters to the command list
                        if c not in pid_getters:
                            self.supported_commands.append(c)

        debug("finished querying with %d commands supported" % len(self.supported_commands))


    def close(self):
        """
            Closes the connection, and clear supported_commands
        """

        self.supported_commands = []

        if self.port is not None:
            debug("Closing connection")
            self.port.close()
            self.port = None


    @property
    def status(self):
        if self.port is None:
            return SerialStatus.NOT_CONNECTED
        else:
            return self.port.status


    def is_connected(self):
        """
            Returns a boolean for whether a connection with the car was made.

            Note: this function returns False when:
            obd.status = SerialStatus.ELM_CONNECTED
        """
        return self.status == SerialStatus.CAR_CONNECTED


    def get_port_name(self):
        """ Returns the name of the currently connected port """
        if self.port is not None:
            return self.port.port_name
        else:
            return "Not connected to any port"


    def print_commands(self):
        """
            Utility function meant for working in interactive mode.
            Prints all commands supported by the car.
        """
        for c in self.supported_commands:
            print(str(c))


    def supports(self, cmd):
        """
            Returns a boolean for whether the given command
            is supported by the car AND this library
        """
        return commands.has_command(cmd) and cmd.supported


    def query(self, cmd, force=False):
        """
            primary API function. Sends commands to the car, and
            protects against sending unsupported commands.
        """

        if self.status == SerialStatus.NOT_CONNECTED:
            debug("Query failed, no connection available", True)
            return OBDResponse()

        if not self.supports(cmd) and not force:
            debug("'%s' is not supported" % str(cmd), True)
            return OBDResponse()

        # send command and retrieve message
        debug("Sending command: %s" % str(cmd))
        messages = self.port.send_and_parse(cmd.command)

        if not messages:
            debug("No valid OBD Messages returned", True)
            return OBDResponse()

        return cmd(messages) # compute a response object
