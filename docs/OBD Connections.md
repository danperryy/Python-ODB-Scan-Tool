After installing the library, simply `import obd`, and create a new OBD connection object. By default, python-OBD will scan for Bluetooth and USB serial ports (in that order), and will pick the first connection it finds. The port can also be specified manually by passing a connection string to the OBD constructor. You can also use the scanSerial helper retrieve a list of connected ports.

```python
import obd

connection = obd.OBD() # auto connect

# OR

connection = obd.OBD("/dev/ttyUSB0") # create connection with USB 0

# OR

ports = obd.scanSerial()       # return list of valid USB or RF ports
print ports                    # ['/dev/ttyUSB0', '/dev/ttyUSB1']
connection = obd.OBD(ports[0]) # connect to the first port in the list
```

<br>

---

## query(command, force=False)

Sends an `OBDCommand` to the car, and returns a `OBDResponse` object. This function will block until a response is recieved from the car. This function will also check whether the given command is supported by your car. If a command is not marked as supported, it will not be sent to the car, and an empty `Response` will be returned. To force an unsupported command to be sent, there is an optional `force` parameter for your convenience.

*For non-blocking querying, see [Async Querying](https://github.com/brendanwhitfield/python-OBD/wiki/Async-Querying)*

```python
import obd
connection = obd.OBD()

r = connection.query(obd.commands.RPM) # returns the response from the car
```

---

## is_connected()

Returns a boolean for whether a connection was established.

---

## get_port_name()

Returns the string name for the currently connected port (`"/dev/ttyUSB0"`). If no connection was made, this function returns `"Not connected to any port"`.

---

## supports(command)

Returns a boolean for whether a command is supported by both the car and python-OBD

---

## close()

Closes the connection.

---

## supported_commands

Property containing a list of commands that are supported by the car.

---

<br>
