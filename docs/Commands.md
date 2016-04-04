
# Lookup

`OBDCommand`s are objects used to query information from the vehicle. They contain all of the information neccessary to perform the query, and decode the cars response. Python-OBD has built in tables for the most common commands. They can be looked up by name, or by mode & PID.

```python
import obd

c = obd.commands.RPM

# OR

c = obd.commands['RPM']

# OR

c = obd.commands[1][12] # mode 1, PID 12 (RPM)
```

The `commands` table also has a few helper methods for determining if a particular name or PID is present.

---

### has_command(command)

Checks the internal command tables for the existance of the given `OBDCommand` object. Commands are compared by mode and PID value.

```python
import obd
obd.commands.has_command(obd.commands.RPM) # True
```

---

### has_name(name)

Checks the internal command tables for a command with the given name. This is also the function of the `in` operator.

```python
import obd

obd.commands.has_name('RPM') # True

# OR

'RPM' in obd.commands # True
```

---

### has_pid(mode, pid)

Checks the internal command tables for a command with the given mode and PID.

```python
import obd
obd.commands.has_pid(1, 12) # True
```

---

<br>

# OBD-II adapter (ELM327 commands)

|PID  | Name        | Description                             |
|-----|-------------|-----------------------------------------|
| N/A | ELM_VERSION | OBD-II adapter version string           |
| N/A | ELM_VOLTAGE | Voltage detected by OBD-II adapter      |

<br>

# Mode 01

