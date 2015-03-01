
from obd.protocols import SAE_J1850_PWM
from obd.elm327 import ELM327


def test_find_primary_ecu():
	# parse from messages

	p = ELM327
	p._ELM327__protocol = SAE_J1850_PWM()

	# use primary ECU when multiple are present
	m = p._ELM327__protocol("48 6B 10 41 00 BE 1F B8 11 AA\r\r 48 6B 12 41 00 BE 1F B8 11 AA\r\r")
	assert p._ELM327__find_primary_ecu(p, m) == 0x10

	# use lone responses regardless
	m = p._ELM327__protocol("48 6B 12 41 00 BE 1F B8 11 AA\r\r")
	assert p._ELM327__find_primary_ecu(p, m) == 0x12

	# if primary ECU is not listed, use response with most PIDs supported
	m = p._ELM327__protocol("48 6B 12 41 00 BE 1F B8 11 AA\r\r 48 6B 14 41 00 00 00 B8 11 AA\r\r ")
	print(m[0].data_bytes)
	assert p._ELM327__find_primary_ecu(p, m) == 0x12

	# if no messages were received, no ECU could be determined
	assert p._ELM327__find_primary_ecu(p, []) == None
