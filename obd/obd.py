
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

from port import OBDPort, State
from commands import commands
from utils import scanSerial, Response
from debug import debug



class OBD():
	""" class representing an OBD-II connection with it's assorted sensors """

	def __init__(self, portstr=None):
		self.port = None
		self.supportedCommands = []

		# initialize by connecting and loading sensors
		debug("Starting python-OBD")
		if self.connect(portstr):
			self.load_commands()
		else:
			debug("Failed to connect")


	def connect(self, portstr=None):
		""" attempts to instantiate an OBDPort object. Return boolean for success/failure"""

		if portstr is None:
			debug("Using scanSerial to select port")
			portnames = scanSerial()

			for port in portnames:

				self.port = OBDPort(port)

				if(self.port.state == State.Connected):
					# success! stop searching for serial
					break
		else:
			debug("Explicit port defined")
			self.port = OBDPort(portstr)

		return self.is_connected()

	# checks the port state for conncetion status
	def is_connected(self):
		return (self.port is not None) and self.port.is_connected()


	def get_port_name(self):
		return self.port.get_port_name()


	def load_commands(self):
		""" queries for available PIDs, sets their support status, and compiles a list of command objects """

		debug("querying for supported PIDs (commands)...")

		self.supportedCommands = []

		pid_getters = commands.pid_getters()

		for get in pid_getters:
			# GET commands should sequentialy turn themselves on (become marked as supported)
			# MODE 1 PID 0 is marked supported by default 
			if not self.has_command(get):
				continue

			response = self.query(get) # ask nicely

			if response.isEmpty():
				continue
			
			supported = response.value # string of binary 01010101010101

			# loop through PIDs binary
			for i in range(len(supported)):
				if supported[i] == "1":

					mode = get.get_mode_int()
					pid  = get.get_pid_int() + i + 1

					if commands.has(mode, pid):
						c = commands[mode][pid]
						c.supported = True

						# don't add PID getters to the command list
						if c not in pid_getters:
							self.supportedCommands.append(c)

		debug("finished querying with %d commands supported" % len(self.supportedCommands))


	def print_commands(self):
		for c in self.supportedCommands:
			print str(c)

	def has_command(self, c):
		return commands.has(c.get_mode_int(), c.get_pid_int()) and c.supported

	def query(self, command, force=False):
		#print "TX: " + str(command)
		
		if self.has_command(command) or force:
			debug("Sending command: %s" % str(command))

			# send command to the port
			self.port.send(command.get_command())
			
			# get the data, and compute a response object
			return command.compute(self.port.get())
		
		else:
			print "'%s' is not supported" % str(command)
			return Response() # return empty response