|PID | Name                      | Description                             |
|----|---------------------------|-----------------------------------------|
| 00 | PIDS_A                    | Supported PIDs [01-20]                  |
| 01 | STATUS                    | Status since DTCs cleared               |
| 02 | *unsupported*             | *unsupported*                           |
| 03 | FUEL_STATUS               | Fuel System Status                      |
| 04 | ENGINE_LOAD               | Calculated Engine Load                  |
| 05 | COOLANT_TEMP              | Engine Coolant Temperature              |
| 06 | SHORT_FUEL_TRIM_1         | Short Term Fuel Trim - Bank 1           |
| 07 | LONG_FUEL_TRIM_1          | Long Term Fuel Trim - Bank 1            |
| 08 | SHORT_FUEL_TRIM_2         | Short Term Fuel Trim - Bank 2           |
| 09 | LONG_FUEL_TRIM_2          | Long Term Fuel Trim - Bank 2            |
| 0A | FUEL_PRESSURE             | Fuel Pressure                           |
| 0B | INTAKE_PRESSURE           | Intake Manifold Pressure                |
| 0C | RPM                       | Engine RPM                              |
| 0D | SPEED                     | Vehicle Speed                           |
| 0E | TIMING_ADVANCE            | Timing Advance                          |
| 0F | INTAKE_TEMP               | Intake Air Temp                         |
| 10 | MAF                       | Air Flow Rate (MAF)                     |
| 11 | THROTTLE_POS              | Throttle Position                       |
| 12 | AIR_STATUS                | Secondary Air Status                    |
| 13 | *unsupported*             | *unsupported*                           |
| 14 | O2_B1S1                   | O2: Bank 1 - Sensor 1 Voltage           |
| 15 | O2_B1S2                   | O2: Bank 1 - Sensor 2 Voltage           |
| 16 | O2_B1S3                   | O2: Bank 1 - Sensor 3 Voltage           |
| 17 | O2_B1S4                   | O2: Bank 1 - Sensor 4 Voltage           |
| 18 | O2_B2S1                   | O2: Bank 2 - Sensor 1 Voltage           |
| 19 | O2_B2S2                   | O2: Bank 2 - Sensor 2 Voltage           |
| 1A | O2_B2S3                   | O2: Bank 2 - Sensor 3 Voltage           |
| 1B | O2_B2S4                   | O2: Bank 2 - Sensor 4 Voltage           |
| 1C | OBD_COMPLIANCE            | OBD Standards Compliance                |
| 1D | *unsupported*             | *unsupported*                           |
| 1E | *unsupported*             | *unsupported*                           |
| 1F | RUN_TIME                  | Engine Run Time                         |
| 20 | PIDS_B                    | Supported PIDs [21-40]                  |
| 21 | DISTANCE_W_MIL            | Distance Traveled with MIL on           |
| 22 | FUEL_RAIL_PRESSURE_VAC    | Fuel Rail Pressure (relative to vacuum) |
| 23 | FUEL_RAIL_PRESSURE_DIRECT | Fuel Rail Pressure (direct inject)      |
| 24 | O2_S1_WR_VOLTAGE          | 02 Sensor 1 WR Lambda Voltage           |
| 25 | O2_S2_WR_VOLTAGE          | 02 Sensor 2 WR Lambda Voltage           |
| 26 | O2_S3_WR_VOLTAGE          | 02 Sensor 3 WR Lambda Voltage           |
| 27 | O2_S4_WR_VOLTAGE          | 02 Sensor 4 WR Lambda Voltage           |
| 28 | O2_S5_WR_VOLTAGE          | 02 Sensor 5 WR Lambda Voltage           |
| 29 | O2_S6_WR_VOLTAGE          | 02 Sensor 6 WR Lambda Voltage           |
| 2A | O2_S7_WR_VOLTAGE          | 02 Sensor 7 WR Lambda Voltage           |
| 2B | O2_S8_WR_VOLTAGE          | 02 Sensor 8 WR Lambda Voltage           |
| 2C | COMMANDED_EGR             | Commanded EGR                           |
| 2D | EGR_ERROR                 | EGR Error                               |
| 2E | EVAPORATIVE_PURGE         | Commanded Evaporative Purge             |
| 2F | FUEL_LEVEL                | Fuel Level Input                        |
| 30 | WARMUPS_SINCE_DTC_CLEAR   | Number of warm-ups since codes cleared  |
| 31 | DISTANCE_SINCE_DTC_CLEAR  | Distance traveled since codes cleared   |
| 32 | EVAP_VAPOR_PRESSURE       | Evaporative system vapor pressure       |
| 33 | BAROMETRIC_PRESSURE       | Barometric Pressure                     |
| 34 | O2_S1_WR_CURRENT          | 02 Sensor 1 WR Lambda Current           |
| 35 | O2_S2_WR_CURRENT          | 02 Sensor 2 WR Lambda Current           |
| 36 | O2_S3_WR_CURRENT          | 02 Sensor 3 WR Lambda Current           |
| 37 | O2_S4_WR_CURRENT          | 02 Sensor 4 WR Lambda Current           |
| 38 | O2_S5_WR_CURRENT          | 02 Sensor 5 WR Lambda Current           |
| 39 | O2_S6_WR_CURRENT          | 02 Sensor 6 WR Lambda Current           |
| 3A | O2_S7_WR_CURRENT          | 02 Sensor 7 WR Lambda Current           |
| 3B | O2_S8_WR_CURRENT          | 02 Sensor 8 WR Lambda Current           |
| 3C | CATALYST_TEMP_B1S1        | Catalyst Temperature: Bank 1 - Sensor 1 |
| 3D | CATALYST_TEMP_B2S1        | Catalyst Temperature: Bank 2 - Sensor 1 |
| 3E | CATALYST_TEMP_B1S2        | Catalyst Temperature: Bank 1 - Sensor 2 |
| 3F | CATALYST_TEMP_B2S2        | Catalyst Temperature: Bank 2 - Sensor 2 |
| 40 | PIDS_C                    | Supported PIDs [41-60]                  |
| 41 | *unsupported*             | *unsupported*                           |
| 42 | *unsupported*             | *unsupported*                           |
| 43 | *unsupported*             | *unsupported*                           |
| 44 | *unsupported*             | *unsupported*                           |
| 45 | RELATIVE_THROTTLE_POS     | Relative throttle position              |
| 46 | AMBIANT_AIR_TEMP          | Ambient air temperature                 |
| 47 | THROTTLE_POS_B            | Absolute throttle position B            |
| 48 | THROTTLE_POS_C            | Absolute throttle position C            |
| 49 | ACCELERATOR_POS_D         | Accelerator pedal position D            |
| 4A | ACCELERATOR_POS_E         | Accelerator pedal position E            |
| 4B | ACCELERATOR_POS_F         | Accelerator pedal position F            |
| 4C | THROTTLE_ACTUATOR         | Commanded throttle actuator             |
| 4D | RUN_TIME_MIL              | Time run with MIL on                    |
| 4E | TIME_SINCE_DTC_CLEARED    | Time since trouble codes cleared        |
| 4F | *unsupported*             | *unsupported*                           |
| 50 | MAX_MAF                   | Maximum value for mass air flow sensor  |
| 51 | FUEL_TYPE                 | Fuel Type                               |
| 52 | ETHANOL_PERCENT           | Ethanol Fuel Percent                    |
| 53 | EVAP_VAPOR_PRESSURE_ABS   | Absolute Evap system Vapor Pressure     |
| 54 | EVAP_VAPOR_PRESSURE_ALT   | Evap system vapor pressure              |
| 55 | SHORT_O2_TRIM_B1          | Short term secondary O2 trim - Bank 1   |
| 56 | LONG_O2_TRIM_B1           | Long term secondary O2 trim - Bank 1    |
| 57 | SHORT_O2_TRIM_B2          | Short term secondary O2 trim - Bank 2   |
| 58 | LONG_O2_TRIM_B2           | Long term secondary O2 trim - Bank 2    |
| 59 | FUEL_RAIL_PRESSURE_ABS    | Fuel rail pressure (absolute)           |
| 5A | RELATIVE_ACCEL_POS        | Relative accelerator pedal position     |
| 5B | HYBRID_BATTERY_REMAINING  | Hybrid battery pack remaining life      |
| 5C | OIL_TEMP                  | Engine oil temperature                  |
| 5D | FUEL_INJECT_TIMING        | Fuel injection timing                   |
| 5E | FUEL_RATE                 | Engine fuel rate                        |
| 5F | *unsupported*             | *unsupported*                           |

