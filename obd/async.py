
import obd
import time
import threading
from util import Response


class OBDThread(threading.Thread):
	def __init__(self, portstr):
		super(OBDThread, self).__init__()

		self.connection = obd.OBD(portstr)
		self._stop = threading.Event()
		self.commands = {} # key = OBDCommand, value = Response

	def stop(self):
		self._stop.set()

	def addCommand(self, c):
		if not self.commands.has_key(c):
			self.commands[c] = Response() # give it an initial value

	def run(self):
		# loop until the stop signal is recieved
		while not self._stop.isSet():
			if len(self.commands) > 0:
				for command in self.commands:
					pass
			else:
				time.sleep(1)


class Async():
	""" class representing an OBD-II connection """

	def __init__(self, portstr=None):
		self.thread = OBDThread(portstr)
		self.thread.start()

	def close(self):
		self.thread.stop()
		self.thread.join()

	def addCommand(self, *commands):
		for c in commands:
			self.thread.addCommand(c)
