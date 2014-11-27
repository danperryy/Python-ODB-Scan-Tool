
import obd
from obd.decoders import pid


def test_list_integrity():
	for mode, cmds in enumerate(obd.commands.modes):
		for pid, cmd in enumerate(cmds):

			# make sure the command tables are in mode & PID order
			assert mode == cmd.get_mode_int()
			assert pid == cmd.get_pid_int()

			# make sure all the fields are set
			assert cmd.name != ""
			assert cmd.desc != ""
			assert (mode >= 1) and (mode <= 9)
			assert (pid >= 0) and (pid <= 196)
			assert cmd.bytes >= 0
			assert hasattr(cmd.decode, '__call__')


def test_unique_names():
	# make sure no two commands have the same name
	names = {}

	for cmds in obd.commands.modes:
		for cmd in cmds:
			assert not names.has_key(cmd.name)
			names[cmd.name] = True


def test_getitem():
	# ensure that __getitem__ works correctly
	for cmds in obd.commands.modes:
		for cmd in cmds:

			# by [mode][pid]
			mode = cmd.get_mode_int()
			pid  = cmd.get_pid_int()
			assert cmd == obd.commands[mode][pid]

			# by [name]
			assert cmd == obd.commands[cmd.name]


def test_pid_getters():
	# ensure that all pid getters are found
	pid_getters = obd.commands.pid_getters()

	for cmds in obd.commands.modes:
		for cmd in cmds:
			if cmd.decode == pid:
				assert cmd in pid_getters
