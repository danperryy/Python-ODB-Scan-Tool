
import time
import pytest
from obd import commands, Unit


@pytest.fixture(scope="module")
def obd(request):
    """provides an OBD connection object for obdsim"""
    import obd
    port = request.config.getoption("--obdsim")

    # TODO: lookup how to fail inside of a fixture
    if port is None:
        print("Please run obdsim and use --obdsim=<port>")
        exit(1)

    return obd.OBD(port)


@pytest.fixture(scope="module")
def async(request):
    """provides an OBD *Async* connection object for obdsim"""
    import obd
    port = request.config.getoption("--obdsim")

    # TODO: lookup how to fail inside of a fixture
    if port is None:
        print("Please run obdsim and use --obdsim=<port>")
        exit(1)

    return obd.Async(port)


def good_rpm_response(r):
    return isinstance(r.value, float) and \
           r.value > 0.0 and \
           r.unit == Unit.RPM

def test_supports(obd):
    assert(len(obd.supported_commands) > 0)
    assert(obd.supports(commands.RPM))


def test_rpm(obd):
    r = obd.query(commands.RPM)
    assert(good_rpm_response(r))


def test_async_query(async):

    rs = []
    async.watch(commands.RPM)
    async.start()

    for i in range(5):
        time.sleep(0.05)
        rs.append(async.query(commands.RPM))

    async.stop()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([ good_rpm_response(r) for r in rs ]))


def test_async_callback(async):

    rs = []
    async.watch(commands.RPM, callback=rs.append)
    async.start()
    time.sleep(0.05)
    async.stop()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([ good_rpm_response(r) for r in rs ]))