<br>

# Mode 02

Mode 02 commands are the same as mode 01, but are metrics from when the last DTC occurred (the freeze frame). To access them by name, simple prepend `DTC_` to the Mode 01 command name.

```python
import obd

obd.commands.RPM # the Mode 01 command
# vs.
obd.commands.DTC_RPM # the Mode 02 command
```

<br>

# Mode 03

Mode 03 contains a single command `GET_DTC` which requests all diagnostic trouble codes from the vehicle's engine.

|PID  | Name    | Description                             |
|-----|---------|-----------------------------------------|
| N/A | GET_DTC | Get Diagnostic Trouble Codes            |

This command requests all diagnostic trouble codes from the vehicle's engine. The `value` field of the response object will contain a list of tuples, where each tuple contains the DTC, and a string description of that DTC (if available).

```python
import obd
connection = obd.OBD()
r = connection.query(obd.commands.GET_DTC)
print(r.value)

'''
example output:
[
  ("P0030", "HO2S Heater Control Circuit"),
  ("P1367", "Unknown error code")
]
'''
```

<br>

# Mode 04

|PID  | Name      | Description                             |
|-----|-----------|-----------------------------------------|
| N/A | CLEAR_DTC | Clear DTCs and Freeze data              |

<br>

# Mode 07

The return value will be encoded in the same structure as the Mode 03 `GET_DTC` command.

|PID  | Name           | Description                  |
|-----|----------------|------------------------------|
| N/A | GET_FREEZE_DTC | Get Freeze DTCs              |

<br>
