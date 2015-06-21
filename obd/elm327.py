
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
from .utils import SerialStatus, numBitsSet
from .debug import debug



class ELM327:
    """
        Provides interface for the vehicles primary ECU.
        After instantiation with a portname (/dev/ttyUSB0, etc...),
        the following functions become available:

            send_and_parse()
            port_name()
            status()
            close()
    """

    _SUPPORTED_PROTOCOLS = {
        #"0" : None, # automatic mode
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

    def __init__(self, portname, baudrate):
        """Initializes port by resetting device and gettings supported PIDs. """

        self.__status      = SerialStatus.NOT_CONNECTED
        self.__port        = None
        self.__protocol    = UnknownProtocol([])


        # ------------- open port -------------
        try:
            debug("Opening serial port '%s'" % portname)
            self.__port = serial.Serial(portname, \
                                      baudrate = baudrate, \
                                      parity   = serial.PARITY_NONE, \
                                      stopbits = 1, \
                                      bytesize = 8, \
                                      timeout  = 3) # seconds
            debug("Serial port successfully opened on " + self.port_name)

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

        # ---------------------- ATSPA8 (protocol AUTO) -----------------------
        r = self.__send("ATSPA8")
        if not self.__isok(r):
            self.__error("ATSPA8 did not return 'OK'")
            return


        # try to communicate with the car, and load the correct protocol parser
        if self.load_protocol():
            self.__status = SerialStatus.CAR_CONNECTED
        else:
            self.__status = SerialStatus.ELM_CONNECTED


        # ------------------------------- done -------------------------------
        debug("Connection successful")


    def load_protocol(self):
        """
            Attempts communication with the car.

            Upon success, the appropriate protocol parser is loaded,
            and this function returns True
        """

        # -------------- 0100 (first command, SEARCH protocols) --------------
        r0100 = self.__send("0100")

        if self.__has_message(r0100, "UNABLE TO CONNECT"):
            debug("The ELM could not establish a connection with the car", True)
            return False

        # ------------------- ATDPN (list protocol number) -------------------
        r = self.__send("ATDPN")

        if not r:
            debug("Describe protocol command didn't return", True)
            return False

        p = r[0]

        # suppress any "automatic" prefix
        p = p[1:] if (len(p) > 1 and p.startswith("A")) else p[:-1]

        if p not in self._SUPPORTED_PROTOCOLS:
            debug("ELM responded with unknown protocol", True)
            return False

        # instantiate the correct protocol handler
        self.__protocol = self._SUPPORTED_PROTOCOLS[p](r0100)

        return True


    def __isok(self, lines, expectEcho=False):
        if not lines:
            return False
        if expectEcho:
            return len(lines) == 2 and lines[1] == 'OK'
        else:
            return len(lines) == 1 and lines[0] == 'OK'


    def __has_message(self, lines, message):
        for line in lines:
            if message in line:
                return True
        return False


    def __error(self, msg=None):
        """ handles fatal failures, print debug info and closes serial """

        self.close()

        debug("Connection Error:", True)
        if msg is not None:
            debug('    ' + str(msg), True)


    @property
    def port_name(self):
        if self.__port is not None:
            return self.__port.portstr
        else:
            return "No Port"


    @property
    def status(self):
        return self.__status


    def close(self):
        """
            Resets the device, and sets all
            attributes to unconnected states.
        """

        self.__status   = SerialStatus.NOT_CONNECTED
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

            Returns a list of Message objects
        """

        if self.__status == SerialStatus.NOT_CONNECTED:
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
            self.__port.flushInput() # dump everything in the input buffer
            self.__port.write(cmd.encode()) # turn the string into bytes and write
            self.__port.flush() # wait for the output buffer to finish transmitting
            debug("write: " + repr(cmd))
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
                        debug("__read() never recieved prompt character")
                        break

                    debug("__read() found nothing")
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
