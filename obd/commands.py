
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
#                                                                      #
########################################################################
#                                                                      #
# commands.py                                                          #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

from .protocols import ECU
from .OBDCommand import OBDCommand
from .decoders import *
from .debug import debug




'''
Define command tables
'''

# NOTE: the NAME field will be used as the dict key for that sensor
# NOTE: commands MUST be in PID order, one command per PID (for fast lookup using __mode1__[pid])

# see OBDCommand.py for descriptions & purposes for each of these fields

__mode1__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_A"                     , "Supported PIDs [01-20]"                  , "0100", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS"                     , "Status since DTCs cleared"               , "0101", 4, status,                ECU.ENGINE, True),
    OBDCommand("FREEZE_DTC"                 , "Freeze DTC"                              , "0102", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("FUEL_STATUS"                , "Fuel System Status"                      , "0103", 2, fuel_status,           ECU.ENGINE, True),
    OBDCommand("ENGINE_LOAD"                , "Calculated Engine Load"                  , "0104", 1, percent,               ECU.ENGINE, True),
    OBDCommand("COOLANT_TEMP"               , "Engine Coolant Temperature"              , "0105", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_1"          , "Short Term Fuel Trim - Bank 1"           , "0106", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_1"           , "Long Term Fuel Trim - Bank 1"            , "0107", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_2"          , "Short Term Fuel Trim - Bank 2"           , "0108", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_2"           , "Long Term Fuel Trim - Bank 2"            , "0109", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_PRESSURE"              , "Fuel Pressure"                           , "010A", 1, fuel_pressure,         ECU.ENGINE, True),
    OBDCommand("INTAKE_PRESSURE"            , "Intake Manifold Pressure"                , "010B", 1, pressure,              ECU.ENGINE, True),
    OBDCommand("RPM"                        , "Engine RPM"                              , "010C", 2, rpm,                   ECU.ENGINE, True),
    OBDCommand("SPEED"                      , "Vehicle Speed"                           , "010D", 1, speed,                 ECU.ENGINE, True),
    OBDCommand("TIMING_ADVANCE"             , "Timing Advance"                          , "010E", 1, timing_advance,        ECU.ENGINE, True),
    OBDCommand("INTAKE_TEMP"                , "Intake Air Temp"                         , "010F", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("MAF"                        , "Air Flow Rate (MAF)"                     , "0110", 2, maf,                   ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS"               , "Throttle Position"                       , "0111", 1, percent,               ECU.ENGINE, True),
    OBDCommand("AIR_STATUS"                 , "Secondary Air Status"                    , "0112", 1, air_status,            ECU.ENGINE, True),
    OBDCommand("O2_SENSORS"                 , "O2 Sensors Present"                      , "0113", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("O2_B1S1"                    , "O2: Bank 1 - Sensor 1 Voltage"           , "0114", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S2"                    , "O2: Bank 1 - Sensor 2 Voltage"           , "0115", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S3"                    , "O2: Bank 1 - Sensor 3 Voltage"           , "0116", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S4"                    , "O2: Bank 1 - Sensor 4 Voltage"           , "0117", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S1"                    , "O2: Bank 2 - Sensor 1 Voltage"           , "0118", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S2"                    , "O2: Bank 2 - Sensor 2 Voltage"           , "0119", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S3"                    , "O2: Bank 2 - Sensor 3 Voltage"           , "011A", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S4"                    , "O2: Bank 2 - Sensor 4 Voltage"           , "011B", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("OBD_COMPLIANCE"             , "OBD Standards Compliance"                , "011C", 1, obd_compliance,        ECU.ENGINE, True),
    OBDCommand("O2_SENSORS_ALT"             , "O2 Sensors Present (alternate)"          , "011D", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("AUX_INPUT_STATUS"           , "Auxiliary input status"                  , "011E", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("RUN_TIME"                   , "Engine Run Time"                         , "011F", 2, seconds,               ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_B"                     , "Supported PIDs [21-40]"                  , "0120", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("DISTANCE_W_MIL"             , "Distance Traveled with MIL on"           , "0121", 2, distance,              ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_VAC"     , "Fuel Rail Pressure (relative to vacuum)" , "0122", 2, fuel_pres_vac,         ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_DIRECT"  , "Fuel Rail Pressure (direct inject)"      , "0123", 2, fuel_pres_direct,      ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_VOLTAGE"           , "02 Sensor 1 WR Lambda Voltage"           , "0124", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_VOLTAGE"           , "02 Sensor 2 WR Lambda Voltage"           , "0125", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_VOLTAGE"           , "02 Sensor 3 WR Lambda Voltage"           , "0126", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_VOLTAGE"           , "02 Sensor 4 WR Lambda Voltage"           , "0127", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_VOLTAGE"           , "02 Sensor 5 WR Lambda Voltage"           , "0128", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_VOLTAGE"           , "02 Sensor 6 WR Lambda Voltage"           , "0129", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_VOLTAGE"           , "02 Sensor 7 WR Lambda Voltage"           , "012A", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_VOLTAGE"           , "02 Sensor 8 WR Lambda Voltage"           , "012B", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("COMMANDED_EGR"              , "Commanded EGR"                           , "012C", 1, percent,               ECU.ENGINE, True),
    OBDCommand("EGR_ERROR"                  , "EGR Error"                               , "012D", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("EVAPORATIVE_PURGE"          , "Commanded Evaporative Purge"             , "012E", 1, percent,               ECU.ENGINE, True),
    OBDCommand("FUEL_LEVEL"                 , "Fuel Level Input"                        , "012F", 1, percent,               ECU.ENGINE, True),
    OBDCommand("WARMUPS_SINCE_DTC_CLEAR"    , "Number of warm-ups since codes cleared"  , "0130", 1, count,                 ECU.ENGINE, True),
    OBDCommand("DISTANCE_SINCE_DTC_CLEAR"   , "Distance traveled since codes cleared"   , "0131", 2, distance,              ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE"        , "Evaporative system vapor pressure"       , "0132", 2, evap_pressure,         ECU.ENGINE, True),
    OBDCommand("BAROMETRIC_PRESSURE"        , "Barometric Pressure"                     , "0133", 1, pressure,              ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_CURRENT"           , "02 Sensor 1 WR Lambda Current"           , "0134", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_CURRENT"           , "02 Sensor 2 WR Lambda Current"           , "0135", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_CURRENT"           , "02 Sensor 3 WR Lambda Current"           , "0136", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_CURRENT"           , "02 Sensor 4 WR Lambda Current"           , "0137", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_CURRENT"           , "02 Sensor 5 WR Lambda Current"           , "0138", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_CURRENT"           , "02 Sensor 6 WR Lambda Current"           , "0139", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_CURRENT"           , "02 Sensor 7 WR Lambda Current"           , "013A", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_CURRENT"           , "02 Sensor 8 WR Lambda Current"           , "013B", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S1"         , "Catalyst Temperature: Bank 1 - Sensor 1" , "013C", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S1"         , "Catalyst Temperature: Bank 2 - Sensor 1" , "013D", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S2"         , "Catalyst Temperature: Bank 1 - Sensor 2" , "013E", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S2"         , "Catalyst Temperature: Bank 2 - Sensor 2" , "013F", 2, catalyst_temp,         ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_C"                     , "Supported PIDs [41-60]"                  , "0140", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS_DRIVE_CYCLE"         , "Monitor status this drive cycle"         , "0141", 4, drop,                  ECU.ENGINE, True),
    OBDCommand("CONTROL_MODULE_VOLTAGE"     , "Control module voltage"                  , "0142", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("ABSOLUTE_LOAD"              , "Absolute load value"                     , "0143", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("COMMAND_EQUIV_RATIO"        , "Command equivalence ratio"               , "0144", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("RELATIVE_THROTTLE_POS"      , "Relative throttle position"              , "0145", 1, percent,               ECU.ENGINE, True),
    OBDCommand("AMBIANT_AIR_TEMP"           , "Ambient air temperature"                 , "0146", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_B"             , "Absolute throttle position B"            , "0147", 1, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_C"             , "Absolute throttle position C"            , "0148", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_D"          , "Accelerator pedal position D"            , "0149", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_E"          , "Accelerator pedal position E"            , "014A", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_F"          , "Accelerator pedal position F"            , "014B", 1, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_ACTUATOR"          , "Commanded throttle actuator"             , "014C", 1, percent,               ECU.ENGINE, True),
    OBDCommand("RUN_TIME_MIL"               , "Time run with MIL on"                    , "014D", 2, minutes,               ECU.ENGINE, True),
    OBDCommand("TIME_SINCE_DTC_CLEARED"     , "Time since trouble codes cleared"        , "014E", 2, minutes,               ECU.ENGINE, True),
    OBDCommand("MAX_VALUES"                 , "Various Max values"                      , "014F", 4, drop,                  ECU.ENGINE, True), # todo: decode this
    OBDCommand("MAX_MAF"                    , "Maximum value for mass air flow sensor"  , "0150", 4, max_maf,               ECU.ENGINE, True),
    OBDCommand("FUEL_TYPE"                  , "Fuel Type"                               , "0151", 1, fuel_type,             ECU.ENGINE, True),
    OBDCommand("ETHANOL_PERCENT"            , "Ethanol Fuel Percent"                    , "0152", 1, percent,               ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ABS"    , "Absolute Evap system Vapor Pressure"     , "0153", 2, abs_evap_pressure,     ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ALT"    , "Evap system vapor pressure"              , "0154", 2, evap_pressure_alt,     ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B1"           , "Short term secondary O2 trim - Bank 1"   , "0155", 2, percent_centered,      ECU.ENGINE, True), # todo: decode seconds value for banks 3 and 4
    OBDCommand("LONG_O2_TRIM_B1"            , "Long term secondary O2 trim - Bank 1"    , "0156", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B2"           , "Short term secondary O2 trim - Bank 2"   , "0157", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_O2_TRIM_B2"            , "Long term secondary O2 trim - Bank 2"    , "0158", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_ABS"     , "Fuel rail pressure (absolute)"           , "0159", 2, fuel_pres_direct,      ECU.ENGINE, True),
    OBDCommand("RELATIVE_ACCEL_POS"         , "Relative accelerator pedal position"     , "015A", 1, percent,               ECU.ENGINE, True),
    OBDCommand("HYBRID_BATTERY_REMAINING"   , "Hybrid battery pack remaining life"      , "015B", 1, percent,               ECU.ENGINE, True),
    OBDCommand("OIL_TEMP"                   , "Engine oil temperature"                  , "015C", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("FUEL_INJECT_TIMING"         , "Fuel injection timing"                   , "015D", 2, inject_timing,         ECU.ENGINE, True),
    OBDCommand("FUEL_RATE"                  , "Engine fuel rate"                        , "015E", 2, fuel_rate,             ECU.ENGINE, True),
    OBDCommand("EMISSION_REQ"               , "Designed emission requirements"          , "015F", 1, drop,                  ECU.ENGINE, True),
]


# mode 2 is the same as mode 1, but returns values from when the DTC occured
__mode2__ = []
for c in __mode1__:
    c = c.clone()
    c.command = "02" + c.command[2:] # change the mode: 0100 ---> 0200
    c.name = "DTC_" + c.name
    c.desc = "DTC " + c.desc
    __mode2__.append(c)


__mode3__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("GET_DTC"                    , "Get DTCs"                                , "03",   0, dtc,                   ECU.ALL,     False),
]

__mode4__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("CLEAR_DTC"                  , "Clear DTCs and Freeze data"              , "04",   0, drop,                  ECU.ALL,     False),
]

__mode7__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("GET_FREEZE_DTC"             , "Get Freeze DTCs"                         , "07",   0, dtc,                   ECU.ALL,     False),
]

__misc__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("ELM_VERSION"                , "ELM327 version string"                   , "ATI",  0, raw_string,            ECU.UNKNOWN, False),
    OBDCommand("ELM_VOLTAGE"                , "Voltage detected by OBD-II adapter"      , "ATRV", 0, elm_voltage,           ECU.UNKNOWN, False),
]



'''
Assemble the command tables by mode, and allow access by name
'''

class Commands():
    def __init__(self):

        # allow commands to be accessed by mode and PID
        self.modes = [
            [],
            __mode1__,
            __mode2__,
            __mode3__,
            __mode4__,
            [],
            [],
            __mode7__
        ]

        # allow commands to be accessed by name
        for m in self.modes:
            for c in m:
                self.__dict__[c.name] = c

        for c in __misc__:
            self.__dict__[c.name] = c


    def __getitem__(self, key):
        """
            commands can be accessed by name, or by mode/pid

            obd.commands.RPM
            obd.commands["RPM"]
            obd.commands[1][12] # mode 1, PID 12 (RPM)
        """

        if isinstance(key, int):
            return self.modes[key]
        elif isinstance(key, str) or isinstance(key, unicode):
            return self.__dict__[key]
        else:
            debug("OBD commands can only be retrieved by PID value or dict name", True)


    def __len__(self):
        """ returns the number of commands supported by python-OBD """
        l = 0
        for m in self.modes:
            l += len(m)
        return l


    def __contains__(self, s):
        """ calls has_name(s) """
        return self.has_name(s)


    def base_commands(self):
        """
            returns the list of commands that should always be
            supported by the ELM327
        """
        return [
            self.PIDS_A,
            self.GET_DTC,
            self.CLEAR_DTC,
            self.GET_FREEZE_DTC,
            self.ELM_VERSION,
            self.ELM_VOLTAGE,
        ]


    def pid_getters(self):
        """ returns a list of PID GET commands """
        getters = []
        for m in self.modes:
            for c in m:
                if c.decode == pid: # GET commands have a special decoder
                    getters.append(c)
        return getters


    def set_supported(self, mode, pid, v):
        """ sets the boolean supported flag for the given command """
        if isinstance(v, bool):
            if self.has(mode, pid):
                self.modes[mode][pid].supported = v
        else:
            debug("set_supported() only accepts boolean values", True)


    def has_command(self, c):
        """ checks for existance of a command by OBDCommand object """
        if isinstance(c, OBDCommand):
            return c in self.__dict__.values()
        else:
            debug("has_command() only accepts OBDCommand objects", True)
            return False


    def has_name(self, s):
        """ checks for existance of a command by name """
        if isinstance(s, str) or isinstance(s, unicode):
            return s.isupper() and (s in self.__dict__.keys())
        else:
            debug("has_name() only accepts string names for commands", True)
            return False


    def has_pid(self, mode, pid):
        """ checks for existance of a command by int mode and int pid """
        if isinstance(mode, int) and isinstance(pid, int):
            if (mode < 0) or (pid < 0):
                return False
            if mode >= len(self.modes):
                return False
            if pid >= len(self.modes[mode]):
                return False
            return True
        else:
            debug("has_pid() only accepts integer values for mode and PID", True)
            return False


# export this object
commands = Commands()
