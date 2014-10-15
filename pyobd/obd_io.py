 #!/usr/bin/env python
###########################################################################
# odb_io.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

import serial
import string
import time

import obd_sensors
from obd_utils import hex_to_int


GET_DTC_COMMAND   = "03"
CLEAR_DTC_COMMAND = "04"
GET_FREEZE_DTC_COMMAND = "07"


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

		print "Opening interface (serial port)"

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

		print "Interface successfully opened on " + self.get_port_name()
		print "Connecting to ECU..."

		try:
			self.send_command("atz")   # initialize
			time.sleep(1)
		except serial.SerialException as e:
			self.error(e)
			return

		self.ELMver = self.get_result()
		if self.ELMver is None :
			self.error("ELMver returned None")
			return

		print "atz response:" + self.ELMver
		self.send_command("ate0")  # echo off
		print "ate0 response:" + self.get_result()
		self.send_command("0100")
		ready = self.get_result()

		if ready is None:
			self.state = State.Unconnected
			return

		print "0100 response:" + ready


	def error(self, msg=None):
		""" called when connection error has been encountered """
		print "Connection Error:"
		if msg is not None:
			print msg
		self.port.close()
		self.state = State.Unconnected


	def get_port_name(self):
		return self.port.portstr if (self.port is not None) else "No Port"


	def close(self):
		""" Resets device and closes all associated filehandles"""

		if (self.port != None) and self.state == State.Connected:
			self.send_command("atz")
			self.port.close()

		self.port = None
		self.ELMver = "Unknown"

	def send_command(self, cmd):
		"""Internal use only: not a public interface"""
		if self.port:
			self.port.flushOutput()
			self.port.flushInput()
			for c in cmd:
				self.port.write(c)
			self.port.write("\r\n")
			#print "Send command:" + cmd

	def interpret_result(self,code):
		"""Internal use only: not a public interface"""
		# Code will be the string returned from the device.
		# It should look something like this:
		# '41 11 0 0\r\r'

		# 9 seems to be the length of the shortest valid response
		if len(code) < 7:
			#raise Exception("BogusCode")
			print "boguscode?"+code

		# get the first thing returned, echo should be off
		code = string.split(code, "\r")
		code = code[0]

		#remove whitespace
		code = string.split(code)
		code = string.join(code, "")

		#cables can behave differently 
		if code[:6] == "NODATA": # there is no such sensor
			return "NODATA"

		# first 4 characters are code from ELM
		code = code[4:]
		return code

	def get_result(self):
		"""Internal use only: not a public interface"""
		#time.sleep(0.01)
		repeat_count = 0
		if self.port is not None:
			buffer = ""
			while 1:
				c = self.port.read(1)
				if len(c) == 0:
					if(repeat_count == 5):
						break
					print "Got nothing\n"
					repeat_count = repeat_count + 1
					continue

				if c == '\r':
					continue

				if c == ">":
					break;

				if buffer != "" or c != ">": #if something is in buffer, add everything
					buffer = buffer + c

			#print "Get result:" + buffer
			if(buffer == ""):
				return None
			return buffer
		else:
			print "NO self.port!"
		return None

	# get sensor value from command
	def get_sensor_value(self,sensor):
		"""Internal use only: not a public interface"""
		cmd = sensor.cmd
		self.send_command(cmd)
		data = self.get_result()

		if data:
			data = self.interpret_result(data)
			if data != "NODATA":
				data = sensor.value(data)
		else:
			return "NORESPONSE"

		return data

	# return string of sensor name and value from sensor index
	def sensor(self , sensor_index):
		"""Returns 3-tuple of given sensors. 3-tuple consists of
		(Sensor Name (string), Sensor Value (string), Sensor Unit (string) ) """
		sensor = obd_sensors.SENSORS[sensor_index]
		r = self.get_sensor_value(sensor)
		return (sensor.name,r, sensor.unit)


	def sensor_names(self):
		"""Internal use only: not a public interface"""
		names = []
		for s in obd_sensors.SENSORS:
			names.append(s.name)
		return names

	def get_tests_MIL(self):
		statusText=["Unsupported","Supported - Completed","Unsupported","Supported - Incompleted"]

		statusRes = self.sensor(1)[1] #GET values
		statusTrans = [] #translate values to text

		statusTrans.append(str(statusRes[0])) #DTCs

		if statusRes[1]==0: #MIL
			statusTrans.append("Off")
		else:
			statusTrans.append("On")

		for i in range(2,len(statusRes)): #Tests
			statusTrans.append(statusText[statusRes[i]]) 

		return statusTrans

	#
	# fixme: j1979 specifies that the program should poll until the number
	# of returned DTCs matches the number indicated by a call to PID 01
	#
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
			self.send_command(GET_DTC_COMMAND)
			res = self.get_result()
			print "DTC result:" + res
			for i in range(0, 3):
				val1 = hex_to_int(res[3+i*6:5+i*6])
				val2 = hex_to_int(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
				val  = (val1<<8)+val2 #DTC val as int

				if val==0: #skip fill of last packet
					break

				DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str((val&0x0f00)>>8)+str((val&0x00f0)>>4)+str(val&0x000f)
				DTCCodes.append(["Active",DTCStr])

		#read mode 7
		self.send_command(GET_FREEZE_DTC_COMMAND)
		res = self.get_result()

		if res[:7] == "NODATA": #no freeze frame
			return DTCCodes

		print "DTC freeze result:" + res
		for i in range(0, 3):
			val1 = hex_to_int(res[3+i*6:5+i*6])
			val2 = hex_to_int(res[6+i*6:8+i*6]) #get DTC codes from response (3 DTC each 2 bytes)
			val  = (val1<<8)+val2 #DTC val as int

			if val==0: #skip fill of last packet
				break

			DTCStr=dtcLetters[(val&0xC000)>14]+str((val&0x3000)>>12)+str((val&0x0f00)>>8)+str((val&0x00f0)>>4)+str(val&0x000f)
			DTCCodes.append(["Passive",DTCStr])

		return DTCCodes

	def clear_dtc(self):
		"""Clears all DTCs and freeze frame data"""
		self.send_command(CLEAR_DTC_COMMAND)     
		r = self.get_result()
		return r

	def log(self, sensor_index, filename): 
		file = open(filename, "w")
		start_time = time.time() 
		if file:
			data = self.sensor(sensor_index)
			file.write("%s     \t%s(%s)\n" % \
						 ("Time", string.strip(data[0]), data[2])) 
			while 1:
				now = time.time()
				data = self.sensor(sensor_index)
				line = "%.6f,\t%s\n" % (now - start_time, data[1])
				file.write(line)
				file.flush()
