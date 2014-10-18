#!/usr/bin/env python

import time

from port import OBDPort, State
from commands import commands
from utils import scanSerial



class OBD():
	""" class representing an OBD-II connection with it's assorted sensors """

	def __init__(self, portstr=None):
		self.port = None
		self.supportedCommands = []

		# initialize by connecting and loading sensors
		if self.connect(portstr):
			self.load_commands()


	def connect(self, portstr=None):
		""" attempts to instantiate an OBDPort object. Return boolean for success/failure"""

		if portstr is None:
			portnames = scanSerial()

			for port in portnames:

				self.port = OBDPort(port)

				if(self.port.state == State.Connected):
					# success! stop searching for serial
					break
		else:
			self.port = OBDPort(portstr)

		return self.is_connected()


	def is_connected(self):
		return (self.port is not None) and (self.port.state == State.Connected)


	def get_port_name(self):
		return self.port.get_port_name()


	def load_commands(self):
		""" queries for available PIDs, and compiles lists of command objects """

		self.supportedCommands = []

		# Find supported sensors - by getting PIDs from OBD (sensor zero)
		# its a string of binary 01010101010101 
		# 1 means the sensor is supported
		supported = self.send_command(commands[1][0]) # mode 01, command 00

		count = min(len(supported), len(commands[1]))

		# loop through PIDs binary
		for i in range(count):
			if supported[i] == "1":
				c = commands[1][i]
				c.supported = True
				self.supportedCommands.append(c)


	def print_commands(self):
		for c in self.supportedCommands:
			print str(c)

	def has_command(self, c):
		return c.supported

	def query(self, command):
		if self.has_command(command):
			return self.port.get_sensor_value(command)
		else:





if __name__ == "__main__":

	o = OBD()
	time.sleep(3)
	if not o.is_connected():
		print "Not connected"
	else:
		print "Connected to " + o.get_port_name()
		o.print_commands()
