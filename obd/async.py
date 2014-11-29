
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
# async.py                                                             #
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

import obd
import time
import threading
from utils import Response
from commands import OBDCommand


class Async(obd.OBD):
	""" subclass representing an OBD-II connection """

	def __init__(self, portstr=None):
		super(Async, self).__init__(portstr)
		self.commands = {} # key = OBDCommand, value = Response
		self.thread = None
		self.running = False
		self.start()

	def start(self):
		self.running = True
		if self.is_connected():
			self.thread = threading.Thread(target=self.run)
			self.thread.daemon = True
			self.thread.start()

	def stop(self):
		self.running = False
		if self.thread is not None:
			self.thread.join()
			self.thread = None

	def close(self):
		self.stop()
		self.close()

	def watch(self, c):

		if not isinstance(c, OBDCommand):
			return False

		if not self.has_command(c):
			return False

		if not self.commands.has_key(c):
			self.commands[c] = Response() # give it an initial value

		return True

	def unwatch(self, c):
		self.commands.pop(c, None)

	def get(self, c):
		if self.commands.has_key(c):
			return self.commands[c]
		else:
			return Response()

	def run(self):
		# loop until the stop signal is recieved
		while self.running:

			if len(self.commands) > 0:
				# loop over the requested commands, and collect the result
				for c in self.commands:
					self.commands[c] = self.query(c)
			else:
				time.sleep(1)
