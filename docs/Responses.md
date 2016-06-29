The `query()` function returns `OBDResponse` objects. These objects have the following properties:

| Property | Description                                                            |
|----------|------------------------------------------------------------------------|
| value    | The decoded value from the car                                         |
| command  | The `OBDCommand` object that triggered this response                   |
| message  | The internal `Message` object containing the raw response from the car |
| time     | Timestamp of response (as given by [`time.time()`](https://docs.python.org/2/library/time.html#time.time)) |



---

### is_null()

Use this function to check if a response is empty. Python-OBD will emit empty responses when it is unable to retrieve data from the car.

```python
r = connection.query(obd.commands.RPM)

if not r.is_null():
	print(r.value)
```

---


# Values

The `value` property typically contains a [Pint](http://pint.readthedocs.io/en/latest/) `Quantity` object, but can also hold complex structures (depending on the request). Pint quantities combine a value and unit into a single class, and are used to represent physical values (such as "4 seconds", and "88 mph"). This allows for consistency when doing math and unit conversions. Pint maintains a registry of units, which is exposed in python-OBD as `obd.Unit`.

Below are common operations that can be done with Pint units and quantities. For more information, check out the [Pint Documentation](http://pint.readthedocs.io/en/latest/).

```python
import obd

>>> response.value
<Quantity(100, 'kph')>

# get the raw python datatype
>>> response.value.magnitude
100

# converts quantities to strings
>>> str(response.value)
'100 kph'

# convert strings to quantities
>>> obd.Unit("100 kph")
<Quantity(100, 'kph')>

# handles conversions nicely
>>> response.value.to('mph')
<Quantity(62.13711922373341, 'mph')>

# scaler math
>>> response.value / 2
<Quantity(50.0, 'kph')>

# non-scaler math requires you to specify units yourself
>>> response.value + (20 * obd.Unit.kph)
<Quantity(120, 'kph')>

# non-scaler math with different units
# handles unit conversions transparently
>>> response.value + (20 * obd.Unit.mph)
<Quantity(132.18688, 'kph')>
```

---

<br>
