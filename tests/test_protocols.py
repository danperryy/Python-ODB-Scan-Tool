
from obd.protocols import *
from obd.protocols.protocol import Message


LEGACY_PROTOCOLS = [
	SAE_J1850_PWM,
	SAE_J1850_VPW,
	ISO_9141_2,
	ISO_14230_4_5baud,
	ISO_14230_4_fast
]

CAN_11_PROTOCOLS = [
	ISO_15765_4_11bit_500k,
	ISO_15765_4_11bit_250k,
]

CAN_29_PROTOCOLS = [
	ISO_15765_4_29bit_500k,
	ISO_15765_4_29bit_250k,
	SAE_J1939
]


def check_message(m, num_frames, tx_id, data_bytes):
		""" generic test for correct message values """
		assert len(m.frames) == num_frames
		assert m.tx_id       == tx_id
		assert m.data_bytes  == data_bytes


def test_legacy():
	for protocol in LEGACY_PROTOCOLS:
		p = protocol()

		# single frame cases

		r = p(["48 6B 10 41 00 BE 1F B8 11 AA"])
		assert len(r) == 1
		check_message(r[0], 1, 16, [190, 31, 184, 17])

		r = p(["48 6B 10 41 00 BE 1F B8 11 AA"])
		assert len(r) == 1
		check_message(r[0], 1, 16, [190, 31, 184, 17])

		r = p(["NO DATA"])
		assert len(r) == 0

		r = p(["TOTALLY NOT HEX"])
		assert len(r) == 0

		# multi-frame cases

		# seperate ECUs, single frames each
		r = p(["48 6B 10 41 00 BE 1F B8 11 AA", "48 6B 11 41 00 01 02 03 04 AA"])
		assert len(r) == 2
		check_message(r[0], 1, 16, [190, 31, 184, 17])
		check_message(r[1], 1, 17, [1,   2,  3,   4 ])

		r = p(["NO DATA", "48 6B 10 41 00 BE 1F B8 11 AA"])
		assert len(r) == 1
		check_message(r[0], 1, 16, [190, 31, 184, 17])

		r = p(["NO DATA", "NO DATA"])
		assert len(r) == 0

		# GET_DTC requests
		r = p(["48 6B 10 43 03 00 03 02 03 03 14", "48 6B 10 43 03 04 00 00 00 00 0D"])
		assert len(r) == 1
		check_message(r[0], 2, 16, [0x03, 0x0, 0x03, 0x02, 0x03, 0x03, 0x03, 0x04, 0x0, 0x0, 0x0, 0x0])

'''
def test_can_11():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol()

		# single frame cases

		r = p("7E8 06 41 00 BE 7F B8 13\r\r")
		assert len(r) == 1
		check_message(r[0], 1, 0, [65, 0, 190, 127, 184, 19])

		r = p("7E8 06 41 00 BE 7F B8 13")
		assert len(r) == 1
		check_message(r[0], 1, 0, [65, 0, 190, 127, 184, 19])

		r = p("NO DATA")
		assert len(r) == 0

		r = p("TOTALLY NOT HEX")
		assert len(r) == 0

		# multi-frame cases

		# seperate ECUs, single frames each
		r = p("7E8 06 41 00 BE 7F B8 13 \r7EB 06 41 00 80 40 00 01 \r7EA 06 41 00 80 00 00 01 \r\r")
		assert len(r) == 3
		# messages are returned in ECU order
		check_message(r[0], 1, 0, [65, 0, 190, 127, 184, 19])
		check_message(r[1], 1, 2, [65, 0, 128, 0,   0,   1 ])
		check_message(r[2], 1, 3, [65, 0, 128, 64,  0,   1 ])

		r = p("NO DATA\r\r7E8 06 41 00 BE 7F B8 13\r\r")
		assert len(r) == 1
		check_message(r[0], 1, 0, [65, 0, 190, 127, 184, 19])

		r = p("NO DATA\r\rNO DATA\r\r")
		assert len(r) == 0
'''

def test_can_29():
	pass
