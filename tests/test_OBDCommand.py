
from obd.OBDCommand import OBDCommand
from obd.OBDResponse import Unit
from obd.decoders import noop
from obd.protocols import *



def test_constructor():

    # default constructor
    #                 name       description        cmd  bytes decoder ECU
    cmd = OBDCommand("Test", "example OBD command", "0123", 2, noop, ECU.ENGINE)
    assert cmd.name      == "Test"
    assert cmd.desc      == "example OBD command"
    assert cmd.command   == "0123"
    assert cmd.bytes     == 2
    assert cmd.decode    == noop
    assert cmd.ecu       == ECU.ENGINE
    assert cmd.fast      == False

    assert cmd.mode_int == 1
    assert cmd.pid_int  == 35

    # a case where "fast", and "supported" were set explicitly
    #                 name       description        cmd  bytes decoder ECU         fast
    cmd = OBDCommand("Test 2", "example OBD command", "0123", 2, noop, ECU.ENGINE, True)
    assert cmd.fast      == True



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
    assert cmd.fast      == cmd.fast



def test_call():
    p = SAE_J1850_PWM(["48 6B 10 41 00 FF FF FF FF AA"]) # train the ecu_map to identify the engine
    messages = p(["48 6B 10 41 00 BE 1F B8 11 AA"]) # parse valid data into response object 

    print(messages[0].data)

    # valid response size
    cmd = OBDCommand("", "", "0123", 4, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == b'\xBE\x1F\xB8\x11'

    # response too short (pad)
    cmd = OBDCommand("", "", "0123", 5, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == b'\xBE\x1F\xB8\x11\x00'

    # response too long (clip)
    cmd = OBDCommand("", "", "0123", 3, noop, ECU.ENGINE)
    r = cmd(messages)
    assert r.value == b'\xBE\x1F\xB8'



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
