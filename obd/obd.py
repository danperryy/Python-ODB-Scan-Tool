
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



class OBD(object):
	""" class representing an OBD-II connection with it's assorted sensors """

	def __init__(self, portstr=None):
		self.port = None
		self.supported_commands = []

		debug("========================== Starting python-OBD ==========================")
		self.connect(portstr) # initialize by connecting and loading sensors
		debug("=========================================================================")


	def connect(self, portstr=None):
		""" attempts to instantiate an OBDPort object. Loads commands on success"""

		if portstr is None:
			debug("Using scanSerial to select port")
			portnames = scanSerial()
			debug("Available ports: " + str(portnames))

			for port in portnames:

				self.port = OBDPort(port)

				if(self.port.state == State.Connected):
					# success! stop searching for serial
					break
		else:
			debug("Explicit port defined")
			self.port = OBDPort(portstr)

		# if a connection was made, query for commands
		if self.is_connected():
			self.load_commands()
		else:
			debug("Failed to connect")


	def close(self):
		if self.is_connected():
			debug("Closing connection")
			self.port.close()
			self.port = None


	# checks the port state for conncetion status
	def is_connected(self):
		return (self.port is not None) and self.port.is_connected()


	def get_port_name(self):
		if self.is_connected():
			return self.port.get_port_name()
		else:
			return "Not connected to any port"


	def load_commands(self):
		""" queries for available PIDs, sets their support status, and compiles a list of command objects """

		debug("querying for supported PIDs (commands)...")

		self.supported_commands = []

		pid_getters = commands.pid_getters()

		for get in pid_getters:
			# GET commands should sequentialy turn themselves on (become marked as supported)
			# MODE 1 PID 0 is marked supported by default 
			if not self.supports(get):
				continue

			response = self.send(get) # ask nicely

			if response.is_null():
				continue
			
			supported = response.value # string of binary 01010101010101

			# loop through PIDs binary
			for i in range(len(supported)):
				if supported[i] == "1":

					mode = get.get_mode_int()
					pid  = get.get_pid_int() + i + 1

					if commands.has_pid(mode, pid):
						c = commands[mode][pid]
						c.supported = True

						# don't add PID getters to the command list
						if c not in pid_getters:
							self.supported_commands.append(c)

		debug("finished querying with %d commands supported" % len(self.supported_commands))


	def print_commands(self):
		for c in self.supported_commands:
			print str(c)


	def supports(self, c):
		return commands.has_command(c) and c.supported


	def send(self, c):
		""" send the given command, retrieve and parse response """

		# check for a connection
		if not self.is_connected():
			debug("Query failed, no connection available", True)
			return Response() # return empty response

		# send the query
		debug("Sending command: %s" % str(c))
		r = self.port.write_and_read(c.get_command()) # send command and retrieve response
		return c.compute(r)                         # compute a response object
		

	def query(self, c, force=False):
		""" facade 'send' command, protects against sending unsupported commands """

		# check that the command is supported
		if not (self.supports(c) or force):
			debug("'%s' is not supported" % str(c), True)
			return Response() # return empty response
		else:
			return self.send(c)


	'''
	def query_DTC(self):
		""" read all DTCs """

		n = self.query(commands.STATUS).value['DTC Count'];

		codes = [];

		# poll until the number of commands received equals that returned from STATUS
		# or until this has looped 128 times (the max number of DTCs that STATUS reports)
		i = 0
		while (len(codes) < n) and (i < 128):
			codes += self.query(commands.GET_DTC).value
			i += 1

		return codes
	'''
