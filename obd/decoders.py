

from utils import Value, Unit, unhex, unbin, bitstring



# functions accepting hex responses from the OBD connection, and computing/returning values with units

def noop(_hex):
	return Value(_hex, Unit.NONE)

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


# these functions draw data from the same PID
def mil(_hex):
	v = bitstring(_hex)
	return v[0] == '1'

def dtc_count(_hex):
	v = bitstring(_hex)
	return unbin(v[1:8])

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
