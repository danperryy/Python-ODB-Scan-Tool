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



from decoders import *



class OBDCommand():
	def __init__(self, sensorname, desc, cmd, pid, returnBytes, decoder):
		self.sensorname = sensorname
		self.desc       = desc
		self.cmd        = cmd
		self.bytes      = returnBytes # number of bytes expected in return
		self.decode     = decoder

	def compute(result):
		if "NODATA" in result:
			return ""
		else:
			if (self.bytes > 0) and (len(result) != self.bytes * 2):
				print "Receieved unexpected number of bytes, trying to parse anyways..."

			# return the decoded value object
			return self.decode(result)




# note, the SENSOR NAME field will be used as the dict key for that sensor
# if no sensor name is given, it will be treated as a special command
commands = [
	#			sensor name				description						   cmd   bytes  decoder
	OBDCommand("PIDS"				, "Supported PIDs"					, "0100" , 4, noop				),
	OBDCommand("STATUS"				, "Status since DTCs cleared"		, "0101" , 4, noop				),
	OBDCommand("FREEZE_DTC"			, "Freeze DTC"						, "0102" , 2, noop				),
	OBDCommand("FUEL_STATUS"		, "Fuel System Status"				, "0103" , 2, noop				),
	OBDCommand("LOAD"				, "Calculated Engine Load"			, "0104" , 1, percent			),
	OBDCommand("COOLANT_TEMP"		, "Engine Coolant Temperature"		, "0105" , 1, temp				),
	OBDCommand("SHORT_FUEL_TRIM_1"	, "Short Term Fuel Trim - Bank 1"	, "0106" , 1, percent_centered	),
	OBDCommand("Long_FUEL_TRIM_1"	, "Long Term Fuel Trim - Bank 1"	, "0107" , 1, percent_centered	),
	OBDCommand("SHORT_FUEL_TRIM_2"	, "Short Term Fuel Trim - Bank 2"	, "0108" , 1, percent_centered	),
	OBDCommand("LONG_FUEL_TRIM_2"	, "Long Term Fuel Trim - Bank 2"	, "0109" , 1, percent_centered	),
	OBDCommand("FUEL_PRESSURE"		, "Fuel Pressure"					, "010A" , 1, fuel_pressure		),
	OBDCommand("INTAKE_PRESSURE"	, "Intake Manifold Pressure"		, "010B" , 1, intake_pressure	),
	OBDCommand("RPM"				, "Engine RPM"						, "010C" , 2, rpm				),
	OBDCommand("SPEED"				, "Vehicle Speed"					, "010D" , 1, speed				),
	OBDCommand("TIMING_ADVANCE"		, "Timing Advance"					, "010E" , 1, timing_advance	),
	OBDCommand("INTAKE_TEMP"		, "Intake Air Temp"					, "010F" , 1, temp				),
	OBDCommand("MAF"				, "Air Flow Rate (MAF)"				, "0110" , 2, maf				),
	OBDCommand("THROTTLE"			, "Throttle Position"				, "0111" , 1, percent			),
	OBDCommand("AIR_STATUS"			, "Secondary Air Status"			, "0112" , 1, noop				),
	OBDCommand("O2_SENSORS"			, "O2 Sensors Present"				, "0113" , 1, noop				),
	OBDCommand("O2_B1S1"			, "O2: Bank 1 - Sensor 1"			, "0114" , 2, sensor_voltage	),
	OBDCommand("O2_B1S2"			, "O2: Bank 1 - Sensor 2"			, "0115" , 2, sensor_voltage	),
	OBDCommand("O2_B1S3"			, "O2: Bank 1 - Sensor 3"			, "0116" , 2, sensor_voltage	),
	OBDCommand("O2_B1S4"			, "O2: Bank 1 - Sensor 4"			, "0117" , 2, sensor_voltage	),
	OBDCommand("O2_B2S1"			, "O2: Bank 2 - Sensor 1"			, "0118" , 2, sensor_voltage	),
	OBDCommand("O2_B2S2"			, "O2: Bank 2 - Sensor 2"			, "0119" , 2, sensor_voltage	),
	OBDCommand("O2_B2S3"			, "O2: Bank 2 - Sensor 3"			, "011A" , 2, sensor_voltage	),
	OBDCommand("O2_B2S4"			, "O2: Bank 2 - Sensor 4"			, "011B" , 2, sensor_voltage	),
	OBDCommand("OBD_STANDARDS"		, "OBD Standards Compliance"		, "011C" , 1, noop				),
	OBDCommand("O2_SENSORS_ALT"		, "O2 Sensors Present (alternate)"	, "011D" , 1, noop				),
	OBDCommand("AUX_INPUT_STATUS"	, "Auxiliary input status"			, "011E" , 1, noop				),
	OBDCommand("RUN_TIME"			, "Engine Run Time"					, "011F" , 2, sec_to_min		),
	#OBDCommand("RUN_TIME_MIL"		, "Engine Run Time MIL"				, "014D" , sec_to_min			),
	

	# DTC handling
	#			sensor name				description						   cmd  bytes  decoder
	OBDCommand("GET_DTC"			, "Get DTCs"						, "03" , 0, noop				),
	OBDCommand("CLEAR_DTC"			, "Clear DTCs"						, "04" , 0, noop				),
	OBDCommand("GET_FREEZE_DTC"		, "Get Freeze DTCs"					, "07" , 0, noop				),
]



class sensors():
	pass

class specials():
	pass


# allow sensor commands to be accessed by name
for command in commands:
	# if the command has no decoder, it is considered a special
	if command.decode == noop:
		specials.__dict__[command.sensorname] = command
	else:
		sensors.__dict__[command.sensorname] = command
