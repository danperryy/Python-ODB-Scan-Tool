
## has_command(command)

Checks the internal command tables for the existance of the given `OBDCommand` object. Commands are compared by mode and PID value.

```python
import obd
obd.commands.has_command(obd.commands.RPM) # True
```

---

## has_name(name)

Checks the internal command tables for a command with the given name. This is also the function of the `in` operator.

```python
import obd

obd.commands.has_name('RPM') # True

# OR

'RPM' in obd.commands # True
```

---

## has_pid(mode, pid)

Checks the internal command tables for a command with the given mode and PID.

```python
import obd
obd.commands.has_pid(1, 12) # True
```

---

<br>
