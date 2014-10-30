
from sys import stdin, stdout, argv

stdout.write("=============================\n")
stdout.write("Welcome to the python-OBD CLI\n")
stdout.write("=============================\n")

def printHelp():
	stdout.write("""
Built for python 2.7

	python obd                auto-detects serial port
	python obd <port_name>    opens specified serial port

	OBD >>> <command_name>    sends command and prints result
	OBD >>> <mode>:<PID>      sends command and prints result
	OBD >>> list              lists all available commands

""")
	

# catch the help flag
if ("help" in argv) or ("--help" in argv):
	printHelp()
	exit()


import obd
obd.debug.console = True
o = None

# connect
if len(argv) == 1:
	o = obd.OBD() # connect using scanSerial
elif len(argv) == 2:
	o = obd.OBD(argv[1]) # connect to specified port
else:
	stdout.write("Unknown command arguments. Please see 'python obd --help'")


def listCommands(o):
	stdout.write("Supported Commands\n")
	for c in o.supportedCommands:
		stdout.write("\t%s:%s\t%s\n" % (c.mode, c.pid, c.desc))
	


if o is not None and o.is_connected():
	
	listCommands(o)

	while True:
		stdout.write("\nOBD >>> ")
		i = stdin.readline()
		i = i.strip()
		i = i.upper()

		if i in ["EXIT", "QUIT"]:
			stdout.write("Goodbye\n")
			break;

		if i == "HELP":
			printHelp()
			continue

		if i == "LIST":
			listCommands(o)
			continue;

		parts = i.split(':')

		try:
			# parse the user's input
			command = None

			if len(parts) == 1:
				command = obd.commands[parts[0]]
			elif len(parts) == 2:
				mode = int(parts[0], 16)
				pid = int(parts[1], 16)
				command = obd.commands[mode][pid]

			# send command and print result
			if command is not None and o.has_command(command):
				r = o.query(command)
				stdout.write("\nDecoded Result:\n%s\n" % str(r))
			else:
				stdout.write("Unsupported command: %s" % str(command))

		except:
			stdout.write("Could not parse command\n")
