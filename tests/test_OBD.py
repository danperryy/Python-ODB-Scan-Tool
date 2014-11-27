
import obd
from obd.utils import Response
from obd.commands import OBDCommand
from obd.decoders import noop


def test_is_connected():
	o = obd.OBD("/dev/null")
	assert not o.is_connected()

	# todo


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
		toCar[0] = cmd

	o.port.send = send
	o.port.get = lambda *args: fromCar

	# test

	fromCar = "41 23 AB CD\r\r"
	r = o.query(cmd)             # make sure unsupported commands don't send
	assert toCar[0] == ""
	assert r.is_null()

	fromCar = "41 23 AB CD\r\r"  # preset the response
	r = o.query(cmd, True)       # run
	assert toCar[0] == "0123"    # verify that the command was sent correctly
	assert r.raw_data == fromCar # verify that raw_data was stored in the Response
	assert r.value == "ABCD"     # verify that the response was parsed correctly

	fromCar = "NO DATA"
	r = o.query(cmd, True)
	assert r.raw_data == fromCar
	assert r.is_null()

	fromCar = "totaly not hex!@#$"
	r = o.query(cmd, True)
	assert r.raw_data == fromCar
	assert r.is_null()

	fromCar = ""
	r = o.query(cmd, True)
	assert r.raw_data == fromCar
	assert r.is_null()


def test_load_commands():
	pass
