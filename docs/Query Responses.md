The `query()` function returns `Response` objects. These objects have the following properties:

| Property | Description                                                            |
|----------|------------------------------------------------------------------------|
| value    | The decoded value from the car                                         |
| unit     | The units of the decoded value                                         |
| command  | The `OBDCommand` object that triggered this response                     |
| message  | The internal `Message` object containing the raw response from the car |
| time     | Timestamp of response (as given by [`time.time()`](https://docs.python.org/2/library/time.html#time.time)) |

The `value` property typically contains numeric values, but can also hold complex structures (depending upon the command being decoded).

If python-OBD is unable to retrieve a response from the car, an empty `Response` object will be returned. Use `is_null()` to check for empty responses.

## Units

Unit values can be found in the `Unit` class (enum).

```python
from obd.utils import Unit
```

| Name        | Value              |
|-------------|--------------------|
| NONE        | None               |
| RATIO       | "Ratio"            |
| COUNT       | "Count"            |
| PERCENT     | "%"                |
| RPM         | "RPM"              |
| VOLT        | "Volt"             |
| F           | "F"                |
| C           | "C"                |
| SEC         | "Second"           |
| MIN         | "Minute"           |
| PA          | "Pa"               |
| KPA         | "kPa"              |
| PSI         | "psi"              |
| KPH         | "kph"              |
| MPH         | "mph"              |
| DEGREES     | "Degrees"          |
| GPS         | "Grams per Second" |
| MA          | "mA"               |
| KM          | "km"               |
| LPH         | "Liters per Hour"  |
