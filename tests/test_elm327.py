
from obd.protocols import ECU, SAE_J1850_PWM
from obd.elm327 import ELM327


def test_find_primary_ecu():
	# parse from messages

	# use primary ECU when multiple are present
	p = SAE_J1850_PWM(["48 6B 10 41 00 BE 1F B8 11 AA", "48 6B 12 41 00 BE 1F B8 11 AA"])
	assert p.ecu_map.lookup(ECU.ENGINE) == 0x10

	# use lone responses regardless
	p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA"])
	assert p.ecu_map.lookup(ECU.ENGINE) == 0x12

	# if primary ECU is not listed, use response with most PIDs supported
	p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA", "48 6B 14 41 00 00 00 B8 11 AA"])
	assert p.ecu_map.lookup(ECU.ENGINE) == 0x12

	# if no messages were received, the defaults stay in place
	p = SAE_J1850_PWM([])
	assert p.ecu_map.lookup(ECU.ENGINE) == p.TX_ID_ENGINE
