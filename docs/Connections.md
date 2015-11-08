
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

### query(command, force=False)

Sends an `OBDCommand` to the car, and returns a `OBDResponse` object. This function will block until a response is recieved from the car. This function will also check whether the given command is supported by your car. If a command is not marked as supported, it will not be sent to the car, and an empty `Response` will be returned. To force an unsupported command to be sent, there is an optional `force` parameter for your convenience.

*For non-blocking querying, see [Async Querying](Async Connections.md)*

```python
import obd
connection = obd.OBD()

r = connection.query(obd.commands.RPM) # returns the response from the car
```

---

### status()

Returns a string value reflecting the status of the connection. These values should be compared against the `OBDStatus` class. The fact that they are strings is for human readability only. There are currently 3 possible states:

```python
from obd import OBDStatus

# no connection is made
OBDStatus.NOT_CONNECTED # "Not Connected"

# successful communication with the ELM327 adapter
OBDStatus.ELM_CONNECTED # "ELM Connected"

# successful communication with the vehicle
OBDStatus.CAR_CONNECTED # "Car Connected"
```

The middle state, `ELM_CONNECTED` is mostly for diagnosing errors. When a proper connection is established, you will never encounter this value.

---

### is_connected()

Returns a boolean for whether a connection was established with the vehicle. It is identical to writing:

```python
connection.status() == OBDStatus.CAR_CONNECTED
```

---

### port_name()

Returns the string name for the currently connected port (`"/dev/ttyUSB0"`). If no connection was made, this function returns `"Not connected to any port"`.

---

### get_port_name()

**Deprecated:** use `port_name()` instead

---

### supports(command)

Returns a boolean for whether a command is supported by both the car and python-OBD

---

### protocol_id()
### protocol_name()

Both functions return string names for the protocol currently being used by the adapter. Protocol *ID's* are the short names used by your adapter, whereas protocol *names* are the human-readable versions. The `protocol_id()` function is a good way to lookup which value to pass in the `protocol` field of the OBD constructor (though, this is mainly for advanced usage). These function do not make any serial requests. When no connection has been made, these functions will return empty strings. The possible values are:

|ID | Name                     |
|---|--------------------------|
| 1 | SAE J1850 PWM            |
| 2 | SAE J1850 VPW            |
| 3 | AUTO, ISO 9141-2         |
| 4 | ISO 14230-4 (KWP 5BAUD)  |
| 5 | ISO 14230-4 (KWP FAST)   |
| 6 | ISO 15765-4 (CAN 11/500) |
| 7 | ISO 15765-4 (CAN 29/500) |
| 8 | ISO 15765-4 (CAN 11/250) |
| 9 | ISO 15765-4 (CAN 29/250) |
| A | SAE J1939 (CAN 29/250)   |

---

<!--

### ecus()

Returns a list of identified "Engine Control Units" visible to the adapter. Each value in the list is a constant representing that ECU's function. These constants are found in the `ECU` class:

```python
from obd import ECU

ECU.UNKNOWN
ECU.ENGINE
```

Python-OBD can currently only detect the engine computer, but future versions may extend this capability.

-->

### close()

Closes the connection.

---

### supported_commands

Property containing a list of commands that are supported by the car.

---

<br>
