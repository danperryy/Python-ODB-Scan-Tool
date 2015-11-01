
from obd.commands import OBDCommand
from obd.decoders import noop
from obd.protocols import *


def test_constructor():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "0123", 2, noop, ECU.ENGINE)
	assert cmd.name      == "Test"
	assert cmd.desc      == "example OBD command"
	assert cmd.command   == "0123"
	assert cmd.bytes     == 2
	assert cmd.decode    == noop
	assert cmd.ecu       == ECU.ENGINE
	assert cmd.supported == False

	assert cmd.mode_int      == 1
	assert cmd.pid_int       == 35

	cmd = OBDCommand("Test", "example OBD command", "0123", 2, noop, ECU.ENGINE, True)
	assert cmd.supported == True


def test_clone():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("", "", "0123", 2, noop, ECU.ENGINE)
	other = cmd.clone()

	assert cmd.name      == other.name
	assert cmd.desc      == other.desc
	assert cmd.command   == other.command
	assert cmd.bytes     == other.bytes
	assert cmd.decode    == other.decode
	assert cmd.ecu       == other.ecu
	assert cmd.supported == cmd.supported


def test_call():
	p = SAE_J1850_PWM(["48 6B 10 41 00 FF FF FF FF AA"]) # train the ecu_map to identify the engine
	messages = p(["48 6B 10 41 00 BE 1F B8 11 AA"]) # parse valid data into response object 

	# valid response size
	cmd = OBDCommand("", "", "0123", 4, noop, ECU.ENGINE)
	r = cmd(messages)
	assert r.value == "BE1FB811"

	# response too short (pad)
	cmd = OBDCommand("", "", "0123", 5, noop, ECU.ENGINE)
	r = cmd(messages)
	assert r.value == "BE1FB81100"

	# response too long (clip)
	cmd = OBDCommand("", "", "0123", 3, noop, ECU.ENGINE)
	r = cmd(messages)
	assert r.value == "BE1FB8"


def test_get_mode_int():
	cmd = OBDCommand("", "", "0123", 4, noop, ECU.ENGINE)
	assert cmd.mode_int == 0x01

	cmd = OBDCommand("", "", "", "23", 4, noop, ECU.ENGINE)
	assert cmd.mode_int == 0


def test_pid_int():
	cmd = OBDCommand("", "", "0123", 4, noop, ECU.ENGINE)
	assert cmd.pid_int == 0x23

	cmd = OBDCommand("", "", "01", 4, noop, ECU.ENGINE)
	assert cmd.pid_int == 0
