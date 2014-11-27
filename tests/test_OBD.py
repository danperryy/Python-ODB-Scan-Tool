
import obd
from obd.utils import Response
from obd.commands import OBDCommand
from obd.decoders import noop


def test_query():
	# we don't need an actual serial connection
	o = obd.OBD("/dev/null")
	# forge our own command, to control the output
	cmd = OBDCommand("", "", "01", "23", 2, noop)

	# forge data IO from the car by overwriting the get/send functions
	
	# buffers
	toCar = [""] # needs to be inside mutable object to allow assignment in closure
	fromCar = ""

	def send(cmd):
		print cmd
		toCar[0] = cmd

	o.port.send = send
	o.port.get = lambda *args: fromCar


	fromCar = "41 23 AB CD\r\r"

	r = o.query(cmd, True)
	
	assert toCar[0] == "0123"    # verify that the command was sent correctly
	assert r.raw_data == fromCar # verify that raw_data was stored in the Response
	assert r.value == "ABCD"     # verify that the response was parsed correctly
