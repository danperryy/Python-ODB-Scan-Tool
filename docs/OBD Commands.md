An `OBDCommand` in python-OBD is an object used to query information from the vehicle. They contain all of the information neccessary to perform the query, and decode the cars response. Python-OBD has built in tables for the most common commands. They can be looked up by name, or by mode/PID (for a full list, see [Command Tables](https://github.com/brendanwhitfield/python-OBD/wiki/Command-Tables)).

```python
import obd

c = obd.commands.RPM

# OR

c = obd.commands['RPM']

# OR

c = obd.commands[1][12] # mode 1, PID 12 (RPM)
```

## Methods

##### Commands.has_command(command):

Checks the internal command tables for the existance of the given `OBDCommand` object. Commands are compared by mode and PID value.

- - -

##### Commands.has_name(name):

Checks the internal command tables for a command with the given name. This is also the function of the `in` operator.

```python
import obd

obd.commands.has_name('RPM') # True

# OR

'RPM' in obd.commands # True
```

- - -

##### Commands.has_pid(mode, pid):

Checks the internal command tables for a command with the given mode and PID.

```python
import obd
obd.commands.has_pid(1, 12) # True
```
