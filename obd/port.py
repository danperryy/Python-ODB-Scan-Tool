
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2014 Brendan Whitfield (bcw7044@rit.edu)                   #
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
import string
import time
from utils import Response, unhex
from debug import debug


class State():
	""" Enum for connection states """
	Unconnected, Connected = range(2)


class OBDPort:
	""" OBDPort abstracts all communication with OBD-II device."""

	def __init__(self, portname):
		"""Initializes port by resetting device and gettings supported PIDs. """

		# These should really be set by the user.
		baud     = 38400
		databits = 8
		parity   = serial.PARITY_NONE
		stopbits = 1
		timeout  = 2 #seconds

		self.ELMver = "Unknown"
		self.state  = State.Connected
		self.port   = None

		debug("Opening serial port...")

		try:
			self.port = serial.Serial(portname, \
									  baud, \
									  parity = parity, \
									  stopbits = stopbits, \
									  bytesize = databits, \
									  timeout = timeout)

		except serial.SerialException as e:
			self.error(e)
			return
		except OSError as e:
			self.error(e)
			return

		debug("Serial port successfully opened on " + self.get_port_name())

		try:
			self.send("atz")   # initialize
			time.sleep(1)
			self.ELMver = self.get()

			if self.ELMver is None :
				self.error("ELMver did not return")
				return
			
			debug("atz response: " + self.ELMver)
		
		except serial.SerialException as e:
			self.error(e)
			return

		self.send("ate0")  # echo off
		debug("ate0 response: " + self.get())
		debug("Connected to ECU")


	def error(self, msg=None):
		""" called when connection error has been encountered """
		debug("Connection Error:", True)

		if msg is not None:
			debug(msg, True)
		
		if self.port is not None:
			self.port.close()
		
		self.state = State.Unconnected


	def get_port_name(self):
		return self.port.portstr if (self.port is not None) else "No Port"

	def is_connected(self):
		return self.state == State.Connected

	def close(self):
		""" Resets device and closes all associated filehandles"""

		if (self.port != None) and (self.state == State.Connected):
			self.send("atz")
			self.port.close()

		self.port = None
		self.ELMver = "Unknown"


	# sends the hex string to the port
	def send(self, cmd):
		if self.port:
			self.port.flushOutput()
			self.port.flushInput()
			for c in cmd:
				self.port.write(c)
			self.port.write("\r\n")

	# accumulates and returns the ports response
	def get(self):
		"""Internal use only: not a public interface"""

		attempts = 5
		result = ""

		if self.port is not None:
			while 1:
				c = self.port.read(1)

				# if nothing was recieved
				if len(c) == 0:

					if(attempts <= 0):
						break

					debug("get() found nothing")
					
					attempts -= 1
					continue

				# skip carraige returns
				if c == '\r':
					continue

				# end on chevron
				if c == ">":
					break;
				else: # whatever is left must be part of the response
					result = result + c
		else:
			debug("NO self.port!", True)

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
			self.send(GET_DTC_COMMAND)
			res = self.get()
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
		self.send(GET_FREEZE_DTC_COMMAND)
		res = self.get()

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
