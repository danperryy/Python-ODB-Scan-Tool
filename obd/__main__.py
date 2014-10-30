
from sys import stdin, stdout, argv

stdout.write("=============================\n")
stdout.write("Welcome to the python-OBD CLI\n")
stdout.write("=============================\n")

# catch the help flag
if ("help" in argv) or ("--help" in argv):
	stdout.write("""
Built for python 2.7

	python obd
	python obd <port_name>

	OBD >>> <command_name>
	OBD >>> <mode>:<PID>

""")
	exit()



import obd
obd.debug.console = True

o = None

if len(argv) == 1:
	o = obd.OBD() # connect using scanSerial
elif len(argv) == 2:
	o = obd.OBD(argv[1]) # connect to specified port
else:
	stdout.write("Unknown command arguments. Please see 'python obd --help'")

if o is not None and o.is_connected():
	
	stdout.write("Supported Commands\n")
	for command in self.supportedCommands:
		stdout.write("\t%s" % str(c))

	while True:
		stdout.write("\nOBD >>> ")
		i = stdin.readline()
		i = i.strip()
		i = i.upper()

		if i in ["EXIT", "QUIT"]:
			stdout.write("Goodbye\n")
			break;

