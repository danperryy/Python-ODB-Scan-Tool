
import obd
import time
import threading


class Async():
	""" class representing an OBD-II connection with it's assorted sensors """

	def __init__(self, portstr=None):
		#self.o = obd.OBD(portstr)
		self.o = 4
		self.a = 0
		self.sensors = {}
		self.thread = threading.Thread(target=self.loop, args=(self.o,))
		self.thread.start()


	def close(self):
		self.thread.join()

	def loop(self, o):
		i = 0
		while True:
			i+=1
			self.a = i
			time.sleep(1)