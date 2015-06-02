
import obd
from obd.decoders import pid


def test_list_integrity():
	for mode, cmds in enumerate(obd.commands.modes):
		for pid, cmd in enumerate(cmds):

			assert cmd.command != "",         "The Command's command string must not be null"

			# make sure the command tables are in mode & PID order
			assert mode == cmd.mode_int,      "Command is in the wrong mode list: %s" % cmd.name
			assert pid == cmd.pid_int,        "The index in the list must also be the PID: %s" % cmd.name

			# make sure all the fields are set
			assert cmd.name != "",                  "Command names must not be null"
			assert cmd.name.isupper(),              "Command names must be upper case"
			assert ' ' not in cmd.name,             "No spaces allowed in command names"
			assert cmd.desc != "",                  "Command description must not be null"
			assert (mode >= 1) and (mode <= 9),     "Mode must be in the range [1, 9] (decimal)"
			assert (pid >= 0) and (pid <= 196),     "PID must be in the range [0, 196] (decimal)"
			assert cmd.bytes >= 0,                  "Number of return bytes must be >= 0"
			assert hasattr(cmd.decode, '__call__'), "Decode is not callable"


def test_unique_names():
	# make sure no two commands have the same name
	names = {}

	for cmds in obd.commands.modes:
		for cmd in cmds:
			assert not names.__contains__(cmd.name), "Two commands share the same name: %s" % cmd.name
			names[cmd.name] = True


def test_getitem():
	# ensure that __getitem__ works correctly
	for cmds in obd.commands.modes:
		for cmd in cmds:

			# by [mode][pid]
			mode = cmd.mode_int
			pid  = cmd.pid_int
			assert cmd == obd.commands[mode][pid], "mode %d, PID %d could not be accessed through __getitem__" % (mode, pid)

			# by [name]
			assert cmd == obd.commands[cmd.name], "command name %s could not be accessed through __getitem__" % (cmd.name)


def test_contains():

	for cmds in obd.commands.modes:
		for cmd in cmds:

			# by (command)
			assert obd.commands.has_command(cmd)

			# by (mode, pid)
			mode = cmd.mode_int
			pid  = cmd.pid_int
			assert obd.commands.has_pid(mode, pid)

			# by (name)
			assert obd.commands.has_name(cmd.name)

			# by `in`
			assert cmd.name in obd.commands

	# test things NOT in the tables, or invalid parameters
	assert 'modes' not in obd.commands
	assert not obd.commands.has_pid(-1, 0)
	assert not obd.commands.has_pid(1, -1)
	assert not obd.commands.has_command("I'm a string, not an OBDCommand")


def test_pid_getters():
	# ensure that all pid getters are found
	pid_getters = obd.commands.pid_getters()

	for cmds in obd.commands.modes:
		for cmd in cmds:
			if cmd.decode == pid:
				assert cmd in pid_getters
