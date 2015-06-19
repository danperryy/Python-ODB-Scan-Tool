Since the standard `query()` function is blocking, it can be a hazard for UI event loops. To deal with this, python-OBD has an `Async` connection object that can be used in place of the standard `OBD` object. `Async` is a subclass of `OBD`, and therefore inherits all of the standard methods. However, `Async` adds a few in order to control a threaded update loop. This loop will keep the values of your commands up to date with the vehicle. This way, when the user `query`s the car, the latest response is returned immediately.

The update loop is controlled by calling `start()` and `stop()`. To subscribe a command for updating, call `watch()` with your requested OBDCommand. Because the update loop is threaded, commands can only be `watch`ed while the loop is `stop`ed.

```python
import obd

connection = obd.Async() # same constructor as 'obd.OBD()'

connection.watch(obd.commands.RPM) # keep track of the RPM

connection.start() # start the async update loop

print connection.query(obd.commands.RPM) # non-blocking, returns immediately
```

Callbacks can also be specified in `watch()`, and will return new `Response`s when available.

```python
import obd
import time

connection = obd.Async()

# a callback that prints every new value to the console
def new_rpm(r):
    print r.value

connection.watch(obd.commands.RPM, callback=new_rpm)
connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(60)
connection.stop()
```

<br>

---

### start()

Starts the update loop.

---

### stop()

Stops the update loop.

---

### paused()

A helper function for use in a Context Manager (a `with` statement) to temporarily stop the update loop. This makes it easy to protect your `watch()` and `unwatch()` calls. If the update loop was running at the time of being paused, it will be restarted upon exitting the context block. For instance:

```python
with connection.paused() as was_running:
	# connection is stopped within this block
	# your code here
```

The code above is equivalent to:

```python
was_running = connection.running
connection.stop()

# your code here

if was_running:
	connection.start()
```

---

### watch(command, callback=None, force=False)

*Note: The async loop must be stopped or paused before this function can be called*

Subscribes a command to be continuously updated. After calling `watch()`, the `query()` function will return the latest `Response` from that command. An optional callback can also be set, and will be fired upon receipt of new values. Multiple callbacks for the same command are welcome. An optional `force` parameter will force an unsupported command to be sent.

---

### unwatch(command, callback=None)

*Note: The async loop must be stopped or paused before this function can be called*

Unsubscribes a command from being updated. If no callback is specified, all callbacks for that command are dropped. If a callback is given, only that callback is unsubscribed (all others remain live).

---

### unwatch_all()

*Note: The async loop must be stopped or paused before this function can be called*

Unsubscribes all commands and callbacks.

---

<br>
