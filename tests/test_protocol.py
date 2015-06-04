
import random
from obd.protocols import *
from obd.protocols.protocol import Frame, Message, ECU_Map


def test_ECU():
    # make sure none of the ECU ID values overlap
    tested = []

    # NOTE: does't include ECU.ALL
    for ecu in [ECU.UNKNOWN, ECU.ENGINE, ECU.TRANSMISSION]:
        assert (ECU.ALL & ecu) > 0, "ECU: %d is not included in ECU.ALL" % ecu

        for other_ecu in tested:
            assert (ecu & other_ecu) == 0, "ECU: %d has a conflicting bit with another ECU constant" %ecu

        tested.append(ecu)


def test_ECU_Map():

    # test simple default map
    e = ECU_Map({
        0 : 0,
        1 : 10,
        2 : 20
    })

    for tx_id in range(3):
        ecu = (tx_id * 10)
        assert e.resolve(tx_id) == ecu, "ECU_Map.resolve() failed"
        assert e.lookup(ecu) == tx_id,  "ECU_Map.lookup() failed"

    # test undefined tx_ids
    assert e.resolve(3) == ECU.UNKNOWN, "ECU_Map.resolve() did not return ECU.UNKNOWN for undefined tx_id"

    # test tx_id writting
    e.set(3, 30)
    assert e.resolve(3) == 30, "ECU_Map.set() failed after resolve()"
    assert e.lookup(30) == 3,  "ECU_Map.set() failed after lookup()"

    # test tx_id overwritting
    e.set(3, 300)
    assert e.resolve(3) == 300, "ECU_Map.set() failed after overwrite"
    assert e.lookup(300) == 3,  "ECU_Map.set() failed after overwrite"

    # test conflicting ECU ID values
    # no two tx_ids should resolve to the same ECU ID
    e.set(3, 0) # should cause tx_id 0 become ECU.UNKNOWN
    assert e.resolve(3) == 0, "ECU_Map.set() after conflicting overwrite"
    assert e.lookup(0) == 3,  "ECU_Map.set() after conflicting overwrite"
    assert e.resolve(0) == ECU.UNKNOWN


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
    assert p.ecu_map.lookup(ECU.ENGINE) == 0x10

    # use lone responses regardless
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA"])
    assert p.ecu_map.lookup(ECU.ENGINE) == 0x12

    # if primary ECU is not listed, use response with most PIDs supported
    p = SAE_J1850_PWM(["48 6B 12 41 00 BE 1F B8 11 AA", "48 6B 14 41 00 00 00 B8 11 AA"])
    assert p.ecu_map.lookup(ECU.ENGINE) == 0x12

    # if no messages were received, the defaults stay in place
    p = SAE_J1850_PWM([])
    assert p.ecu_map.lookup(ECU.ENGINE) == p.TX_ID_ENGINE


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
