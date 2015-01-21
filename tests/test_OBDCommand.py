
from obd.commands import OBDCommand
from obd.decoders import noop


def test_constructor():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "23", 2, noop)
	assert cmd.name      == "Test"
	assert cmd.desc      == "example OBD command"
	assert cmd.mode      == "01"
	assert cmd.pid       == "23"
	assert cmd.bytes     == 2
	assert cmd.decode    == noop
	assert cmd.supported == False

	assert cmd.get_command()  == "0123"
	assert cmd.get_mode_int() == 1
	assert cmd.get_pid_int()  == 35

	cmd = OBDCommand("Test", "example OBD command", "01", "23", 2, noop, True)
	assert cmd.supported == True


def test_clone():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "23", 2, noop)
	other = cmd.clone()

	assert cmd.name      == other.name
	assert cmd.desc      == other.desc
	assert cmd.mode      == other.mode
	assert cmd.pid       == other.pid
	assert cmd.bytes     == other.bytes
	assert cmd.decode    == other.decode
	assert cmd.supported == cmd.supported


def test_data_stripping():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "00", 2, noop)
	r = cmd.compute("48 6B 10 41 00 01 01 10\r\n")
	assert not r.is_null()
	assert r.value == "0101"


def test_data_not_hex():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "00", 2, noop)
	r = cmd.compute("48 6B 10 41 00 wx yz 10\r\n")
	assert r.is_null()
	

def test_data_length():
	#                 name       description        mode  cmd bytes decoder
	cmd = OBDCommand("Test", "example OBD command", "01", "00", 2, noop)
	r = cmd.compute("48 6B 10 41 00 01 23 45 10\r\n")
	assert r.value == "0123"
	r = cmd.compute("48 6B 10 41 00 01 10\r\n")
	assert r.value == "0100"
