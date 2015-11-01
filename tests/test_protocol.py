
import random
from obd.protocols import *
from obd.protocols.protocol import Frame, Message


def test_ECU():
    # make sure none of the ECU ID values overlap
    tested = []

    # NOTE: does't include ECU.ALL
    for ecu in [ECU.UNKNOWN, ECU.ENGINE, ECU.TRANSMISSION]:
        assert (ECU.ALL & ecu) > 0, "ECU: %d is not included in ECU.ALL" % ecu

        for other_ecu in tested:
            assert (ecu & other_ecu) == 0, "ECU: %d has a conflicting bit with another ECU constant" %ecu

        tested.append(ecu)


def test_frame():
    # constructor
    f = Frame("asdf")
    assert f.raw == "asdf", "Frame failed to accept raw data as __init__ argument"
    assert f.priority  == None
    assert f.addr_mode == None
    assert f.rx_id     == None
    assert f.tx_id     == None
    assert f.type      == None
    assert f.seq_index == 0
    assert f.data_len  == None


def test_message():

    # constructor
    f = Frame("")
    f.tx_id = 42
    R = ["asdf"]
    F = [f]
    m = Message(R, F)

    assert m.raw == R
    assert m.frames == F
    assert m.tx_id == 42
    assert m.ecu == ECU.UNKNOWN


def test_populate_ecu_map():
    # parse from messages

    # use primary ECU when multiple are present
    p = SAE_J1850_PWM(["48 6B 10 41 00 BE 1F B8 11 AA", "48 6B 12 41 00 BE 1F B8 11 AA"])
    assert p.ecu_map[0x10] == ECU.ENGINE

    # use lone responses regardless
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA"])
    assert p.ecu_map[0x12] == ECU.ENGINE

    # if primary ECU is not listed, use response with most PIDs supported
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA", "48 6B 14 41 00 00 00 B8 11 AA"])
    assert p.ecu_map[0x12] == ECU.ENGINE

    # if no messages were received, then the map is empty
    p = SAE_J1850_PWM([])
    assert len(p.ecu_map) == 0


def test_call_filtering():

    # test the basic frame construction
    p = UnknownProtocol([])

    f1 = "48 6B 12 41 00 BE 1F B8 11 AA"
    f2 = "48 6B 14 41 00 00 00 B8 11 AA"
    raw = [f1, f2]
    m = p(raw)
    assert len(m) == 1
    assert len(m[0].frames) == 2
    assert m[0].raw == raw
    assert m[0].frames[0].raw == f1.replace(' ', '')
    assert m[0].frames[1].raw == f2.replace(' ', '')


    # test invalid hex dropping
    p = UnknownProtocol([])

    raw = ["not hex", f2]
    m = p(raw)
    assert len(m) == 1
    assert len(m[0].frames) == 1
    assert m[0].raw == raw
    assert m[0].frames[0].raw == f2.replace(' ', '')
