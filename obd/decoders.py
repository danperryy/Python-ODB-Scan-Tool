
import math
from utils import *
from codes import *


# todo
def todo(_hex, r):
	r.set(_hex, Unit.NONE)

# hex in, hex out
def noop(_hex, r):
	r.set(_hex, Unit.NONE)

# hex in, bitstring out
def pid(_hex, r):
	v = bitstring(_hex)
	r.set(v, Unit.NONE)

'''
Sensor decoders
Return Value object with value and units
'''

def count(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.COUNT)

# 0 to 100 %
def percent(_hex, r):
	v = unhex(_hex[0:2])
	v = v * 100.0 / 255.0
	r.set(v, Unit.PERCENT)

# -100 to 100 %
def percent_centered(_hex, r):
	v = unhex(_hex[0:2])
	v = (v - 128) * 100.0 / 128.0
	r.set(v, Unit.PERCENT)

# -40 to 215 C
def temp(_hex, r):
	v = unhex(_hex)
	v = v - 40
	r.set(v, Unit.C)

# -40 to 6513.5 C
def catalyst_temp(_hex, r):
	v = unhex(_hex)
	v = (v / 10.0) - 40
	r.set(v, Unit.C)

# -128 to 128 mA
def current_centered(_hex, r):
	v = unhex(_hex[4:8])
	v = (v / 256.0) - 128
	r.set(v, Unit.MA)

# 0 to 1.275 volts
def sensor_voltage(_hex, r):
	v = unhex(_hex[0:2])
	v = v / 200.0
	r.set(v, Unit.VOLT)

# 0 to 8 volts
def sensor_voltage_big(_hex, r):
	v = unhex(_hex[4:8])
	v = (v * 8.0) / 65535
	r.set(v, Unit.VOLT)

# 0 to 765 kPa
def fuel_pressure(_hex, r):
	v = unhex(_hex)
	v = v * 3
	r.set(v, Unit.KPA)

# 0 to 255 kPa
def pressure(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.KPA)

# 0 to 5177 kPa
def fuel_pres_vac(_hex, r):
	v = unhex(_hex)
	v = v * 0.079
	r.set(v, Unit.KPA)

# 0 to 655,350 kPa
def fuel_pres_direct(_hex, r):
	v = unhex(_hex)
	v = v * 10
	r.set(v, Unit.KPA)

# -8192 to 8192 Pa
def evap_pressure(_hex, r):
	# decode the twos complement
	a = twos_comp(unhex(_hex[0:2], 8))
	b = twos_comp(unhex(_hex[2:4], 8))
	v = ((a * 256.0) + b) / 4.0
	r.set(v, Unit.PA)

# 0 to 327.675 kPa
def abs_evap_pressure(_hex, r):
	v = unhex(_hex)
	v = v / 200
	r.set(v, Unit.KPA)

# -32767 to 32768 Pa
def evap_pressure_alt(_hex, r):
	v = unhex(_hex)
	v = v - 32767
	r.set(v, Unit.PA)

# 0 to 16,383.75 RPM
def rpm(_hex, r):
	v = unhex(_hex)
	v = v / 4.0
	r.set(v, Unit.RPM)

# 0 to 255 KPH
def speed(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.KPH)

# -64 to 63.5 degrees
def timing_advance(_hex, r):
	v = unhex(_hex)
	v = (v - 128) / 2.0
	r.set(v, Unit.DEGREES)

# -210 to 301 degrees
def inject_timing(_hex, r):
	v = unhex(_hex)
	v = (v - 26880) / 128.0
	r.set(v, Unit.DEGREES)

# 0 to 655.35 grams/sec
def maf(_hex, r):
	v = unhex(_hex)
	v = v / 100.0
	r.set(v, Unit.GPS)

# 0 to 2550 grams/sec
def max_maf(_hex, r):
	v = unhex(_hex[0:2])
	v = v * 10
	r.set(v, Unit.GPS)

# 0 to 65535 seconds
def seconds(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.SECONDS)

