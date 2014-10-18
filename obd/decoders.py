
from utils import Value, Unit, Test, unhex, unbin, bitstring, bitToBool
from codes import *



def noop(_hex):
	return _hex




'''
Sensor decoders
Return Value object with value and units
'''

# 0 to 100 %
def percent(_hex):
	v = unhex(_hex)
	v = v * 100.0 / 255.0
	return Value(v, Unit.PERCENT)

# -100 to 100 %
def percent_centered(_hex):
	v = unhex(_hex)
	v = (v - 128) * 100.0 / 128.0
	return Value(v, Unit.PERCENT)

# -40 to 215 C
def temp(_hex):
	v = unhex(_hex)
	v = v - 40
	return Value(v, Unit.C)

# 0 to 1.275 volts
def sensor_voltage(_hex):
	v = unhex(_hex[0:2])
	return Value(v, Unit.VOLT)

# 0 to 765 kPa
def fuel_pressure(_hex):
	v = unhex(_hex)
	v = v * 3
	return Value(v, Unit.KPA)

# 0 to 255 kPa
def intake_pressure(_hex):
	v = unhex(_hex)
	return Value(v, Unit.KPA)

# 0 to 16,383.75 RPM
def rpm(_hex):
	v = unhex(_hex)
	v = v / 4.0
	return Value(v, Unit.RPM)

# 0 to 255 KPH
def speed(_hex):
	v = unhex(_hex)
	return Value(v, Unit.KPH)

# -64 to 63.5
def timing_advance(_hex):
	v = unhex(_hex)
	v = (v - 128) / 2.0
	return Value(v, Unit.DEGREES)

# 0 to 655.35 grams/sec
def maf(_hex):
	v = unhex(_hex)
	v = v / 100.0
	return Value(v, Unit.GRAM_P_SEC)

# 0 to 655.35 seconds
def seconds(_hex):
	v = unhex(_hex)
	return Value(v, Unit.SECONDS)





'''
Special decoders
Return objects, lists, etc
'''



def status(_hex):
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


def mil(_hex):
	v = bitstring(_hex)
	return v[0] == '1'

def dtc_count(_hex):
	v = bitstring(_hex)
	return unbin(v[1:8])


# Get the description of a DTC
def describeCode(code):
	code.upper()
	if DTC.has_key(code):
		return DTC[code]
	else:
		return "Unknown or manufacturer specific code. Consult the internet."

# converts 2 bytes of hex into a DTC code
def dtc(_hex):
	dtc = ""
	bits = bitstring(_hex[0])

	dtc += ['P', 'C', 'B', 'U'][unbin(bits[0:2]))]
	dtc += str(unbin(bits[2:4]))
	dtc += _hex[1:4]
	return dtc

# converts a frame of 2-byte DTCs into a list of DTCs
def dtc_frame(_hex):
	code_length = 4 # number of hex chars consumed by one code
	size = len(_hex / 4) # number of codes defined in THIS FRAME (not total)
	codes = []
	for n in range(size):

		start = code_length * n
		end = start + code_length
		
		codes.append(dtc(_hex[start:end]))

	return codes
