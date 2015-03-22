
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




		# MODE 03 COMMANDS (GET_DTC) RETURN NO PID BYTE

		test_case = [
			"48 6B 10 43 00 01 02 03 04 05 FF",
			"48 6B 10 43 06 07 08 09 0A 0B FF",
		]

		correct_data = list(range(12)) # data is stitched in order recieved

		r = p(test_case)
		assert len(r) == 1
		check_message(r[0], len(test_case), 0x10, correct_data)
