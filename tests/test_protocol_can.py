
import random
from obd.protocols import *
from obd.protocols.protocol import Message

from obd import debug
debug.console = True


CAN_11_PROTOCOLS = [
	ISO_15765_4_11bit_500k,
	ISO_15765_4_11bit_250k,
]

CAN_29_PROTOCOLS = [
	ISO_15765_4_29bit_500k,
	ISO_15765_4_29bit_250k,
	SAE_J1939
]


def check_message(m, num_frames, tx_id, data):
		""" generic test for correct message values """
		assert len(m.frames) == num_frames
		assert m.tx_id       == tx_id
		assert m.data        == data





def test_single_frame():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol([])


		r = p(["7E8 06 41 00 00 01 02 03"])
		assert len(r) == 1
		check_message(r[0], 1, 0x0, list(range(4)))



def test_hex_straining():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol([])


		r = p(["NO DATA"])
		assert len(r) == 0

		r = p(["TOTALLY NOT HEX"])
		assert len(r) == 0

		r = p(["NO DATA", "7E8 06 41 00 00 01 02 03"])
		assert len(r) == 1
		check_message(r[0], 1, 0x0, list(range(4)))

		r = p(["NO DATA", "NO DATA"])
		assert len(r) == 0



def test_multi_ecu():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol([])


		test_case = [
			"7E8 06 41 00 00 01 02 03",
			"7EB 06 41 00 00 01 02 03",
			"7EA 06 41 00 00 01 02 03",
		]

		correct_data = list(range(4))

		# seperate ECUs, single frames each
		r = p(test_case)
		assert len(r) == 3

		# messages are returned in ECU order
		check_message(r[0], 1, 0x0, correct_data)
		check_message(r[1], 1, 0x2, correct_data)
		check_message(r[2], 1, 0x3, correct_data)




def test_multi_line():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol([])


		test_case = [
			"7E8 10 20 49 04 00 01 02 03",
			"7E8 21 04 05 06 07 08 09 0A",
			"7E8 22 0B 0C 0D 0E 0F 10 11",
			"7E8 23 12 13 14 15 16 17 18"
		]

		correct_data = list(range(25))

		# in-order
		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0x0, correct_data)

		# test a few out-of-order cases
		for n in range(4):
			random.shuffle(test_case) # mix up the frame strings
			r = p(test_case)
			assert len(r) == 1
			check_message(r[0], len(test_case), 0x0, correct_data)


		# missing frames in a multi-frame message should drop the message
		# (tests the contiguity check, and data length byte)

		test_case = [
			"7E8 10 20 49 04 00 01 02 03",
			"7E8 21 04 05 06 07 08 09 0A",
			"7E8 22 0B 0C 0D 0E 0F 10 11",
			"7E8 23 12 13 14 15 16 17 18"
		]

		for n in range(len(test_case) - 1):
			sub_test = list(test_case)
			del sub_test[n]

			r = p(sub_test)
			assert len(r) == 0


		# MODE 03 COMMANDS (GET_DTC) RETURN NO PID BYTE

		test_case = [
			"7E8 10 20 43 04 00 01 02 03",
			"7E8 21 04 05 06 07 08 09 0A",
		]

		correct_data = list(range(8))

		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0, correct_data)



def test_can_29():
	pass
