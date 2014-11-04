python-OBD
==========

A python module for handling realtime sensor data from OBD-II vehicle ports

This library is forked from:

+ https://github.com/peterh/pyobd
+ https://github.com/Pbartek/pyobd-pi


Dependencies
------------

+ pySerial
+ OBD-II adapter (ELM327 Bluetooth Adapter or ELM327 USB Cable)


Usage
-----

After installing the library, simply import 'obd', and create a new OBD connection object. By default, python-OBD will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor. You can also use the scanSerial helper retrieve a list of connected ports::

    import obd

    connection = obd.OBD() # create connection object

    # OR

    connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

    # OR

    ports = obd.scanSerial() # return list of valid USB or RF ports
    print ports
    connection = obd.OBD(ports[0]) # connect to the first port in the list


Once a connection is made, python-OBD will load a list of the available commands in your car. A "Command" in python-OBD is an object used to query specific information from the vehicle. A command object contains its name, units, codes, and decoding functions. To get the value of a sensor, call the query() function with that sensor's command as an argument::

    import obd

    connection = obd.OBD()
    
    for command in connection.supportedCommands:
        print str(command)                      # prints the command name
        response = connection.query(command)    # sends the command, and returns the decoded response
        print response.value, response.unit     # prints the data and units returned from the car


Commands can also be accessed explicitly, either by name, or by code value. The has_command() function will determine whether or not your car supports the requested command::

    import obd

    connection = obd.OBD()


    c = obd.commands.RPM

    # OR

    c = obd.commands['RPM']

    # OR

    c = obd.commands[1][12] # mode 1, PID 12 (decimal)


    if connection.has_command(c):        # check for existance of sensor
        print connection.query(c).value  # get and print value of sensor


Here are a few of the currently supported commands (for a full list, see commands.py):

(note: support for these commands will vary from car to car)

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
+ Barometric Pressure
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


Debug
-----

python-OBD also contains a debug object that can be used to print status messages and errors. Console printing is disabled by default, but can be enabled manually. A custom debug handler can also be set::

    import obd

    obd.debug.console = True

    # AND / OR

    def log(msg):
        print msg

    obd.debug.handler = log

Enjoy and drive safe!
