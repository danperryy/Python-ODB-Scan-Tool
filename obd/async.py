
import obd
import time
import threading
from utils import Response
from commands import OBDCommand


class Async():
	""" class representing an OBD-II connection """

	def __init__(self, portstr=None):
		self.connection = obd.OBD(portstr)
		self.commands = {} # key = OBDCommand, value = Response
		self.thread = None
		self.running = False
		self.start()

	def start(self):
		self.running = True
		if self.connection.is_connected():
			self.thread = threading.Thread(target=self.run, args=(self.connection,))
			self.thread.start()

	def stop(self):
		self.running = False
		if self.thread is not None:
			self.thread.join()
			self.thread = None

	def close(self):
		self.stop()
		self.connection.close()

	def watch(self, *commands):

		errors = []

		for c in commands:
			if not isinstance(c, OBDCommand):
				errors.append(c)
				continue

			if not self.connection.has_command(c):
				errors.append(c)
				continue

			if not self.commands.has_key(c):
				self.commands[c] = Response() # give it an initial value

		return errors

	def unwatch(self, c):
		self.commands.pop(c, None)

	def get(self, c):
		if self.commands.has_key(c):
			return self.commands[c]
		else:
			return Response()

	def run(self, connection):
		# loop until the stop signal is recieved
		while self.running:

			if len(self.commands) > 0:
				# loop over the requested commands, and collect the result
				for c in self.commands:
					self.commands[c] = connection.query(c)
			else:
				time.sleep(1)
