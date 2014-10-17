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
	def __init__(self, sensorname, desc, mode, pid, pid, returnBytes, decoder):
		self.sensorname = sensorname
		self.desc       = desc
		self.mode       = mode
		self.pid        = pid
		self.bytes      = returnBytes # number of bytes expected in return
		self.decode     = decoder

	def clone(self):
		return OBDCommand(self.sensorname,
						  self.desc,
						  self.mode,
						  self.pid,
						  self.bytes,
						  self.decode)

	def getCommand(self):
		return self.mode + self.pid

	def compute(result):
		if "NODATA" in result:
			return ""
		else:
			if (self.bytes > 0) and (len(result) != self.bytes * 2):
				print "Receieved unexpected number of bytes, trying to parse anyways..."

			# return the decoded value object
			return self.decode(result)




# note, the SENSOR NAME field will be used as the dict key for that sensor

__mode1__ = [
	# mode 1
	#			sensor name				description						  mode  cmd  bytes  decoder
	OBDCommand("PIDS"				, "Supported PIDs"					, "01", "00" , 4, noop				),
	OBDCommand("STATUS"				, "Status since DTCs cleared"		, "01", "01" , 4, noop				),
	OBDCommand("FREEZE_DTC"			, "Freeze DTC"						, "01", "02" , 2, noop				),
	OBDCommand("FUEL_STATUS"		, "Fuel System Status"				, "01", "03" , 2, noop				),
	OBDCommand("LOAD"				, "Calculated Engine Load"			, "01", "04" , 1, percent			),
	OBDCommand("COOLANT_TEMP"		, "Engine Coolant Temperature"		, "01", "05" , 1, temp				),
	OBDCommand("SHORT_FUEL_TRIM_1"	, "Short Term Fuel Trim - Bank 1"	, "01", "06" , 1, percent_centered	),
	OBDCommand("Long_FUEL_TRIM_1"	, "Long Term Fuel Trim - Bank 1"	, "01", "07" , 1, percent_centered	),
	OBDCommand("SHORT_FUEL_TRIM_2"	, "Short Term Fuel Trim - Bank 2"	, "01", "08" , 1, percent_centered	),
	OBDCommand("LONG_FUEL_TRIM_2"	, "Long Term Fuel Trim - Bank 2"	, "01", "09" , 1, percent_centered	),
	OBDCommand("FUEL_PRESSURE"		, "Fuel Pressure"					, "01", "0A" , 1, fuel_pressure		),
	OBDCommand("INTAKE_PRESSURE"	, "Intake Manifold Pressure"		, "01", "0B" , 1, intake_pressure	),
	OBDCommand("RPM"				, "Engine RPM"						, "01", "0C" , 2, rpm				),
	OBDCommand("SPEED"				, "Vehicle Speed"					, "01", "0D" , 1, speed				),
	OBDCommand("TIMING_ADVANCE"		, "Timing Advance"					, "01", "0E" , 1, timing_advance	),
	OBDCommand("INTAKE_TEMP"		, "Intake Air Temp"					, "01", "0F" , 1, temp				),
	OBDCommand("MAF"				, "Air Flow Rate (MAF)"				, "01", "10" , 2, maf				),
	OBDCommand("THROTTLE"			, "Throttle Position"				, "01", "11" , 1, percent			),
	OBDCommand("AIR_STATUS"			, "Secondary Air Status"			, "01", "12" , 1, noop				),
	OBDCommand("O2_SENSORS"			, "O2 Sensors Present"				, "01", "13" , 1, noop				),
	OBDCommand("O2_B1S1"			, "O2: Bank 1 - Sensor 1"			, "01", "14" , 2, sensor_voltage	),
	OBDCommand("O2_B1S2"			, "O2: Bank 1 - Sensor 2"			, "01", "15" , 2, sensor_voltage	),
	OBDCommand("O2_B1S3"			, "O2: Bank 1 - Sensor 3"			, "01", "16" , 2, sensor_voltage	),
	OBDCommand("O2_B1S4"			, "O2: Bank 1 - Sensor 4"			, "01", "17" , 2, sensor_voltage	),
	OBDCommand("O2_B2S1"			, "O2: Bank 2 - Sensor 1"			, "01", "18" , 2, sensor_voltage	),
	OBDCommand("O2_B2S2"			, "O2: Bank 2 - Sensor 2"			, "01", "19" , 2, sensor_voltage	),
	OBDCommand("O2_B2S3"			, "O2: Bank 2 - Sensor 3"			, "01", "1A" , 2, sensor_voltage	),
	OBDCommand("O2_B2S4"			, "O2: Bank 2 - Sensor 4"			, "01", "1B" , 2, sensor_voltage	),
	OBDCommand("OBD_STANDARDS"		, "OBD Standards Compliance"		, "01", "1C" , 1, noop				),
	OBDCommand("O2_SENSORS_ALT"		, "O2 Sensors Present (alternate)"	, "01", "1D" , 1, noop				),
	OBDCommand("AUX_INPUT_STATUS"	, "Auxiliary input status"			, "01", "1E" , 1, noop				),
	OBDCommand("RUN_TIME"			, "Engine Run Time"					, "01", "1F" , 2, seconds			),
	#OBDCommand("RUN_TIME_MIL"		, "Engine Run Time MIL"				, "01", "4D" , sec_to_min			),
]

# mode 2 is the same as mode 1, but returns values from when the DTC occured
__mode2__ = []
for c in __mode1__:
	c = c.clone()
	c.mode = "02"
	c.name = "DTC_" + c.name
	c.desc = "DTC " + c.desc
	__mode2__.append(c)


__mode3__ = [
	#			sensor name				description						  mode  cmd  bytes  decoder
	OBDCommand("GET_DTC"			, "Get DTCs"						, "03", "" , 0, noop				),
]

__mode4__ = [
	#			sensor name				description						  mode  cmd  bytes  decoder
	OBDCommand("CLEAR_DTC"			, "Clear DTCs"						, "04", "" , 0, noop				),
]

__mode7__ [
	#			sensor name				description						  mode  cmd  bytes  decoder
	OBDCommand("GET_FREEZE_DTC"		, "Get Freeze DTCs"					, "07", "" , 0, noop				),
]




# assemble the commands by mode
commands = [
	[],
	__mode1__,
	__mode2__,
	__mode3__,
	__mode4__,
	[],
	[],
	__mode7__
]


class sensors():
	pass

class specials():
	pass


# allow sensor commands to be accessed by name
for m in commands:
	for c in m:
		# if the command has no decoder, it is considered a special
		if c.decode == noop:
			specials.__dict__[c.sensorname] = c
		else:
			sensors.__dict__[c.sensorname] = c
