If the command you need is not in python-OBDs tables, you can create a new `OBDCommand` object. The constructor accepts the following arguments (each will become a property).

| Argument             | Type     | Description                                                              |
|----------------------|----------|--------------------------------------------------------------------------|
| name                 | string   | (human readability only)                                                 |
| desc                 | string   | (human readability only)                                                 |
| mode                 | string   | OBD mode (hex)                                                           |
| pid                  | string   | OBD PID (hex)                                                            |
| bytes                | int      | Number of bytes expected in response                                     |
| decoder              | callable | Function used for decoding the hex response                              |
| supported (optional) | bool     | Flag to prevent the sending of unsupported commands (`False` by default) |

*When the command is sent, the `mode` and `pid` properties are simply concatenated. For unusual codes that don't follow the `mode + pid` structure, feel free to use just one, while setting the other to an empty string.*

The `decoder` argument is a function of following form.

```python
	def <name>(_hex):
		...
		return (<value>, <unit>)
```

The `_hex` argument is the data recieved from the car, and is guaranteed to be the size of the `bytes` property specified in the OBDCommand.

For example:

```python
from obd import OBDCommand
from obd.utils import unhex

def rpm(_hex):
	v = unhex(_hex) # helper function to convert hex to int
	v = v / 4.0
	return (v, obd.Unit.RPM)

c = OBDCommand("RPM", "Engine RPM", "01", "0C", 2, rpm)
```
