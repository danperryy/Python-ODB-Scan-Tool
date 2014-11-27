python-OBD
==========

A python module for handling realtime sensor data from OBD-II vehicle ports. Works with ELM327 OBD-II adapters, and is fit for the Raspberry Pi.


Installation
------------

::

    $ pip install obd


Basic Usage
-----------

::

    import obd

    connection = obd.OBD() # auto-connects to USB or RF port

    cmd = obd.commands.RPM # select an OBD command (sensor)

    response = connection.query(cmd) # send the command, and parse the response

    print(response.value)
    print(response.unit)


Documentation
-------------
`Visit the GitHub Wiki! <http://github.com/brendanwhitfield/python-OBD/wiki>`_


Commands
--------
Here are a few of the currently supported commands (note: support for these commands will vary from car to car):

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
+ Fuel Level Input
+ Number of warm-ups since codes cleared
+ Barometric Pressure
+ Ambient air temperature
+ Commanded throttle actuator
+ Time run with MIL on
+ Time since trouble codes cleared
+ Hybrid battery pack remaining life
+ Engine fuel rate
+ etc... (for a full list, see `commands.py <http://github.com/brendanwhitfield/python-OBD/blob/master/obd/commands.py#L106>`_)

License
-------
GNU GPL v2

This library is forked from:

+ https://github.com/peterh/pyobd
+ https://github.com/Pbartek/pyobd-pi

Enjoy and drive safe!
