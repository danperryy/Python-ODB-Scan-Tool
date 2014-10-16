#!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################


from obd_utils import hex_to_int


def maf(code):
    code = hex_to_int(code)
    return code * 0.00132276

def throttle_pos(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def fuel_pressure(code): # in kPa
	code = hex_to_int(code)
	return (code * 3) / 0.14504

def intake_pressure(code): # in kPa
    code = hex_to_int(code)
    return code / 0.14504
  
def rpm(code):
    code = hex_to_int(code)
    return code / 4

def speed(code):
    code = hex_to_int(code)
    return code / 1.609

def percent_scale(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def timing_advance(code):
    code = hex_to_int(code)
    return (code - 128) / 2.0

def sec_to_min(code):
    code = hex_to_int(code)
    return code / 60

def temp(code):
    code = hex_to_int(code)
    c = code - 40 
    return 32 + (9 * c / 5) 

def cpass(code):
    #fixme
    return code

def fuel_trim_percent(code):
    code = hex_to_int(code)
    #return (code - 128.0) * 100.0 / 128
    return (code - 128) * 100 / 128

def dtc_decrypt(code):
    #first byte is byte after PID and without spaces
    num = hex_to_int(code[:2]) #A byte
    res = []

    if num & 0x80: # is mil light on
        mil = 1
    else:
        mil = 0
        
    # bit 0-6 are the number of dtc's. 
    num = num & 0x7f
    
    res.append(num)
    res.append(mil)
    
    numB = hex_to_int(code[2:4]) #B byte
      
    for i in range(0,3):
        res.append(((numB>>i)&0x01)+((numB>>(3+i))&0x02))
    
    numC = hex_to_int(code[4:6]) #C byte
    numD = hex_to_int(code[6:8]) #D byte
       
    for i in range(0,7):
        res.append(((numC>>i)&0x01)+(((numD>>i)&0x01)<<1))
    
    res.append(((numD>>7)&0x01)) #EGR SystemC7  bit of different 
    
    #return res
    return "#"

def hex_to_bitstring(str):
    bitstring = ""
    for i in str:
        # silly type safety, we don't want to eval random stuff
        if type(i) == type(''): 
            v = eval("0x%s" % i)
            if v & 8 :
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 4:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 2:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 1:
                bitstring += '1'
            else:
                bitstring += '0'                
    return bitstring


class Sensor:
    def __init__(self, shortname, name, command, valueFunction, unit):
        self.shortname = shortname
        self.name      = name
        self.cmd       = command
        self.value     = valueFunction
        self.unit      = unit
        self.supported = False

    def __str__(self):
        return self.name


class sensors():

	# sensors must be in order of PID
	# note, the SHORTNAME field will be used as the dict key for that sensor
    by_PID = [
		Sensor("PIDS"				, "Supported PIDs"					, "0100" , hex_to_bitstring , ""       ),
		Sensor("DTC_STATUS"			, "S-S DTC Cleared"					, "0101" , dtc_decrypt      , ""       ),
		Sensor("DTC_FF"				, "DTC C-F-F"						, "0102" , cpass            , ""       ),
		Sensor("FUEL_STATUS"		, "Fuel System Status"				, "0103" , cpass            , ""       ),
		Sensor("LOAD"				, "Calculated Engine Load"			, "01041", percent_scale    , "%"      ),
		Sensor("COOLANT_TEMP"		, "Engine Coolant Temperature"		, "0105" , temp             , "F"      ),
		Sensor("SHORT_FUEL_TRIM_1"	, "Short Term Fuel Trim - Bank 1"	, "0106" , fuel_trim_percent, "%"      ),
		Sensor("Long_FUEL_TRIM_1"	, "Long Term Fuel Trim - Bank 1"	, "0107" , fuel_trim_percent, "%"      ),
		Sensor("SHORT_FUEL_TRIM_2"	, "Short Term Fuel Trim - Bank 2"	, "0108" , fuel_trim_percent, "%"      ),
		Sensor("LONG_FUEL_TRIM_2"	, "Long Term Fuel Trim - Bank 2"	, "0109" , fuel_trim_percent, "%"      ),
		Sensor("FUEL_PRESSURE"		, "Fuel Pressure"					, "010A" , fuel_pressure    , "psi"    ),
		Sensor("INTAKE_PRESSURE"	, "Intake Manifold Pressure"		, "010B" , intake_pressure  , "psi"    ),
		Sensor("RPM"				, "Engine RPM"						, "010C1", rpm              , ""       ),
		Sensor("SPEED"				, "Vehicle Speed"					, "010D1", speed            , "MPH"    ),
		Sensor("TIMING_ADVANCE"		, "Timing Advance"					, "010E" , timing_advance   , "degrees"),
		Sensor("INTAKE_TEMP"		, "Intake Air Temp"					, "010F" , temp             , "F"      ),
		Sensor("MAF"				, "Air Flow Rate (MAF)"				, "0110" , maf              , "lb/min" ),
		Sensor("THROTTLE"			, "Throttle Position"				, "01111", throttle_pos     , "%"      ),
		Sensor("AIR_STATUS"			, "Secondary Air Status"			, "0112" , cpass            , ""       ),
		Sensor("O2_SENSORS"			, "O2 Sensors Present"				, "0113" , cpass            , ""       ),
		Sensor("O2_B1_S1"			, "O2: Bank 1 - Sensor 1"			, "0114" , fuel_trim_percent, "%"      ),
		Sensor("O2_B1_S2"			, "O2: Bank 1 - Sensor 2"			, "0115" , fuel_trim_percent, "%"      ),
		Sensor("O2_B1_S3"			, "O2: Bank 1 - Sensor 3"			, "0116" , fuel_trim_percent, "%"      ),
		Sensor("O2_B1_S4"			, "O2: Bank 1 - Sensor 4"			, "0117" , fuel_trim_percent, "%"      ),
		Sensor("O2_B2_S1"			, "O2: Bank 2 - Sensor 1"			, "0118" , fuel_trim_percent, "%"      ),
		Sensor("O2_B2_S2"			, "O2: Bank 2 - Sensor 2"			, "0119" , fuel_trim_percent, "%"      ),
		Sensor("O2_B2_S3"			, "O2: Bank 2 - Sensor 3"			, "011A" , fuel_trim_percent, "%"      ),
		Sensor("O2_B2_S4"			, "O2: Bank 2 - Sensor 4"			, "011B" , fuel_trim_percent, "%"      ),
		Sensor("OBD_STANDARDS"		, "OBD Standards Compliance"		, "011C" , cpass            , ""       ),
		Sensor("O2_SENSORS_ALT"		, "O2 Sensors Present (alternate)"	, "011D" , cpass            , ""       ),
		Sensor("AUX_INPUT_STATUS"	, "Auxiliary input status"			, "011E" , cpass            , ""       ),
		Sensor("RUN_TIME"			, "Engine Run Time"				, "011F" , sec_to_min       , "min"    ),
		#Sensor("RUN_TIME_MIL"		, "Engine Run Time MIL"					, "014D" , sec_to_min       , "min"    ),
    ]

# assemble the dict, to access sensors by name
for sensor in sensors.by_PID:
	sensors.__dict__[sensor.shortname] = sensor

#___________________________________________________________

def test():
    for i in SENSORS:
        print i.name, i.value("F")

if __name__ == "__main__":
    test()
