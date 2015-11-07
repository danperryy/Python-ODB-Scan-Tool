
import obd
from obd.utils import OBDStatus
from obd.OBDResponse import OBDResponse
from obd.OBDCommand import OBDCommand
from obd.decoders import noop
from obd.protocols import SAE_J1850_PWM


def test_is_connected():
	o = obd.OBD("/dev/null")
	assert not o.is_connected()

	# todo

"""
# TODO: rewrite for new protocol architecture
def test_query():
	# we don't need an actual serial connection
	o = obd.OBD("/dev/null")
	# forge our own command, to control the output
	cmd = OBDCommand("TEST", "Test command", "0123", 2, noop, False)

	# forge IO from the car by overwriting the read/write functions
	
	# buffers
	toCar = [""] # needs to be inside mutable object to allow assignment in closure
	fromCar = ""

	def write(cmd):
		toCar[0] = cmd

	o.is_connected              = lambda *args: True
	o.port.is_connected         = lambda *args: True
	o.port._ELM327__status      = OBDStatus.CAR_CONNECTED
	o.port._ELM327__protocol    = SAE_J1850_PWM([])
	o.port._ELM327__primary_ecu = 0x10
	o.port._ELM327__write       = write
	o.port._ELM327__read        = lambda *args: fromCar

	# make sure unsupported commands don't write ------------------------------
	fromCar = ["48 6B 10 41 23 AB CD 10"]
	r = o.query(cmd)
	assert toCar[0] == ""
	assert r.is_null()

	# a correct command transaction -------------------------------------------
	fromCar = ["48 6B 10 41 23 AB CD 10"]  # preset the response
	r = o.query(cmd, force=True) # run
	assert toCar[0] == "0123"    # verify that the command was sent correctly
	assert not r.is_null()
	assert r.value == "ABCD"     # verify that the response was parsed correctly

	# response of greater length ----------------------------------------------
	fromCar = ["48 6B 10 41 23 AB CD EF 10"]
	r = o.query(cmd, force=True)
	assert toCar[0] == "0123"
	assert r.value == "ABCD"

	# response of lesser length -----------------------------------------------
	fromCar = ["48 6B 10 41 23 AB 10"]
	r = o.query(cmd, force=True)
	assert toCar[0] == "0123"
	assert r.value == "AB00"

	# NO DATA response --------------------------------------------------------
	fromCar = ["NO DATA"]
	r = o.query(cmd, force=True)
	assert r.is_null()

	# malformed response ------------------------------------------------------
	fromCar = ["totaly not hex!@#$"]
	r = o.query(cmd, force=True)
	assert r.is_null()

	# no response -------------------------------------------------------------
	fromCar = [""]
	r = o.query(cmd, force=True)
	assert r.is_null()

	# reject responses from other ECUs  ---------------------------------------
	fromCar = ["48 6B 12 41 23 AB CD 10"]
	r = o.query(cmd, force=True)
	assert toCar[0] == "0123"
	assert r.is_null()

	# filter for primary ECU --------------------------------------------------
	fromCar = ["48 6B 12 41 23 AB CD 10", "48 6B 10 41 23 AB CD 10"]
	r = o.query(cmd, force=True)
	assert toCar[0] == "0123"
	assert r.value == "ABCD"

	'''
	# ignore multiline responses ----------------------------------------------
	fromCar = ["48 6B 10 41 23 AB CD 10", "48 6B 10 41 23 AB CD 10"]
	r = o.query(cmd, force=True)
	assert toCar[0] == "0123"
	assert r.is_null()
	'''
"""

def test_load_commands():
	pass
