
import random
from obd.protocols import *
from obd.protocols.protocol import Message, ECU_Map


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

