
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
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


from .__version__ import __version__
from .elm327 import ELM327
from .commands import commands
from .OBDResponse import OBDResponse
from .utils import scan_serial, OBDStatus
from .debug import debug



class OBD(object):
    """
        Class representing an OBD-II connection
        with it's assorted commands/sensors.
    """

    def __init__(self, portstr=None, baudrate=38400, protocol=None, fast=True):
        self.port = None
        self.supported_commands = set(commands.base_commands())
        self.fast = fast
        self.__last_command = "" # used for running the previous command with a CR

        debug("========================== python-OBD (v%s) ==========================" % __version__)
        self.__connect(portstr, baudrate, protocol) # initialize by connecting and loading sensors
        self.__load_commands()            # try to load the car's supported commands
        debug("=========================================================================")


    def __connect(self, portstr, baudrate, protocol):
        """
            Attempts to instantiate an ELM327 connection object.
        """

        if portstr is None:
            debug("Using scan_serial to select port")
            portnames = scan_serial()
            debug("Available ports: " + str(portnames))

            if not portnames:
                debug("No OBD-II adapters found", True)
                return

            for port in portnames:
                debug("Attempting to use port: " + str(port))
                self.port = ELM327(port, baudrate, protocol)

                if self.port.status() >= OBDStatus.ELM_CONNECTED:
                    break # success! stop searching for serial
        else:
            debug("Explicit port defined")
            self.port = ELM327(portstr, baudrate, protocol)

        # if the connection failed, close it
        if self.port.status == OBDStatus.NOT_CONNECTED:
            # the ELM327 class will report its own errors
            self.close()


    def __load_commands(self):
        """
            Queries for available PIDs, sets their support status,
            and compiles a list of command objects.
        """

        if self.status() != OBDStatus.CAR_CONNECTED:
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
            # prevents problems when query is redefined in a subclass (like Async)
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
                        self.supported_commands.add(commands[mode][pid])

                    # set support for mode 2 commands
                    if mode == 1 and commands.has_pid(2, pid):
                        self.supported_commands.add(commands[2][pid])

        debug("finished querying with %d commands supported" % len(self.supported_commands))


    def close(self):
        """
            Closes the connection, and clears supported_commands
        """

        self.supported_commands = []

        if self.port is not None:
            debug("Closing connection")
            self.port.close()
            self.port = None


    def status(self):
        """ returns the OBD connection status """
        if self.port is None:
            return OBDStatus.NOT_CONNECTED
        else:
            return self.port.status()


    # not sure how useful this would be

    # def ecus(self):
    #     """ returns a list of ECUs in the vehicle """
    #     if self.port is None:
    #         return []
    #     else:
    #         return self.port.ecus()


    def protocol_name(self):
        """ returns the name of the protocol being used by the ELM327 """
        if self.port is None:
            return ""
        else:
            return self.port.protocol_name()


    def protocol_id(self):
        """ returns the ID of the protocol being used by the ELM327 """
        if self.port is None:
            return ""
        else:
            return self.port.protocol_id()


    def get_port_name(self):
        # TODO: deprecated, remove later
        print("OBD.get_port_name() is deprecated, use OBD.port_name() instead")
        return self.port_name()


    def port_name(self):
        """ Returns the name of the currently connected port """
        if self.port is not None:
            return self.port.port_name()
        else:
            return "Not connected to any port"


    def is_connected(self):
        """
            Returns a boolean for whether a connection with the car was made.

            Note: this function returns False when:
            obd.status = OBDStatus.ELM_CONNECTED
        """
        return self.status() == OBDStatus.CAR_CONNECTED


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
            is supported by the car
        """
        return cmd in self.supported_commands


    def query(self, cmd, force=False):
        """
            primary API function. Sends commands to the car, and
            protects against sending unsupported commands.
        """

        if self.status() == OBDStatus.NOT_CONNECTED:
            debug("Query failed, no connection available", True)
            return OBDResponse()

        if not force and not self.supports(cmd):
            debug("'%s' is not supported" % str(cmd), True)
            return OBDResponse()


        # send command and retrieve message
        debug("Sending command: %s" % str(cmd))
        cmd_string = self.__build_command_string(cmd)
        messages = self.port.send_and_parse(cmd_string)

        # if we're sending a new command, note it
        if cmd_string:
            self.__last_command = cmd_string

        if not messages:
            debug("No valid OBD Messages returned", True)
            return OBDResponse()

        return cmd(messages) # compute a response object


    def __build_command_string(self, cmd):
        """ assembles the appropriate command string """
        cmd_string = cmd.command

        # only wait for as many ECUs as we've seen
        if self.fast and cmd.fast:
            cmd_string += str(len(self.port.ecus()))

        # if we sent this last time, just send
        if self.fast and (cmd_string == self.__last_command):
            cmd_string = ""

        return cmd_string
