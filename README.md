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

After installing the library, simply import pyobd, and create a new OBD connection object:

	import obd
	connection = obd.OBD() # create connection object

By default, pyOBD-IO will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor.

	import obd
	connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

You can also use the scanSerial helper retrieve a list of connected ports

	import obd

	ports = obd.scanSerial()
	print ports
	connection = obd.OBD(ports[0]) # connect to the first port in the list

Once a connection is made, pyOBD-IO will load a list of the available sensors in your car. A "Sensor" in pyOBD-IO is an object containing its name, units, and retrival functions.




Enjoy and drive safe!
