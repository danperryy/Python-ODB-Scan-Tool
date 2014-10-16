import serial
import errno


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



def hex_to_int(str):
    return int(str, 16)



def decrypt_dtc_code(code):
	"""Returns the 5-digit DTC code from hex encoding"""
	dtc = []
	current = code
	for i in range(0,3):
		if len(current)<4:
			raise "Tried to decode bad DTC: %s" % code

		tc = hex_to_int(current[0]) #typecode
		tc = tc >> 2
		if   tc == 0:
			type = "P"
		elif tc == 1:
			type = "C"
		elif tc == 2:
			type = "B"
		elif tc == 3:
			type = "U"
		else:
			raise tc

		dig1 = str(hex_to_int(current[0]) & 3)
		dig2 = str(hex_to_int(current[1]))
		dig3 = str(hex_to_int(current[2]))
		dig4 = str(hex_to_int(current[3]))
		dtc.append(type+dig1+dig2+dig3+dig4)
		current = current[4:]
	return dtc
