
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


def check_message(m, num_frames, tx_id, data_bytes):
		""" generic test for correct message values """
		assert len(m.frames) == num_frames
		assert m.tx_id       == tx_id
		assert m.data_bytes  == data_bytes


def test_can_11():
	for protocol in CAN_11_PROTOCOLS:
		p = protocol()

		# single frame cases

		r = p(["7E8 06 41 00 BE 7F B8 13"])
		assert len(r) == 1
		check_message(r[0], 1, 0, [190, 127, 184, 19])

		r = p(["NO DATA"])
		assert len(r) == 0

		r = p(["TOTALLY NOT HEX"])
		assert len(r) == 0

		# seperate ECUs, single frames each
		r = p(["7E8 06 41 00 BE 7F B8 13", "7EB 06 41 00 80 40 00 01", "7EA 06 41 00 80 00 00 01"])
		assert len(r) == 3
		# messages are returned in ECU order
		check_message(r[0], 1, 0, [190, 127, 184, 19])
		check_message(r[1], 1, 2, [128, 0,   0,   1 ])
		check_message(r[2], 1, 3, [128, 64,  0,   1 ])

		r = p(["NO DATA", "7E8 06 41 00 BE 7F B8 13"])
		assert len(r) == 1
		check_message(r[0], 1, 0, [190, 127, 184, 19])

		r = p(["NO DATA", "NO DATA"])
		assert len(r) == 0



		# MULTI-LINE STITCHING

		test_case = [
			"7E8 10 20 49 04 00 01 02 03",
			"7E8 21 04 05 06 07 08 09 0A",
			"7E8 22 0B 0C 0D 0E 0F 10 11",
			"7E8 23 12 13 14 15 16 17 18"
		]

		correct_data = list(range(25)) # range(25) = [00, 01, 02 ... 17, 18]

		# in-order
		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0, correct_data)

		# test a few out-of-order cases
		for n in range(4):
			random.shuffle(test_case) # mix up the frame strings
			r = p(test_case)
			assert len(r) == 1
			check_message(r[0], len(test_case), 0, correct_data)



		# MODE 03 COMMANDS (GET_DTC) RETURN NO PID BYTE

		test_case = [
			"7E8 10 20 43 00 01 02 03 04",
			"7E8 21 05 06 07 08 09 0A 0B",
		]

		correct_data = list(range(12)) # range(12) = [00, 01, 02 ... 0A, 0B]

		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0, correct_data)



		'''
		# multi-line with shorter length
		r = p(["7E8 10 14 01 02 03 04 05 06",
		       "7E8 21 07 08 09 0A 0B 0C 0D",
		       "7E8 22 0E 0F 10 11 12 13 14"
		])
		assert len(r) == 1
		check_message(r[0], 3, 0, list(range(2, 20)))
		'''


		'''
		r = p(["7E8 10 13 49 04 01 35 36 30",
				"7E8 21 32 38 39 34 39 41 43",
				"7E8 22 00 00 00 00 00 00 31"
		])
		assert len(r) == 1
		'''


def test_can_29():
	pass
