pyOBD-IO
========

##### A python module for handling realtime sensor data from OBD-II vehicle ports

This library is forked from:

+ https://github.com/peterh/pyobd
+ https://github.com/Pbartek/pyobd-pi


### Dependencies

+ pySerial
+ OBD-II addapter (ELM327 Bluetooth Adapter or ELM327 USB Cable)


### Usage

After installing the library, simply import pyobd, and create a new OBD connection object. By default, pyOBD-IO will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor. You can also use the scanSerial helper retrieve a list of connected ports

	import obd

	connection = obd.OBD() # create connection object

	# OR

	connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

	# OR

	ports = obd.scanSerial() # return list of valid USB or RF ports
	print ports
	connection = obd.OBD(ports[0]) # connect to the first port in the list


Once a connection is made, pyOBD-IO will load a list of the available sensors in your car. A "Sensor" in pyOBD-IO is an object containing its name, units, and retrieval functions. To get the value of a sensor, call the valueOf() function with a sensor object as an argument.

	import obd

	connection = obd.OBD()
	
	for sensor in connection.supportedSensors:
		print str(sensor)                 # prints the sensor name
		print connection.valueOf(sensor)  # gets and prints the sensor's value
		print sensor.unit                 # prints the sensors units


Sensors can also be explicitly targetted for values. The hasSensor() function will determine whether or not your car has the requested sensor.

	import obd

	connection = obd.OBD()

	if connection.hasSensor(obd.sensors.RPM):       # check for existance of sensor
		print connection.valueOf(obd.sensors.RPM)   # get value of sensor


Here are the currently supported sensors with pyOBD-IO:

+ S-S DTC Cleared
+ Calculated Engine Load
+ Engine Coolant Temperature
+ Short Term Fuel Trim - Bank 1
+ Long Term Fuel Trim - Bank 1
+ Short Term Fuel Trim - Bank 2
+ Long Term Fuel Trim - Bank 2
+ Fuel Pressure
+ Intake Manifold Pressure
+ Engine RPM
+ Vehicle Speed
+ Timing Advance
+ Intake Air Temp
+ Air Flow Rate (MAF)
+ Throttle Position
+ O2: Bank 1 - Sensor 1
+ O2: Bank 1 - Sensor 2
+ O2: Bank 1 - Sensor 3
+ O2: Bank 1 - Sensor 4
+ O2: Bank 2 - Sensor 1
+ O2: Bank 2 - Sensor 2
+ O2: Bank 2 - Sensor 3
+ O2: Bank 2 - Sensor 4
+ Engine Run Time


Enjoy and drive safe!
