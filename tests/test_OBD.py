
"""
    Tests for the API layer
"""

import obd
from obd import Unit
from obd import ECU
from obd.protocols.protocol import Message
from obd.utils import OBDStatus
from obd.OBDCommand import OBDCommand
from obd.decoders import noop



class FakeELM:
    """
        Fake ELM327 driver class for intercepting the commands from the API
    """

    def __init__(self, portname, baudrate, protocol):
        self.portname = portname
        self.baudrate = baudrate
        self.protocol = protocol
        self._status = OBDStatus.CAR_CONNECTED
        self.last_command = None

    def port_name(self):
        return self.portname

    def status(self):
        return self._status

    def ecus(self):
        return [ ECU.ENGINE, ECU.UNKNOWN ]

    def protocol_name(self):
        return "ISO 15765-4 (CAN 11/500)"

    def protocol_id(self):
        return "6"

    def close(self):
        pass

    def send_and_parse(self, cmd):
        # stow this, so we can check that the API made the right request
        print(cmd)
        self.last_command = cmd

        # all commands succeed
        message = Message([])
        message.data = b'response data'
        message.ecu = ECU.ENGINE # picked engine so that simple commands like RPM will work
        return [ message ]

    def _test_last_command(self, expected):
        r = self.last_command == expected
        print(self.last_command)
        self.last_command = None
        return r


# a toy command to test with
command = OBDCommand("Test_Command", \
                     "A test command", \
                     "0123456789ABCDEF", \
                     0, \
                     noop, \
                     ECU.ALL, \
                     True, \
                     True)





def test_is_connected():
    o = obd.OBD("/dev/null")
    assert not o.is_connected()

    # our fake ELM class always returns success for connections
    o.port = FakeELM("/dev/null", 34800, None)
    assert o.is_connected()


def test_status():
    """
        Make sure that the API's status() functions reports the
        same values as the underlying ELM327 class.
    """
    o = obd.OBD("/dev/null")
    assert o.status() == OBDStatus.NOT_CONNECTED

    # we can manually set our fake ELM class to test
    # the other values
    o.port = FakeELM("/dev/null", 34800, None)

    o.port._status = OBDStatus.ELM_CONNECTED
    assert o.status() == OBDStatus.ELM_CONNECTED

    o.port._status = OBDStatus.CAR_CONNECTED
    assert o.status() == OBDStatus.CAR_CONNECTED


def test_supports():
    o = obd.OBD("/dev/null")

    # since we haven't actually connected,
    # no commands should be marked as supported
    assert not o.supports(obd.commands.RPM)
    obd.commands.RPM.supported = True
    assert o.supports(obd.commands.RPM)

    # commands that aren't in python-OBD's tables are unsupported by default
    assert not o.supports(command)


def test_force():
    o = obd.OBD("/dev/null", fast=False) # disable the trailing response count byte
    o.port = FakeELM("/dev/null", 34800, None)

    # a command marked as unsupported
    obd.commands.RPM.supported = False

    r = o.query(obd.commands.RPM)
    assert r.is_null()
    assert o.port._test_last_command(None)

    r = o.query(obd.commands.RPM, force=True)
    assert not r.is_null()
    assert o.port._test_last_command(obd.commands.RPM.command)

    # a command that isn't in python-OBD's tables
    r = o.query(command)
    assert r.is_null()
    assert o.port._test_last_command(None)

    r = o.query(command, force=True)
    assert o.port._test_last_command(command.command)



def test_fast():
    o = obd.OBD("/dev/null", fast=False)
    o.port = FakeELM("/dev/null", 34800, None)
    

    assert command.fast
    o.query(command, force=True) # force since this command isn't in the tables
    # assert o.port._test_last_command(command.command)







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