# 0 to 65535 minutes
def minutes(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.MIN)

# 0 to 65535 km
def distance(_hex, r):
	v = unhex(_hex)
	r.set(v, Unit.KM)

# 0 to 3212 Liters/hour
def fuel_rate(_hex, r):
	v = unhex(_hex)
	v = v * 0.05
	r.set(v, Unit.LPH)


'''
Special decoders
Return objects, lists, etc
'''



def status(_hex, r):
	bits = bitstring(_hex)

	output = {}
	output["Check Engine Light"] = bitToBool(bits[0])
	output["DTC Count"]          = unbin(bits[1:8])
	output["Ignition Type"]      = IGNITION_TYPE[unbin(bits[12])]
	output["Tests"]              = []

	output["Tests"].append(Test("Misfire", \
								bitToBool(bits[15]), \
								bitToBool(bits[11])))

	output["Tests"].append(Test("Fuel System", \
								bitToBool(bits[16]), \
								bitToBool(bits[12])))

	output["Tests"].append(Test("Components", \
								bitToBool(bits[17]), \
								bitToBool(bits[13])))


	# different tests for different ignition types 
	if(output["Ignition Type"] == IGNITION_TYPE[0]): # spark
		for i in range(8):
			if SPARK_TESTS[i] is not None:

				t = Test(SPARK_TESTS[i], \
						 bitToBool(bits[(2 * 8) + i]), \
						 bitToBool(bits[(3 * 8) + i]))

				output["Tests"].append(t)

	elif(output["Ignition Type"] == IGNITION_TYPE[1]): # compression
		for i in range(8):
			if COMPRESSION_TESTS[i] is not None:

				t = Test(COMPRESSION_TESTS[i], \
						 bitToBool(bits[(2 * 8) + i]), \
						 bitToBool(bits[(3 * 8) + i]))
				
				output["Tests"].append(t)

	return output



def fuel_status(_hex, r):
	v = unhex(_hex)
	i = int(math.sqrt(v)) # only a single bit should be on

	v = "Error: Unknown fuel status response"

	if i < len(FUEL_STATUS):
		v = FUEL_STATUS[i]

	r.set(v, Unit.NONE)


def air_status(_hex, r):
	v = unhex(_hex)
	i = int(math.sqrt(v)) # only a single bit should be on

	v = "Error: Unknown air status response"

	if i < len(AIR_STATUS):
		v = AIR_STATUS[i]

	r.set(v, Unit.NONE)

def obd_compliance(_hex, r):
	i = unhex(_hex)

	v = "Error: Unknown OBD compliance response"

	if i < len(OBD_COMPLIANCE):
		v = OBD_COMPLIANCE[i]

	r.set(v, Unit.NONE) 


def fuel_type(_hex, r):
	i = unhex(_hex)

	v = "Error: Unknown fuel type response"

	if i < len(FUEL_TYPES):
		v = FUEL_TYPES[i]

	r.set(v, Unit.NONE)

# Get the description of a DTC
def describeCode(code):
	code.upper()

	v = "Unknown or manufacturer specific code. Consult the internet."

	if DTC.has_key(code):
		v = DTC[code]

	r.set(v, Unit.NONE)

# converts 2 bytes of hex into a DTC code
def dtc(_hex, r):
	dtc = ""
	bits = bitstring(_hex[0])

	dtc += ['P', 'C', 'B', 'U'][unbin(bits[0:2])]
	dtc += str(unbin(bits[2:4]))
	dtc += _hex[1:4]

	r.set(dtc, Unit.NONE)

# converts a frame of 2-byte DTCs into a list of DTCs
def dtc_frame(_hex, r):
	code_length = 4 # number of hex chars consumed by one code
	size = len(_hex / 4) # number of codes defined in THIS FRAME (not total)
	codes = []
	for n in range(size):

		start = code_length * n
		end = start + code_length
		
		codes.append(dtc(_hex[start:end]))

	r.set(codes, Unit.NONE)
