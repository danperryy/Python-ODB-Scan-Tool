
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


def test_rpm(obd):
    r = obd.query(commands.RPM)
    assert(isinstance(r.value, float))
    assert(r.unit == Unit.RPM)
