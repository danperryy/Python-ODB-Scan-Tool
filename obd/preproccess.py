

from utils import Value, Units, hex_to_int


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