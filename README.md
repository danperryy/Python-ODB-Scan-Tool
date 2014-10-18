python-OBD
========

##### A python module for handling realtime sensor data from OBD-II vehicle ports

This library is forked from:

+ https://github.com/peterh/pyobd
+ https://github.com/Pbartek/pyobd-pi


### Dependencies

+ pySerial
+ OBD-II addapter (ELM327 Bluetooth Adapter or ELM327 USB Cable)


### Usage

After installing the library, simply import pyobd, and create a new OBD connection object. By default, python-OBD will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor. You can also use the scanSerial helper retrieve a list of connected ports

	import obd

	connection = obd.OBD() # create connection object

	# OR

	connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

	# OR

	ports = obd.scanSerial() # return list of valid USB or RF ports
	print ports
	connection = obd.OBD(ports[0]) # connect to the first port in the list


Once a connection is made, python-OBD will load a list of the available sensors in your car. A "Sensor" in python-OBD is an object containing its name, units, and retrieval functions. To get the value of a sensor, call the valueOf() function with a sensor object as an argument.

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


Here are a few of the currently supported commands (for a full list, see commands.py):

+ Calculated Engine Load
+ Engine Coolant Temperature
+ Fuel Pressure
+ Intake Manifold Pressure
+ Engine RPM
+ Vehicle Speed
+ Timing Advance
+ Intake Air Temp
+ Air Flow Rate (MAF)
+ Throttle Position
+ Engine Run Time
+ Distance Traveled with MIL on
+ Fuel Rail Pressure (relative to vacuum)
+ Fuel Rail Pressure (direct inject)
+ Fuel Level Input
+ Number of warm-ups since codes cleared
+ Distance traveled since codes cleared
+ Evaporative system vapor pressure
+ Baromtric Pressure
+ Control module voltage
+ Relative throttle position
+ Ambient air temperature
+ Commanded throttle actuator
+ Time run with MIL on
+ Time since trouble codes cleared
+ Fuel Type
+ Ethanol Fuel Percent
+ Fuel rail pressure (absolute)
+ Relative accelerator pedal position
+ Hybrid battery pack remaining life
+ Engine oil temperature
+ Fuel injection timing
+ Engine fuel rate


Enjoy and drive safe!
