# Welcome

Python-OBD is a library for handling data from a car's [**O**n-**B**oard **D**iagnostics port](https://en.wikipedia.org/wiki/On-board_diagnostics) (OBD-II). It can stream real time sensor data, perform diagnostics (such as reading check-engine codes), and is fit for the Raspberry Pi. This library is designed to work with standard [ELM327 OBD-II adapters](http://www.amazon.com/s/ref=nb_sb_noss?field-keywords=elm327).

<br>

# Installation

Install the latest release from pypi:

```shell
$ pip install obd
```

If you are using a bluetooth adapter, you will need to install the following packages:

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

<br>

# License

GNU General Public License V2

---

<br>
