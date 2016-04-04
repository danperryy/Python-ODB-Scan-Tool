# Welcome

Python-OBD is a library for handling data from a car's [**O**n-**B**oard **D**iagnostics port](https://en.wikipedia.org/wiki/On-board_diagnostics) (OBD-II). It can stream real time sensor data, perform diagnostics (such as reading check-engine codes), and is fit for the Raspberry Pi. This library is designed to work with standard [ELM327 OBD-II adapters](http://www.amazon.com/s/ref=nb_sb_noss?field-keywords=elm327).

<br>

# Installation

Install the latest release from pypi:

```shell
$ pip install obd
```

*Note: If you are using a Bluetooth adapter on Linux, you may also need to install and configure your Bluetooth stack. On Debian-based systems, this usually means installing the following packages:*

```shell
$ sudo apt-get install bluetooth bluez-utils blueman
```

<br>

# Basic Usage

```python
import obd

connection = obd.OBD() # auto-connects to USB or RF port

cmd = obd.commands.RPM # select an OBD command (sensor)

response = connection.query(cmd) # send the command, and parse the response

print(response.value)
print(response.unit)
```

OBD connections operate in a request-reply fashion. To retrieve data from the car, you must send commands that query for the data you want (e.g. RPM, Vehicle speed, etc). In python-OBD, this is done with the `query()` function. The commands themselves are represented as objects, and can be looked up by name or value in `obd.commands`. The `query()` function will return a response object with parsed data in its `value` and `unit` properties.

<br>

# License

GNU General Public License V2

---

<br>
