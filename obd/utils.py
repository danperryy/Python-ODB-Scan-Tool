import serial
import errno



class Unit:
	NONE    = None
	RATIO   = "Ratio"
	COUNT   = "Count"
	PERCENT = "Percent"
	RPM     = "RPM"
	VOLT    = "Volt"
	F       = "F"
	C       = "C"
	SEC     = "Second"
	MIN     = "Minute"
	PA      = "Pa"
	KPA     = "kPa"
	PSI     = "PSI"
	KPH     = "Kilometers per Hour"
	MPH     = "Miles per Hour"
	DEGREES = "Degrees"
	GPS     = "Grams per Second"
	MA      = "mA"
	KM      = "km"
	LPH     = "Liters per Hour"


class Response():
	def __init__(self, raw_data=""):
		self.value   = None
		self.unit    = Unit.NONE
		self.raw_data = raw_data

	def isEmpty(self):
		return (self.value == None) or (len(self.raw_data) == 0)

	def set(self, decode):
		self.value = decode[0]
		self.unit  = decode[1]

	def __str__(self):
		return "%s %s" % (str(self.value), str(self.unit))


class Test():
	def __init__(self, name, available, incomplete):
		self.name       = name
		self.available  = available
		self.incomplete = incomplete

	def __str__(self):
		a = "Available" if self.available else "Unavailable"
		c = "Incomplete" if self.incomplete else "Complete"
		return "Test %s: %s, %s" % (name, a, c)



def unhex(_hex):
	return int(_hex, 16)

def unbin(_bin):
	return int(_bin, 2)

def bitstring(_hex):
	return bin(unhex(_hex))[2:]

def bitToBool(_bit):
	return (_bit == '1')

def twos_comp(val, num_bits):
	"""compute the 2's compliment of int value val"""
	if( (val&(1<<(num_bits-1))) != 0 ):
		val = val - (1<<num_bits)
	return val

# pads or chops hex to the requested number of bytes
def constrainHex(_hex, b):
	diff = (b * 2) - len(_hex) # length discrepency in number of hex digits

	if diff > 0:
		print "Receieved less data than expected, trying to parse anyways..."
		_hex += ('0' * diff) # pad the right side with zeros
	elif diff < 0:
		print "Receieved more data than expected, trying to parse anyways..."
		_hex = _hex[:diff] # chop off the right side to fit

	return _hex


def tryPort(portStr):
	"""returns boolean for port availability"""
	try:
		s = serial.Serial(portStr)
		s.close()   # explicit close 'cause of delayed GC in java
		return True

	except serial.SerialException:
		pass
	except OSError as e:
		if e.errno != errno.ENOENT: # permit "no such file or directory" errors
			raise e

	return False



def scanSerial():
	"""scan for available ports. return a list of serial names"""
	available = []

	# Enable Bluetooh connection
	for i in range(10):
		portStr = "/dev/rfcomm%d" % i
		if tryPort(portStr):
			available.append(portStr)

	# Enable USB connection
	for i in range(256):
		portStr = "/dev/ttyUSB%d" % i
		if tryPort(portStr):
			available.append(portStr)

	# Enable obdsim
	'''
	for i in range(256):
		portStr = "/dev/pts/%d" % i
		if tryPort(portStr):
			available.append(portStr)
	'''
	
	return available
