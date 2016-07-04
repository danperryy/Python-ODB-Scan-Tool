
import time
import pytest
from obd import commands, Unit

STANDARD_WAIT_TIME = 0.2


@pytest.fixture(scope="module")
def obd(request):
    """provides an OBD connection object for obdsim"""
    import obd
    port = request.config.getoption("--port")
    return obd.OBD(port)


@pytest.fixture(scope="module")
def async(request):
    """provides an OBD *Async* connection object for obdsim"""
    import obd
    port = request.config.getoption("--port")
    return obd.Async(port)


def good_rpm_response(r):
    return (not r.is_null()) and \
           (r.value.u == Unit.rpm) and \
           (r.value >= 0.0 * Unit.rpm)


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_supports(obd):
    assert(len(obd.supported_commands) > 0)
    assert(obd.supports(commands.RPM))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_rpm(obd):
    r = obd.query(commands.RPM)
    assert(good_rpm_response(r))


# Async tests

@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_query(async):

    rs = []
    async.watch(commands.RPM)
    async.start()

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        rs.append(async.query(commands.RPM))

    async.stop()
    async.unwatch_all()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([ good_rpm_response(r) for r in rs ]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_callback(async):

    rs = []
    async.watch(commands.RPM, callback=rs.append)
    async.start()
    time.sleep(STANDARD_WAIT_TIME)
    async.stop()
    async.unwatch_all()

    # make sure we got data
    assert(len(rs) > 0)
    assert(all([ good_rpm_response(r) for r in rs ]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_paused(async):

    assert(not async.running)
    async.watch(commands.RPM)
    async.start()
    assert(async.running)

    with async.paused() as was_running:
        assert(not async.running)
        assert(was_running)

    assert(async.running)
    async.stop()
    assert(not async.running)


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_unwatch(async):

    watched_rs = []
    unwatched_rs = []

    async.watch(commands.RPM)
    async.start()

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        watched_rs.append(async.query(commands.RPM))

    with async.paused():
        async.unwatch(commands.RPM)

    for i in range(5):
        time.sleep(STANDARD_WAIT_TIME)
        unwatched_rs.append(async.query(commands.RPM))

    async.stop()

    # the watched commands
    assert(len(watched_rs) > 0)
    assert(all([ good_rpm_response(r) for r in watched_rs ]))

    # the unwatched commands
    assert(len(unwatched_rs) > 0)
    assert(all([ r.is_null() for r in unwatched_rs ]))


@pytest.mark.skipif(not pytest.config.getoption("--port"),
                    reason="needs --port=<port> to run")
def test_async_unwatch_callback(async):

    a_rs = []
    b_rs = []
    async.watch(commands.RPM, callback=a_rs.append)
    async.watch(commands.RPM, callback=b_rs.append)

    async.start()
    time.sleep(STANDARD_WAIT_TIME)

    with async.paused():
        async.unwatch(commands.RPM, callback=b_rs.append)

    time.sleep(STANDARD_WAIT_TIME)
    async.stop()
    async.unwatch_all()

    assert(all([ good_rpm_response(r) for r in a_rs + b_rs ]))
    assert(len(a_rs) > len(b_rs))
