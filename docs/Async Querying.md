Since the standard `query()` function is blocking, it can be a hazard for UI event loops. To deal with this, python-OBD has an `Async` connection object that can be used in place of the standard `OBD` object.

`Async` is a subclass of `OBD`, and therefore inherits all of the standard methods. However, `Async` adds a few, in order to manage a list of commands and responses. This way, when the user `query`s the car, the latest response is returned immediately.

```python
import obd

connection = obd.Async() # same constructor as 'obd.OBD()'

connection.watch(obd.commands.RPM) # keep track of the RPM

connection.start() # start the async update loop

print connection.query(obd.commands.RPM) # non-blocking, returns immediately
```

Callbacks can also be specified, and will return new `Response`s when available.

```python
import obd
import time

connection = obd.Async() # same constructor as 'obd.OBD()'

# a callback that prints every new value to the console
def new_rpm(r):
    print r.value

connection.watch(obd.commands.RPM, callback=new_rpm)
connection.start()

# the callback will now be fired upon receipt of new values

time.sleep(60)
connection.stop()
```


## Methods

##### Async.start()

Starts the update loop.

- - -

##### Async.stop()

Stops the update loop.

- - -

##### Async.watch(command, callback=None, force=False)

*Note: The async loop must be stopped before this function can be called*

Subscribes a command to be continuously updated. After calling `watch()`, the `query()` function will return the latest `Response` from that command. An optional callback can also be set, and will be fired upon receipt of new values. Multiple callbacks for the same command are welcome. An optional `force` parameter will force an unsupported command to be sent.

- - -

##### Async.unwatch(command, callback=None)

*Note: The async loop must be stopped before this function can be called*

Unsubscribes a command from being updated. If no callback is specified, all callbacks for that command are dropped. If a callback is given, only that callback is unsubscribed (all others remain live).

- - -

##### Async.unwatch_all()

*Note: The async loop must be stopped before this function can be called*

Unsubscribes all commands and callbacks.
