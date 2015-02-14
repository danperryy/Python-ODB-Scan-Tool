
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
from utils import strip
from debug import debug



class ELM327:
	""" ELM327 abstracts all communication with OBD-II device."""

	_SUPPORTED_PROTOCOLS = {
		"0" : None,
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
		"B" : None,
		"C" : None,
	}

	def __init__(self, portname):
		"""Initializes port by resetting device and gettings supported PIDs. """

		self.connected = False
		self.port      = None
		self.protocol  = None

		# ------------- open port -------------

		debug("Opening serial port '%s'" % portname)

		try:
			self.port = serial.Serial(portname, \
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
			r = self.send("ATZ", delay=1) # wait 1 second for ELM to initialize
			# return data can be junk, so don't bother checking
		except serial.SerialException as e:
			self.__error(e)
			return


		# -------------------------- ATE0 (echo OFF) --------------------------
		r = self.send("ATE0")
		r = strip(r)
		if not r.endswith("OK"):
			self.__error("ATE0 did not return 'OK'")
			return


		# ------------------------- ATH1 (headers ON) -------------------------
		r = self.send("ATH1")
		r = strip(r)
		if r != 'OK':
			self.__error("ATH1 did not return 'OK', or echoing is still ON")
			return


		# ----------------------- ATSP0 (protocol AUTO) -----------------------
		r = self.send("ATSP0")
		r = strip(r)
		if r != 'OK':
			self.__error("ATSP0 did not return 'OK'")
			return


		# -------------- 0100 (first command, SEARCH protocols) --------------
		r = self.send("0100", delay=1) # give it a second to search


		# ------------------- ATDPN (list protocol number) -------------------
		r = self.send("ATDPN")
		r = strip(r)
		# suppress any "automatic" prefix
		r = r[1:] if (len(r) > 1 and r.startswith("A")) else r

		if r not in _SUPPORTED_PROTOCOLS:
			self.__error("ELM responded with unknown protocol")
			return

		self.protocol = _SUPPORTED_PROTOCOLS[r]()


		# ------------------------------- done -------------------------------
		debug("Connection successful")
		self.connected = True


	def __error(self, msg=None):
		""" handles fatal failures, print debug info and closes serial """
		
		debug("Connection Error:", True)

		if msg is not None:
			debug('    ' + str(msg), True)

		if self.port is not None:
			self.port.close()

		self.connected = False


	def get_port_name(self):
		return self.port.portstr if (self.port is not None) else "No Port"


	def is_connected(self):
		return self.connected


	def close(self):
		""" Resets device and closes all associated filehandles"""

		if (self.port != None) and self.connected:
			self.__write("ATZ")
			self.port.close()

			self.connected = False
			self.port      = None
			self.protocol  = None


	def send_and_parse(self, cmd, delay=None):

		r = self.send(cmd, delay)

		messages = self.protocol(r) # parses string into list of messages

		# if more than one ECUs have responded, pick the primary
		# TODO: add support for more ECU types
		if len(messages) > 1:
			messages = filter(lambda m: m.tx_id == self.protocol.PRIMARY_ECU, messages)

		return messages[0]


	def send(self, cmd, delay=None):

		self.__write(cmd)

		if delay is not None:
			time.sleep(delay)

		r = self.__read()

		return r # return raw string only


	# sends the hex string to the port
	def __write(self, cmd):
		if self.port:
			cmd += "\r\n" # terminate
			self.port.flushOutput()
			self.port.flushInput()
			self.port.write(cmd)
			debug("write: " + repr(cmd))
		else:
			debug("cannot perform write() when unconnected", True)


	# accumulates until the prompt character is seen
	# returns raw string
	def __read(self):

		attempts = 2
		result = ""

		if self.port:
			while True:
				c = self.port.read(1)

				# if nothing was recieved
				if not c:

					if attempts <= 0:
						break

					debug("read() found nothing")
					attempts -= 1
					continue

				# end on chevron
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


	#
	# fixme: j1979 specifies that the program should poll until the number
	# of returned DTCs matches the number indicated by a call to PID 01
	#
	'''
	def get_dtc(self):
		"""Returns a list of all pending DTC codes. Each element consists of
		a 2-tuple: (DTC code (string), Code description (string) )"""
		dtcLetters = ["P", "C", "B", "U"]
		r = self.sensor(1)[1] #data
		dtcNumber = r[0]
		mil = r[1]
		DTCCodes = []


		print "Number of stored DTC:" + str(dtcNumber) + " MIL: " + str(mil)
		# get all DTC, 3 per mesg response
		for i in range(0, ((dtcNumber+2)/3)):
			self.write(GET_DTC_COMMAND)
			res = self.read()
			print "DTC result:" + res
			for i in range(0, 3):
				val1 = unhex(res[3+i*6:5+i*6])
				val2 = unhex(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
				val  = (val1<<8)+val2 #DTC val as int

				if val==0: #skip fill of last packet
					break

				DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str((val&0x0f00)>>8)+str((val&0x00f0)>>4)+str(val&0x000f)
				DTCCodes.append(["Active",DTCStr])

		#read mode 7
		self.write(GET_FREEZE_DTC_COMMAND)
		res = self.read()

		if res[:7] == "NODATA": #no freeze frame
			return DTCCodes

		print "DTC freeze result:" + res
		for i in range(0, 3):
			val1 = unhex(res[3+i*6:5+i*6])
			val2 = unhex(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
			val  = (val1<<8)+val2 #DTC val as int

			if val==0: #skip fill of last packet
				break

			DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str((val&0x0f00)>>8)+str((val&0x00f0)>>4)+str(val&0x000f)
			DTCCodes.append(["Passive",DTCStr])

		return DTCCodes
	'''
