
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

import logging

logger = logging.getLogger(__name__)



'''
Define command tables
'''

# NOTE: the NAME field will be used as the dict key for that sensor
# NOTE: commands MUST be in PID order, one command per PID (for fast lookup using __mode1__[pid])

# see OBDCommand.py for descriptions & purposes for each of these fields

__mode1__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_A"                     , "Supported PIDs [01-20]"                  , b"0100", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS"                     , "Status since DTCs cleared"               , b"0101", 4, status,                ECU.ENGINE, True),
    OBDCommand("FREEZE_DTC"                 , "Freeze DTC"                              , b"0102", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("FUEL_STATUS"                , "Fuel System Status"                      , b"0103", 2, fuel_status,           ECU.ENGINE, True),
    OBDCommand("ENGINE_LOAD"                , "Calculated Engine Load"                  , b"0104", 1, percent,               ECU.ENGINE, True),
    OBDCommand("COOLANT_TEMP"               , "Engine Coolant Temperature"              , b"0105", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_1"          , "Short Term Fuel Trim - Bank 1"           , b"0106", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_1"           , "Long Term Fuel Trim - Bank 1"            , b"0107", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_FUEL_TRIM_2"          , "Short Term Fuel Trim - Bank 2"           , b"0108", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_FUEL_TRIM_2"           , "Long Term Fuel Trim - Bank 2"            , b"0109", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_PRESSURE"              , "Fuel Pressure"                           , b"010A", 1, fuel_pressure,         ECU.ENGINE, True),
    OBDCommand("INTAKE_PRESSURE"            , "Intake Manifold Pressure"                , b"010B", 1, pressure,              ECU.ENGINE, True),
    OBDCommand("RPM"                        , "Engine RPM"                              , b"010C", 2, rpm,                   ECU.ENGINE, True),
    OBDCommand("SPEED"                      , "Vehicle Speed"                           , b"010D", 1, speed,                 ECU.ENGINE, True),
    OBDCommand("TIMING_ADVANCE"             , "Timing Advance"                          , b"010E", 1, timing_advance,        ECU.ENGINE, True),
    OBDCommand("INTAKE_TEMP"                , "Intake Air Temp"                         , b"010F", 1, temp,                  ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("MAF"                        , "Air Flow Rate (MAF)"                     , b"0110", 2, maf,                   ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS"               , "Throttle Position"                       , b"0111", 1, percent,               ECU.ENGINE, True),
    OBDCommand("AIR_STATUS"                 , "Secondary Air Status"                    , b"0112", 1, air_status,            ECU.ENGINE, True),
    OBDCommand("O2_SENSORS"                 , "O2 Sensors Present"                      , b"0113", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("O2_B1S1"                    , "O2: Bank 1 - Sensor 1 Voltage"           , b"0114", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S2"                    , "O2: Bank 1 - Sensor 2 Voltage"           , b"0115", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S3"                    , "O2: Bank 1 - Sensor 3 Voltage"           , b"0116", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B1S4"                    , "O2: Bank 1 - Sensor 4 Voltage"           , b"0117", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S1"                    , "O2: Bank 2 - Sensor 1 Voltage"           , b"0118", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S2"                    , "O2: Bank 2 - Sensor 2 Voltage"           , b"0119", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S3"                    , "O2: Bank 2 - Sensor 3 Voltage"           , b"011A", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("O2_B2S4"                    , "O2: Bank 2 - Sensor 4 Voltage"           , b"011B", 2, sensor_voltage,        ECU.ENGINE, True),
    OBDCommand("OBD_COMPLIANCE"             , "OBD Standards Compliance"                , b"011C", 1, obd_compliance,        ECU.ENGINE, True),
    OBDCommand("O2_SENSORS_ALT"             , "O2 Sensors Present (alternate)"          , b"011D", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("AUX_INPUT_STATUS"           , "Auxiliary input status"                  , b"011E", 1, drop,                  ECU.ENGINE, True),
    OBDCommand("RUN_TIME"                   , "Engine Run Time"                         , b"011F", 2, seconds,               ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_B"                     , "Supported PIDs [21-40]"                  , b"0120", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("DISTANCE_W_MIL"             , "Distance Traveled with MIL on"           , b"0121", 2, distance,              ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_VAC"     , "Fuel Rail Pressure (relative to vacuum)" , b"0122", 2, fuel_pres_vac,         ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_DIRECT"  , "Fuel Rail Pressure (direct inject)"      , b"0123", 2, fuel_pres_direct,      ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_VOLTAGE"           , "02 Sensor 1 WR Lambda Voltage"           , b"0124", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_VOLTAGE"           , "02 Sensor 2 WR Lambda Voltage"           , b"0125", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_VOLTAGE"           , "02 Sensor 3 WR Lambda Voltage"           , b"0126", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_VOLTAGE"           , "02 Sensor 4 WR Lambda Voltage"           , b"0127", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_VOLTAGE"           , "02 Sensor 5 WR Lambda Voltage"           , b"0128", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_VOLTAGE"           , "02 Sensor 6 WR Lambda Voltage"           , b"0129", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_VOLTAGE"           , "02 Sensor 7 WR Lambda Voltage"           , b"012A", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_VOLTAGE"           , "02 Sensor 8 WR Lambda Voltage"           , b"012B", 4, sensor_voltage_big,    ECU.ENGINE, True),
    OBDCommand("COMMANDED_EGR"              , "Commanded EGR"                           , b"012C", 1, percent,               ECU.ENGINE, True),
    OBDCommand("EGR_ERROR"                  , "EGR Error"                               , b"012D", 1, percent_centered,      ECU.ENGINE, True),
    OBDCommand("EVAPORATIVE_PURGE"          , "Commanded Evaporative Purge"             , b"012E", 1, percent,               ECU.ENGINE, True),
    OBDCommand("FUEL_LEVEL"                 , "Fuel Level Input"                        , b"012F", 1, percent,               ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("WARMUPS_SINCE_DTC_CLEAR"    , "Number of warm-ups since codes cleared"  , b"0130", 1, count,                 ECU.ENGINE, True),
    OBDCommand("DISTANCE_SINCE_DTC_CLEAR"   , "Distance traveled since codes cleared"   , b"0131", 2, distance,              ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE"        , "Evaporative system vapor pressure"       , b"0132", 2, evap_pressure,         ECU.ENGINE, True),
    OBDCommand("BAROMETRIC_PRESSURE"        , "Barometric Pressure"                     , b"0133", 1, pressure,              ECU.ENGINE, True),
    OBDCommand("O2_S1_WR_CURRENT"           , "02 Sensor 1 WR Lambda Current"           , b"0134", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S2_WR_CURRENT"           , "02 Sensor 2 WR Lambda Current"           , b"0135", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S3_WR_CURRENT"           , "02 Sensor 3 WR Lambda Current"           , b"0136", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S4_WR_CURRENT"           , "02 Sensor 4 WR Lambda Current"           , b"0137", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S5_WR_CURRENT"           , "02 Sensor 5 WR Lambda Current"           , b"0138", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S6_WR_CURRENT"           , "02 Sensor 6 WR Lambda Current"           , b"0139", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S7_WR_CURRENT"           , "02 Sensor 7 WR Lambda Current"           , b"013A", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("O2_S8_WR_CURRENT"           , "02 Sensor 8 WR Lambda Current"           , b"013B", 4, current_centered,      ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S1"         , "Catalyst Temperature: Bank 1 - Sensor 1" , b"013C", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S1"         , "Catalyst Temperature: Bank 2 - Sensor 1" , b"013D", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B1S2"         , "Catalyst Temperature: Bank 1 - Sensor 2" , b"013E", 2, catalyst_temp,         ECU.ENGINE, True),
    OBDCommand("CATALYST_TEMP_B2S2"         , "Catalyst Temperature: Bank 2 - Sensor 2" , b"013F", 2, catalyst_temp,         ECU.ENGINE, True),

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("PIDS_C"                     , "Supported PIDs [41-60]"                  , b"0140", 4, pid,                   ECU.ENGINE, True),
    OBDCommand("STATUS_DRIVE_CYCLE"         , "Monitor status this drive cycle"         , b"0141", 4, drop,                  ECU.ENGINE, True),
    OBDCommand("CONTROL_MODULE_VOLTAGE"     , "Control module voltage"                  , b"0142", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("ABSOLUTE_LOAD"              , "Absolute load value"                     , b"0143", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("COMMAND_EQUIV_RATIO"        , "Command equivalence ratio"               , b"0144", 2, drop,                  ECU.ENGINE, True),
    OBDCommand("RELATIVE_THROTTLE_POS"      , "Relative throttle position"              , b"0145", 1, percent,               ECU.ENGINE, True),
    OBDCommand("AMBIANT_AIR_TEMP"           , "Ambient air temperature"                 , b"0146", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_B"             , "Absolute throttle position B"            , b"0147", 1, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_POS_C"             , "Absolute throttle position C"            , b"0148", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_D"          , "Accelerator pedal position D"            , b"0149", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_E"          , "Accelerator pedal position E"            , b"014A", 1, percent,               ECU.ENGINE, True),
    OBDCommand("ACCELERATOR_POS_F"          , "Accelerator pedal position F"            , b"014B", 1, percent,               ECU.ENGINE, True),
    OBDCommand("THROTTLE_ACTUATOR"          , "Commanded throttle actuator"             , b"014C", 1, percent,               ECU.ENGINE, True),
    OBDCommand("RUN_TIME_MIL"               , "Time run with MIL on"                    , b"014D", 2, minutes,               ECU.ENGINE, True),
    OBDCommand("TIME_SINCE_DTC_CLEARED"     , "Time since trouble codes cleared"        , b"014E", 2, minutes,               ECU.ENGINE, True),
    OBDCommand("MAX_VALUES"                 , "Various Max values"                      , b"014F", 4, drop,                  ECU.ENGINE, True), # todo: decode this

    #                      name                             description                    cmd  bytes       decoder           ECU       fast
    OBDCommand("MAX_MAF"                    , "Maximum value for mass air flow sensor"  , b"0150", 4, max_maf,               ECU.ENGINE, True),
    OBDCommand("FUEL_TYPE"                  , "Fuel Type"                               , b"0151", 1, fuel_type,             ECU.ENGINE, True),
    OBDCommand("ETHANOL_PERCENT"            , "Ethanol Fuel Percent"                    , b"0152", 1, percent,               ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ABS"    , "Absolute Evap system Vapor Pressure"     , b"0153", 2, abs_evap_pressure,     ECU.ENGINE, True),
    OBDCommand("EVAP_VAPOR_PRESSURE_ALT"    , "Evap system vapor pressure"              , b"0154", 2, evap_pressure_alt,     ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B1"           , "Short term secondary O2 trim - Bank 1"   , b"0155", 2, percent_centered,      ECU.ENGINE, True), # todo: decode seconds value for banks 3 and 4
    OBDCommand("LONG_O2_TRIM_B1"            , "Long term secondary O2 trim - Bank 1"    , b"0156", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("SHORT_O2_TRIM_B2"           , "Short term secondary O2 trim - Bank 2"   , b"0157", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("LONG_O2_TRIM_B2"            , "Long term secondary O2 trim - Bank 2"    , b"0158", 2, percent_centered,      ECU.ENGINE, True),
    OBDCommand("FUEL_RAIL_PRESSURE_ABS"     , "Fuel rail pressure (absolute)"           , b"0159", 2, fuel_pres_direct,      ECU.ENGINE, True),
    OBDCommand("RELATIVE_ACCEL_POS"         , "Relative accelerator pedal position"     , b"015A", 1, percent,               ECU.ENGINE, True),
    OBDCommand("HYBRID_BATTERY_REMAINING"   , "Hybrid battery pack remaining life"      , b"015B", 1, percent,               ECU.ENGINE, True),
    OBDCommand("OIL_TEMP"                   , "Engine oil temperature"                  , b"015C", 1, temp,                  ECU.ENGINE, True),
    OBDCommand("FUEL_INJECT_TIMING"         , "Fuel injection timing"                   , b"015D", 2, inject_timing,         ECU.ENGINE, True),
    OBDCommand("FUEL_RATE"                  , "Engine fuel rate"                        , b"015E", 2, fuel_rate,             ECU.ENGINE, True),
    OBDCommand("EMISSION_REQ"               , "Designed emission requirements"          , b"015F", 1, drop,                  ECU.ENGINE, True),
]


# mode 2 is the same as mode 1, but returns values from when the DTC occured
__mode2__ = []
for c in __mode1__:
    c = c.clone()
    c.command = b"02" + c.command[2:] # change the mode: 0100 ---> 0200
    c.name = "DTC_" + c.name
    c.desc = "DTC " + c.desc
    __mode2__.append(c)


__mode3__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("GET_DTC"                    , "Get DTCs"                                , b"03",   0, dtc,                   ECU.ALL,     False),
]

__mode4__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("CLEAR_DTC"                  , "Clear DTCs and Freeze data"              , b"04",   0, drop,                  ECU.ALL,     False),
]

__mode7__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("GET_FREEZE_DTC"             , "Get Freeze DTCs"                         , b"07",   0, dtc,                   ECU.ALL,     False),
]

__mode9__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("PIDS_9A"                    , "Supported PIDs [01-20]"                  , b"0900", 4, pid,                   ECU.ENGINE,  True),
    OBDCommand("VIN_MESSAGE_COUNT"          , "VIN Message Count"                       , b"0901", 1, count,                 ECU.ENGINE,  True),
    OBDCommand("VIN"                        , "Get Vehicle Identification Number"       , b"0902", 20, raw_string,           ECU.ENGINE,  True),
]

__misc__ = [
    #                      name                             description                    cmd  bytes       decoder           ECU        fast
    OBDCommand("ELM_VERSION"                , "ELM327 version string"                   , b"ATI",  0, raw_string,            ECU.UNKNOWN, False),
    OBDCommand("ELM_VOLTAGE"                , "Voltage detected by OBD-II adapter"      , b"ATRV", 0, elm_voltage,           ECU.UNKNOWN, False),
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
            __mode7__,
            [],
            __mode9__,
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
            logger.warning("OBD commands can only be retrieved by PID value or dict name")


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
            logger.warning("set_supported() only accepts boolean values")


    def has_command(self, c):
        """ checks for existance of a command by OBDCommand object """
        if isinstance(c, OBDCommand):
            return c in self.__dict__.values()
        else:
            logger.warning("has_command() only accepts OBDCommand objects")
            return False


    def has_name(self, s):
        """ checks for existance of a command by name """
        if isinstance(s, str) or isinstance(s, unicode):
            return s.isupper() and (s in self.__dict__.keys())
        else:
            logger.warning("has_name() only accepts string names for commands")
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
            logger.warning("has_pid() only accepts integer values for mode and PID")
            return False


# export this object
commands = Commands()
