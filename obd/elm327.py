
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
# port.py                                                              #
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

import serial
import time
from protocols import *
from utils import strip, numBitsSet
from debug import debug



class ELM327:
	"""
		Provides interface for the vehicles primary ECU.
		After instantiation with a portname (/dev/ttyUSB0, etc...),
		the following functions become available:

			send_and_parse()
			get_port_name()
			is_connected()
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

	def __init__(self, portname):
		"""Initializes port by resetting device and gettings supported PIDs. """

		self.__connected   = False
		self.__port        = None
		self.__protocol    = None
		self.__primary_ecu = None # message.tx_id

		# ------------- open port -------------

		debug("Opening serial port '%s'" % portname)

		try:
			self.__port = serial.Serial(portname, \
									  baudrate = 38400, \
									  parity   = serial.PARITY_NONE, \
									  stopbits = 1, \
									  bytesize = 8, \
									  timeout  = 1) # seconds

		except serial.SerialException as e:
			self.__error(e)
			return
		except OSError as e:
			self.__error(e)
			return

		debug("Serial port successfully opened on " + self.get_port_name())


		# ---------------------------- ATZ (reset) ----------------------------
		try:
			r = self.__send("ATZ", delay=1) # wait 1 second for ELM to initialize
			# return data can be junk, so don't bother checking
		except serial.SerialException as e:
			self.__error(e)
			return


		# -------------------------- ATE0 (echo OFF) --------------------------
		r = self.__send("ATE0")
		r = strip(r)
		if not r.endswith("OK"):
			self.__error("ATE0 did not return 'OK'")
			return


		# ------------------------- ATH1 (headers ON) -------------------------
		r = self.__send("ATH1")
		r = strip(r)
		if r != 'OK':
			self.__error("ATH1 did not return 'OK', or echoing is still ON")
			return


		# ----------------------- ATSP0 (protocol AUTO) -----------------------
		r = self.__send("ATSP0")
		r = strip(r)
		if r != 'OK':
			self.__error("ATSP0 did not return 'OK'")
			return


		# -------------- 0100 (first command, SEARCH protocols) --------------
		r0100 = self.__send("0100", delay=1) # give it a second to search


		# ------------------- ATDPN (list protocol number) -------------------
		r = self.__send("ATDPN")
		r = strip(r)
		# suppress any "automatic" prefix
		r = r[1:] if (len(r) > 1 and r.startswith("A")) else r

		if r not in _SUPPORTED_PROTOCOLS:
			self.__error("ELM responded with unknown protocol")
			return

		self.__protocol = _SUPPORTED_PROTOCOLS[r]()


		# Now that a protocol has been selected, we can figure out
		# which ECU is the primary.

		m = self.__protocol(r0100)
		self.__primary_ecu = self.__find_primary_ecu(m)
		if self.__primary_ecu is None:
			self.__error("Failed to choose primary ECU")
			return

		# ------------------------------- done -------------------------------
		debug("Connection successful")
		self.__connected = True


	def __find_primary_ecu(messages):
		"""
			Given a list of messages from different ECUS,
			(in response to the 0100 PID listing command)
			choose the ID of the primary ECU
		"""

		if len(messages) == 0:
			return None
		elif len(messages) == 1:
			return messages[0].tx_id
		else:
			# first, try filtering for the standard ECU IDs
			test = lambda m: m.tx_id == self.__protocol.PRIMARY_ECU

			if bool(filter(test, messages)):
				return self.__protocol.PRIMARY_ECU
			else:
				# last resort solution, choose ECU
				# with the most PIDs supported
				best = 0
				tx_id = None

				for message in messages:
					bits = sum([numBitsSet(b) for b in message.data_bytes])
					if bits > best:
						best = bits
						tx_id = message.tx_id

				return tx_id


	def __error(self, msg=None):
		""" handles fatal failures, print debug info and closes serial """
		
		debug("Connection Error:", True)

		if msg is not None:
			debug('    ' + str(msg), True)

		if self.__port is not None:
			self.__port.close()

		self.__connected = False


	def get_port_name(self):
		return self.__port.portstr if (self.__port is not None) else "No Port"


	def is_connected(self):
		return self.__connected and (self.__port is not None)


	def close(self):
		"""
			Resets the device, and clears all attributes to unconnected state
		"""

		if (self.__port != None) and self.__connected:
			self.__write("ATZ")
			self.__port.close()

			self.__connected   = False
			self.__port        = None
			self.__protocol    = None
			self.__primary_ecu = None


	def send_and_parse(self, cmd, delay=None):
		"""
			send() function used to service all OBDCommands

			Sends the given command string (rejects "AT" command),
			parses the response string with the appropriate protocol object.

			Returns the Message object from the primary ECU, or None,
			if no appropriate response was recieved.
		"""

		if "AT" not in cmd.upper():

			r = self.__send(cmd, delay)

			messages = self.__protocol(r) # parses string into list of messages

			# select the first message with the ECU ID we're looking for
			# TODO: use ELM header settings to query ECU by address directly
			for message in messages:
				if message.tx_id == self.__primary_ecu:
					return message

		else:
			debug("Rejected sending AT command")
			return None


	def __send(self, cmd, delay=None):
		"""
			unprotected send() function

			will __write() the given string, no questions asked.
			returns result of __read() after an optional delay.
		"""

		self.__write(cmd)

		if delay is not None:
			time.sleep(delay)

		r = self.__read()

		return r


	def __write(self, cmd):
		"""
			"low-level" function to write a string to the port
		"""

		if self.is_connected():
			cmd += "\r\n" # terminate
			self.__port.flushOutput()
			self.__port.flushInput()
			self.__port.write(cmd)
			debug("write: " + repr(cmd))
		else:
			debug("cannot perform write() when unconnected", True)


	def __read(self):
		"""
			"low-level" read function

			accumulates characters until the prompt character is seen
			returns the raw string
		"""

		attempts = 2
		result = ""

		if self.__port:
			while True:
				c = self.__port.read(1)

				# if nothing was recieved
				if not c:

					if attempts <= 0:
						break

					debug("__read() found nothing")
					attempts -= 1
					continue

				# end on chevron (ELM prompt character)
				if c == ">":
					break

				# skip null characters (ELM spec page 9)
				if c == '\x00':
					continue

				result += c # whatever is left must be part of the response
		else:
			debug("cannot perform read() when unconnected", True)

		debug("read: " + repr(result))
		return result
