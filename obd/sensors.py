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



from preprocess import *



class OBDCommand():
	def __init__(self, shortname, name, mode, pid, expectedBytes, preprocessor):
		self.shortname = shortname
		self.name      = name
		self.mode = mode # hex mode
		self.pid = pid   # hex PID
		self.expectedBytes = expectedBytes # int number of bytes expected in return
		self.preprocess = preprocessor

	def compute(result):
		if "NODATA" in result:
			return None
		else:
			if len(result) != self.expectedBytes:
				print "Receieved unexpected number of bytes, trying to parse anyways..."

			# return the value object
			return self.preprocess(result)


class sensors():

	# sensors must be in order of PID
	# note, the SHORTNAME field will be used as the dict key for that sensor
	by_PID = [
		#			shortname				name							  mode	PID  bytes  preprocessor
		OBDCommand("PIDS"				, "Supported PIDs"					, "01",	"00" , 4, hex_to_bitstring 	),
		OBDCommand("DTC_STATUS"			, "S-S DTC Cleared"					, "01",	"01" , 4, dtc_decrypt      	),
		OBDCommand("DTC_FF"				, "DTC C-F-F"						, "01",	"02" , 2, cpass            	),
		OBDCommand("FUEL_STATUS"		, "Fuel System Status"				, "01",	"03" , 2, cpass            	),
		OBDCommand("LOAD"				, "Calculated Engine Load"			, "01",	"041", 1, percent_scale    	),
		OBDCommand("COOLANT_TEMP"		, "Engine Coolant Temperature"		, "01",	"05" , 1, temp             	),
		OBDCommand("SHORT_FUEL_TRIM_1"	, "Short Term Fuel Trim - Bank 1"	, "01",	"06" , 1, fuel_trim_percent	),
		OBDCommand("Long_FUEL_TRIM_1"	, "Long Term Fuel Trim - Bank 1"	, "01",	"07" , 1, fuel_trim_percent	),
		OBDCommand("SHORT_FUEL_TRIM_2"	, "Short Term Fuel Trim - Bank 2"	, "01",	"08" , 1, fuel_trim_percent	),
		OBDCommand("LONG_FUEL_TRIM_2"	, "Long Term Fuel Trim - Bank 2"	, "01",	"09" , 1, fuel_trim_percent	),
		OBDCommand("FUEL_PRESSURE"		, "Fuel Pressure"					, "01",	"0A" , 1, fuel_pressure    	),
		OBDCommand("INTAKE_PRESSURE"	, "Intake Manifold Pressure"		, "01",	"0B" , 1, intake_pressure  	),
		OBDCommand("RPM"				, "Engine RPM"						, "01",	"0C1", 2, rpm              	),
		OBDCommand("SPEED"				, "Vehicle Speed"					, "01",	"0D1", 1, speed            	),
		OBDCommand("TIMING_ADVANCE"		, "Timing Advance"					, "01",	"0E" , 1, timing_advance   	),
		OBDCommand("INTAKE_TEMP"		, "Intake Air Temp"					, "01",	"0F" , 1, temp             	),
		OBDCommand("MAF"				, "Air Flow Rate (MAF)"				, "01",	"10" , 2, maf              	),
		OBDCommand("THROTTLE"			, "Throttle Position"				, "01",	"111", 1, throttle_pos     	),
		OBDCommand("AIR_STATUS"			, "Secondary Air Status"			, "01",	"12" , 1, cpass            	),
		OBDCommand("O2_SENSORS"			, "O2 Sensors Present"				, "01",	"13" , 1, cpass            	),
		OBDCommand("O2_B1_S1"			, "O2: Bank 1 - Sensor 1"			, "01",	"14" , 2, fuel_trim_percent	),
		OBDCommand("O2_B1_S2"			, "O2: Bank 1 - Sensor 2"			, "01",	"15" , 2, fuel_trim_percent	),
		OBDCommand("O2_B1_S3"			, "O2: Bank 1 - Sensor 3"			, "01",	"16" , 2, fuel_trim_percent	),
		OBDCommand("O2_B1_S4"			, "O2: Bank 1 - Sensor 4"			, "01",	"17" , 2, fuel_trim_percent	),
		OBDCommand("O2_B2_S1"			, "O2: Bank 2 - Sensor 1"			, "01",	"18" , 2, fuel_trim_percent	),
		OBDCommand("O2_B2_S2"			, "O2: Bank 2 - Sensor 2"			, "01",	"19" , 2, fuel_trim_percent	),
		OBDCommand("O2_B2_S3"			, "O2: Bank 2 - Sensor 3"			, "01",	"1A" , 2, fuel_trim_percent	),
		OBDCommand("O2_B2_S4"			, "O2: Bank 2 - Sensor 4"			, "01",	"1B" , 2, fuel_trim_percent	),
		OBDCommand("OBD_STANDARDS"		, "OBD Standards Compliance"		, "01",	"1C" , 1, cpass            	),
		OBDCommand("O2_SENSORS_ALT"		, "O2 Sensors Present (alternate)"	, "01",	"1D" , 1, cpass            	),
		OBDCommand("AUX_INPUT_STATUS"	, "Auxiliary input status"			, "01",	"1E" , 1, cpass            	),
		OBDCommand("RUN_TIME"			, "Engine Run Time"					, "01",	"1F" , 2, sec_to_min       	),
		#Sensor("RUN_TIME_MIL"		, "Engine Run Time MIL"					, "014D" , sec_to_min       , "min"		),
	]

# allow commands to be accessed by name
for sensor in sensors.by_PID:
	sensors.__dict__[sensor.shortname] = sensor
