python-OBD also contains a debug object that receives status messages and errors. Console printing is disabled by default, but can be enabled manually. A custom debug handler can also be set.

```python
import obd

obd.debug.console = True

# AND / OR

def log(msg):
	print msg

obd.debug.handler = log
```

---

<br>
