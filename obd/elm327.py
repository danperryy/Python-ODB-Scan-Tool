
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
# elm327.py                                                            #
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

import re
import serial
import time
from .protocols import *
from .utils import OBDStatus
from .debug import debug



class ELM327:
    """
        Handles communication with the ELM327 adapter.

        After instantiation with a portname (/dev/ttyUSB0, etc...),
        the following functions become available:

            send_and_parse()
            close()
            status()
            port_name()
            protocol_name()
            ecus()
    """

    _SUPPORTED_PROTOCOLS = {
        #"0" : None, # Automatic Mode. This isn't an actual protocol. If the
                     # ELM reports this, then we don't have enough
                     # information. see auto_protocol()
        "1" : SAE_J1850_PWM,
        "2" : SAE_J1850_VPW,
        "3" : ISO_9141_2,
        "4" : ISO_14230_4_5baud,
        "5" : ISO_14230_4_fast,
        "6" : ISO_15765_4_11bit_500k,
        "7" : ISO_15765_4_29bit_500k,
        "8" : ISO_15765_4_11bit_250k,
        "9" : ISO_15765_4_29bit_250k,
        "A" : SAE_J1939,
        #"B" : None, # user defined 1
        #"C" : None, # user defined 2
    }

    # used as a fallback, when ATSP0 doesn't cut it
    _TRY_PROTOCOL_ORDER = [
        "6", # ISO_15765_4_11bit_500k
        "8", # ISO_15765_4_11bit_250k
        "1", # SAE_J1850_PWM
        "7", # ISO_15765_4_29bit_500k
        "9", # ISO_15765_4_29bit_250k
        "2", # SAE_J1850_VPW
        "3", # ISO_9141_2
        "4", # ISO_14230_4_5baud
        "5", # ISO_14230_4_fast
        "A", # SAE_J1939
    ]


    def __init__(self, portname, baudrate, protocol):
        """Initializes port by resetting device and gettings supported PIDs. """

        self.__status   = OBDStatus.NOT_CONNECTED
        self.__port     = None
        self.__protocol = UnknownProtocol([])


        # ------------- open port -------------
        try:
            debug("Opening serial port '%s'" % portname)
            self.__port = serial.Serial(portname, \
                                        baudrate = baudrate, \
                                        parity   = serial.PARITY_NONE, \
                                        stopbits = 1, \
                                        bytesize = 8, \
                                        timeout  = 3) # seconds
            debug("Serial port successfully opened on " + self.port_name())

        except serial.SerialException as e:
            self.__error(e)
            return
        except OSError as e:
            self.__error(e)
            return


        # ---------------------------- ATZ (reset) ----------------------------
        try:
            self.__send("ATZ", delay=1) # wait 1 second for ELM to initialize
            # return data can be junk, so don't bother checking
        except serial.SerialException as e:
            self.__error(e)
            return

        # -------------------------- ATE0 (echo OFF) --------------------------
        r = self.__send("ATE0")
        if not self.__isok(r, expectEcho=True):
            self.__error("ATE0 did not return 'OK'")
            return

        # ------------------------- ATH1 (headers ON) -------------------------
        r = self.__send("ATH1")
        if not self.__isok(r):
            self.__error("ATH1 did not return 'OK', or echoing is still ON")
            return

        # ------------------------ ATL0 (linefeeds OFF) -----------------------
        r = self.__send("ATL0")
        if not self.__isok(r):
            self.__error("ATL0 did not return 'OK'")
            return

        # by now, we've successfuly communicated with the ELM, but not the car
        self.__status = OBDStatus.ELM_CONNECTED

        # try to communicate with the car, and load the correct protocol parser
        if self.load_protocol(protocol):
            self.__status = OBDStatus.CAR_CONNECTED
            debug("Connection successful")
        else:
            debug("Connected to the adapter, but failed to connect to the vehicle", True)


    def load_protocol(self, protocol):
        if protocol is not None:
            # an explicit protocol was specified
            if protocol not in self._SUPPORTED_PROTOCOLS:
                debug("%s is not a valid protocol. Please use \"1\" through \"A\"", True)
                return False
            return self.manual_protocol(protocol)
        else:
            # auto detect the protocol
            return self.auto_protocol()


    def manual_protocol(self, protocol):

        r = self.__send("ATTP%s" % protocol)
        r0100 = self.__send("0100")

        if not self.__has_message(r0100, "UNABLE TO CONNECT"):
            # success, found the protocol
            self.__protocol = self._SUPPORTED_PROTOCOLS[protocol](r0100)
            return True

        return False


    def auto_protocol(self):
        """
            Attempts communication with the car.

            If no protocol is specified, then protocols at tried with `ATTP`

            Upon success, the appropriate protocol parser is loaded,
            and this function returns True
        """

        # -------------- try the ELM's auto protocol mode --------------
        r = self.__send("ATSP0")

        # -------------- 0100 (first command, SEARCH protocols) --------------
        r0100 = self.__send("0100")

        # ------------------- ATDPN (list protocol number) -------------------
        r = self.__send("ATDPN")
        if len(r) != 1:
            debug("Failed to retrieve current protocol", True)
            return False


        p = r[0] # grab the first (and only) line returned
        # suppress any "automatic" prefix
        p = p[1:] if (len(p) > 1 and p.startswith("A")) else p

        # check if the protocol is something we know
        if p in self._SUPPORTED_PROTOCOLS:
            # jackpot, instantiate the corresponding protocol handler
            self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
            return True
        else:
            # an unknown protocol
            # this is likely because not all adapter/car combinations work
            # in "auto" mode. Some respond to ATDPN responded with "0"
            debug("ELM responded with unknown protocol. Trying them one-by-one")

            for p in self._TRY_PROTOCOL_ORDER:
                r = self.__send("ATTP%s" % p)
                r0100 = self.__send("0100")
                if not self.__has_message(r0100, "UNABLE TO CONNECT"):
                    # success, found the protocol
                    self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)
                    return True

        # if we've come this far, then we have failed...
        return False



    def __isok(self, lines, expectEcho=False):
        if not lines:
            return False
        if expectEcho:
            # don't test for the echo itself
            # allow the adapter to already have echo disabled
            return self.__has_message(lines, 'OK')
        else:
            return len(lines) == 1 and lines[0] == 'OK'


    def __has_message(self, lines, text):
        for line in lines:
            if text in line:
                return True
        return False


    def __error(self, msg=None):
        """ handles fatal failures, print debug info and closes serial """

        self.close()

        debug("Connection Error:", True)
        if msg is not None:
            debug('    ' + str(msg), True)


    def port_name(self):
        if self.__port is not None:
            return self.__port.portstr
        else:
            return "No Port"


    def status(self):
        return self.__status


    def ecus(self):
        return self.__protocol.ecu_map.values()


    def protocol_name(self):
        return self.__protocol.ELM_NAME


    def protocol_id(self):
        return self.__protocol.ELM_ID


    def close(self):
        """
            Resets the device, and sets all
            attributes to unconnected states.
        """

        self.__status   = OBDStatus.NOT_CONNECTED
        self.__protocol = None

        if self.__port is not None:
            self.__write("ATZ")
            self.__port.close()
            self.__port = None


    def send_and_parse(self, cmd):
        """
            send() function used to service all OBDCommands

            Sends the given command string, and parses the
            response lines with the protocol object.

            An empty command string will re-trigger the previous command

            Returns a list of Message objects
        """

        if self.__status == OBDStatus.NOT_CONNECTED:
            debug("cannot send_and_parse() when unconnected", True)
            return None

        lines = self.__send(cmd)
        messages = self.__protocol(lines)
        return messages


    def __send(self, cmd, delay=None):
        """
            unprotected send() function

            will __write() the given string, no questions asked.
            returns result of __read() (a list of line strings)
            after an optional delay.
        """

        self.__write(cmd)

        if delay is not None:
            debug("wait: %d seconds" % delay)
            time.sleep(delay)

        return self.__read()


    def __write(self, cmd):
        """
            "low-level" function to write a string to the port
        """

        if self.__port:
            cmd += "\r\n" # terminate
            debug("write: " + repr(cmd))
            self.__port.flushInput() # dump everything in the input buffer
            self.__port.write(cmd.encode()) # turn the string into bytes and write
            self.__port.flush() # wait for the output buffer to finish transmitting
        else:
            debug("cannot perform __write() when unconnected", True)


    def __read(self):
        """
            "low-level" read function

            accumulates characters until the prompt character is seen
            returns a list of [/r/n] delimited strings
        """

        attempts = 2
        buffer = b''

        if self.__port:
            while True:
                c = self.__port.read(1)

                # if nothing was recieved
                if not c:

                    if attempts <= 0:
                        debug("Failed to read port, giving up")
                        break

                    debug("Failed to read port, trying again...")
                    attempts -= 1
                    continue

                # end on chevron (ELM prompt character)
                if c == b'>':
                    break

                # skip null characters (ELM spec page 9)
                if c == b'\x00':
                    continue

                buffer += c # whatever is left must be part of the response
        else:
            debug("cannot perform __read() when unconnected", True)
            return ""

        debug("read: " + repr(buffer))

        # convert bytes into a standard string
        raw = buffer.decode()

        # splits into lines
        # removes empty lines
        # removes trailing spaces
        lines = [ s.strip() for s in re.split("[\r\n]", raw) if bool(s) ]

        return lines
