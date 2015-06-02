
import random
from obd.protocols import *
from obd.protocols.protocol import Message

from obd import debug
debug.console = True


LEGACY_PROTOCOLS = [
	SAE_J1850_PWM,
	SAE_J1850_VPW,
	ISO_9141_2,
	ISO_14230_4_5baud,
	ISO_14230_4_fast
]


def check_message(m, num_frames, tx_id, data):
		""" generic test for correct message values """
		assert len(m.frames) == num_frames
		assert m.tx_id       == tx_id
		assert m.data        == data


def test_single_frame():
	for protocol in LEGACY_PROTOCOLS:
		p = protocol([])

		# minimum valid length
		r = p(["48 6B 10 41 00 FF"])
		assert len(r) == 1
		check_message(r[0], 1, 0x10, [])

		# maximum valid length
		r = p(["48 6B 10 41 00 00 01 02 03 04 FF"])
		assert len(r) == 1
		check_message(r[0], 1, 0x10, list(range(5)))

		# to short
		r = p(["48 6B 10 41 FF"])
		assert len(r) == 0

		# to long
		r = p(["48 6B 10 41 00 00 01 02 03 04 05 FF"])
		assert len(r) == 0


def test_hex_straining():
	for protocol in LEGACY_PROTOCOLS:
		p = protocol([])


		r = p(["NO DATA"])
		assert len(r) == 0

		r = p(["TOTALLY NOT HEX"])
		assert len(r) == 0

		r = p(["NO DATA", "NO DATA"])
		assert len(r) == 0

		r = p(["NO DATA", "48 6B 10 41 00 00 01 02 03 FF"])
		assert len(r) == 1
		check_message(r[0], 1, 0x10, list(range(4)))



def test_multi_ecu():
	for protocol in LEGACY_PROTOCOLS:
		p = protocol([])


		test_case = [
			"48 6B 13 41 00 00 01 02 03 FF",			
			"48 6B 10 41 00 00 01 02 03 FF",
			"48 6B 11 41 00 00 01 02 03 FF",
		]

		correct_data = list(range(4))

		# seperate ECUs, single frames each
		r = p(test_case)
		assert len(r) == len(test_case)

		# messages are returned in ECU order
		check_message(r[0], 1, 0x10, correct_data)
		check_message(r[1], 1, 0x11, correct_data)
		check_message(r[2], 1, 0x13, correct_data)



def test_multi_line():
	for protocol in LEGACY_PROTOCOLS:
		p = protocol([])


		test_case = [
			"48 6B 10 49 02 01 00 01 02 03 FF",
			"48 6B 10 49 02 02 04 05 06 07 FF",
			"48 6B 10 49 02 03 08 09 0A 0B FF",
		]

		correct_data = list(range(12))

		# in-order
		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0x10, correct_data)

		# test a few out-of-order cases
		for n in range(4):
			random.shuffle(test_case) # mix up the frame strings
			r = p(test_case)
			assert len(r) == 1
			check_message(r[0], len(test_case), 0x10, correct_data)


		# missing frames in a multi-frame message should drop the message
		# (tests the contiguity check, and data length byte)

		test_case = [
			"48 6B 10 49 02 01 00 01 02 03 FF",
			"48 6B 10 49 02 02 04 05 06 07 FF",
			"48 6B 10 49 02 03 08 09 0A 0B FF",
		]

		for n in range(len(test_case) - 1):
			sub_test = list(test_case)
			del sub_test[n]

			r = p(sub_test)
			assert len(r) == 0


		# MODE 03 COMMANDS (GET_DTC) RETURN NO PID BYTE

		test_case = [
			"48 6B 10 43 00 01 02 03 04 05 FF",
			"48 6B 10 43 06 07 08 09 0A 0B FF",
		]

		correct_data = list(range(12)) # data is stitched in order recieved

		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0x10, correct_data)
