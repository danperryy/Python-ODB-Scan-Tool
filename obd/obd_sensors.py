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





class Units():
	NONE      = None
	BITSTRING = "Bit String"
	PERCENT   = "%"
	VOLTS     = "V"
	DEGREES   = "°"
	SEC       = "Sec"
	MIN       = "Min"
	PSI       = "PSI"
	KPA       = "KPA"
	KPH       = "KPH"
	MPH       = "MPH"
	F         = "F°"
	C         = "C°"


class Value():
	def __init__(self, value, unit):
		self.value = value
		self.unit = unit

	def __str__(self):
		return "%s %s" % (str(self.value), str(self.unit))


class OBDCommand():
	def __init__(self, shortname, name, mode, pid, expectedBytes, convertFunc, unit):
		self.shortname = shortname
		self.name      = name
		self.mode = mode # hex mode
		self.pid = pid   # hex PID
		self.expectedBytes = expectedBytes # int number of bytes expected in return
		self.convert = converterFunc

	def compute(result):
		if "NODATA" in result:
			return None
		else:
			if len(result) != self.expectedBytes:
				print "Receieved unexpected number of bytes, trying to parse anyways..."

			# return the value object
			return Value(self.convert(result), self.unit)


class sensors():

	# sensors must be in order of PID
	# note, the SHORTNAME field will be used as the dict key for that sensor
	by_PID = [
		#			shortname				name							  mode	PID  bytes  convertFunc		unit
		OBDCommand("PIDS"				, "Supported PIDs"					, "01",	"00" , 4, hex_to_bitstring , None			),
		OBDCommand("DTC_STATUS"			, "S-S DTC Cleared"					, "01",	"01" , 4, dtc_decrypt      , None			),
		OBDCommand("DTC_FF"				, "DTC C-F-F"						, "01",	"02" , 2, cpass            , None			),
		OBDCommand("FUEL_STATUS"		, "Fuel System Status"				, "01",	"03" , 2, cpass            , None			),
		OBDCommand("LOAD"				, "Calculated Engine Load"			, "01",	"041", 1, percent_scale    , Units.PERCENT	),
		OBDCommand("COOLANT_TEMP"		, "Engine Coolant Temperature"		, "01",	"05" , 1, temp             , Units.F		),
		OBDCommand("SHORT_FUEL_TRIM_1"	, "Short Term Fuel Trim - Bank 1"	, "01",	"06" , 1, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("Long_FUEL_TRIM_1"	, "Long Term Fuel Trim - Bank 1"	, "01",	"07" , 1, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("SHORT_FUEL_TRIM_2"	, "Short Term Fuel Trim - Bank 2"	, "01",	"08" , 1, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("LONG_FUEL_TRIM_2"	, "Long Term Fuel Trim - Bank 2"	, "01",	"09" , 1, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("FUEL_PRESSURE"		, "Fuel Pressure"					, "01",	"0A" , 1, fuel_pressure    , Units.PSI		),
		OBDCommand("INTAKE_PRESSURE"	, "Intake Manifold Pressure"		, "01",	"0B" , 1, intake_pressure  , Units.PSI		),
		OBDCommand("RPM"				, "Engine RPM"						, "01",	"0C1", 2, rpm              , None			),
		OBDCommand("SPEED"				, "Vehicle Speed"					, "01",	"0D1", 1, speed            , Units.MPH		),
		OBDCommand("TIMING_ADVANCE"		, "Timing Advance"					, "01",	"0E" , 1, timing_advance   , Units.DEGREES	),
		OBDCommand("INTAKE_TEMP"		, "Intake Air Temp"					, "01",	"0F" , 1, temp             , Units.F		),
		OBDCommand("MAF"				, "Air Flow Rate (MAF)"				, "01",	"10" , 2, maf              , "lb/min"		),
		OBDCommand("THROTTLE"			, "Throttle Position"				, "01",	"111", 1, throttle_pos     , Units.PERCENT	),
		OBDCommand("AIR_STATUS"			, "Secondary Air Status"			, "01",	"12" , 1, cpass            , None			),
		OBDCommand("O2_SENSORS"			, "O2 Sensors Present"				, "01",	"13" , 1, cpass            , None			),
		OBDCommand("O2_B1_S1"			, "O2: Bank 1 - Sensor 1"			, "01",	"14" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B1_S2"			, "O2: Bank 1 - Sensor 2"			, "01",	"15" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B1_S3"			, "O2: Bank 1 - Sensor 3"			, "01",	"16" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B1_S4"			, "O2: Bank 1 - Sensor 4"			, "01",	"17" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B2_S1"			, "O2: Bank 2 - Sensor 1"			, "01",	"18" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B2_S2"			, "O2: Bank 2 - Sensor 2"			, "01",	"19" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B2_S3"			, "O2: Bank 2 - Sensor 3"			, "01",	"1A" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("O2_B2_S4"			, "O2: Bank 2 - Sensor 4"			, "01",	"1B" , 2, fuel_trim_percent, Units.PERCENT	),
		OBDCommand("OBD_STANDARDS"		, "OBD Standards Compliance"		, "01",	"1C" , 1, cpass            , None			),
		OBDCommand("O2_SENSORS_ALT"		, "O2 Sensors Present (alternate)"	, "01",	"1D" , 1, cpass            , None			),
		OBDCommand("AUX_INPUT_STATUS"	, "Auxiliary input status"			, "01",	"1E" , 1, cpass            , None			),
		OBDCommand("RUN_TIME"			, "Engine Run Time"					, "01",	"1F" , 2, sec_to_min       , Units.MIN		),
		#Sensor("RUN_TIME_MIL"		, "Engine Run Time MIL"					, "014D" , sec_to_min       , "min"		),
	]

# allow commands to be accessed by name
for sensor in sensors.by_PID:
	sensors.__dict__[sensor.shortname] = sensor

