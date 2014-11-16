
import obd
import time
import threading
from utils import Response
from commands import OBDCommand


class Async():
	""" class representing an OBD-II connection """

	def __init__(self, portstr=None):
		self.connection = obd.OBD(portstr)
		self.running = True
		self.commands = {} # key = OBDCommand, value = Response
		
		if self.connection.is_connected():
			self.thread = threading.Thread(target=self.run, args=(self.connection,))
			self.thread.start()

	def close(self):
		self.running = False
		self.thread.join()
		self.connection.close

	def get(self, c):
		if self.commands.has_key(c):
			return self.commands[c]
		else:
			return Response()

	def add(self, *commands):
		for c in commands:
			if isinstance(c, OBDCommand) and self.connection.has_command(c):
				if not self.commands.has_key(c):
					self.commands[c] = Response() # give it an initial value

	def remove(self, c):
		self.commands.pop(c, None)

	def run(self, connection):
		# loop until the stop signal is recieved
		while self.running:
			if len(self.commands) > 0:
				# loop over the requested commands, and collect the result
				for c in self.commands:
					self.commands[c] = connection.query(c)
			else:
				time.sleep(1)
