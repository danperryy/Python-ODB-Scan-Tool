#!/usr/bin/env python

import time

from obd_port import State
from obd_port import OBDPort
from obd_sensors import sensors
from obd_utils import scanSerial



class OBD():
	""" class representing an OBD-II connection with it's assorted sensors """

	def __init__(self, portstr=None):
		self.port = None
		self.sensors = []

		# initialize by connecting and loading sensors
		if self.connect(portstr):
			self.load_sensors()


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


	def load_sensors(self):
		""" queries for available sensors, and compiles lists of indices and sensor objects """

		self.sensors = []

		# Find supported sensors - by getting PIDs from OBD (sensor zero)
		# its a string of binary 01010101010101 
		# 1 means the sensor is supported
		supported = self.valueOf(sensors.PIDS)

		count = min(len(supported), len(sensors.by_PID))

		# loop through PIDs binary
		for i in range(count):
			if supported[i] == "1":
				sensor = sensors.by_PID[i]
				sensor.supported = True
				self.supportedSensors.append(sensor)


	def printSensors(self):
		for sensor in self.sensors:
			print str(sensor)

	def hasSensor(sensor):
		return sensor.supported

	def valueOf(sensor):
		if self.hasSensor(sensor):
			return self.port.get_sensor_value(sensor)
		else:
			return "Unsupported Sensor"



if __name__ == "__main__":

	o = OBD()
	#o.connect()
	time.sleep(3)
	if not o.is_connected():
		print "Not connected"
	else:
		print "Connected to " + o.get_port_name()
		#o.load_sensors()
		o.printSensors()
