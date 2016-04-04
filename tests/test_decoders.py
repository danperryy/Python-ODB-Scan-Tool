
from binascii import unhexlify

from obd.OBDResponse import Unit
from obd.protocols.protocol import Frame, Message
import obd.decoders as d


# returns a list with a single valid message,
# containing the requested data
def m(hex_data, frames=[]):
    # most decoders don't look at the underlying frame objects
    message = Message(frames)
    message.data = bytearray(unhexlify(hex_data))
    return [message]


def float_equals(d1, d2):
    values_match = (abs(d1[0] - d2[0]) < 0.02)
    units_match   = (d1[1] == d2[1])
    return values_match and units_match





def test_noop():
    assert d.noop(m("00010203")) == (bytearray([0, 1, 2, 3]), Unit.NONE)

def test_drop():
    assert d.drop(m("deadbeef")) == (None, Unit.NONE)

def test_raw_string():
    assert d.raw_string([ Message([]) ]) == ("", Unit.NONE)
    assert d.raw_string([ Message([ Frame("NO DATA") ]) ]) == ("NO DATA", Unit.NONE)
    assert d.raw_string([ Message([ Frame("A"), Frame("B") ]) ]) == ("A\nB", Unit.NONE)
    assert d.raw_string([ Message([ Frame("A") ]), Message([ Frame("B") ]) ]) == ("A\nB", Unit.NONE)

def test_pid():
    assert d.pid(m("00000000")) == ("00000000000000000000000000000000", Unit.NONE)
    assert d.pid(m("F00AA00F")) == ("11110000000010101010000000001111", Unit.NONE)
    assert d.pid(m("11")) == ("00010001", Unit.NONE)

def test_count():
    assert d.count(m("00"))   == (0,    Unit.COUNT)
    assert d.count(m("0F"))   == (15,   Unit.COUNT)
    assert d.count(m("03E8")) == (1000, Unit.COUNT)

def test_percent():
    assert d.percent(m("00"))  == (0.0,   Unit.PERCENT)
    assert d.percent(m("FF"))  == (100.0, Unit.PERCENT)

def test_percent_centered():
    assert              d.percent_centered(m("00")) == (-100.0, Unit.PERCENT)
    assert              d.percent_centered(m("80")) == (0.0,    Unit.PERCENT)
    assert float_equals(d.percent_centered(m("FF")),   (99.2,   Unit.PERCENT))

def test_temp():
    assert d.temp(m("00"))   == (-40, Unit.C)
    assert d.temp(m("FF"))   == (215, Unit.C)
    assert d.temp(m("03E8")) == (960, Unit.C)

def test_catalyst_temp():
    assert d.catalyst_temp(m("0000")) == (-40.0,  Unit.C)
    assert d.catalyst_temp(m("FFFF")) == (6513.5, Unit.C)

def test_current_centered():
    assert              d.current_centered(m("00000000")) == (-128.0, Unit.MA)
    assert              d.current_centered(m("00008000")) == (0.0,    Unit.MA)
    assert float_equals(d.current_centered(m("0000FFFF")),   (128.0,  Unit.MA))
    assert              d.current_centered(m("ABCD8000")) == (0.0,    Unit.MA) # first 2 bytes are unused (should be disregarded)

def test_sensor_voltage():
    assert d.sensor_voltage(m("0000")) == (0.0,   Unit.VOLT)
    assert d.sensor_voltage(m("FFFF")) == (1.275, Unit.VOLT)

def test_sensor_voltage_big():
    assert              d.sensor_voltage_big(m("00000000")) == (0.0, Unit.VOLT)
    assert float_equals(d.sensor_voltage_big(m("00008000")),   (4.0, Unit.VOLT))
    assert              d.sensor_voltage_big(m("0000FFFF")) == (8.0, Unit.VOLT)
    assert              d.sensor_voltage_big(m("ABCD0000")) == (0.0, Unit.VOLT) # first 2 bytes are unused (should be disregarded)

def test_fuel_pressure():
    assert d.fuel_pressure(m("00")) == (0, Unit.KPA)
    assert d.fuel_pressure(m("80")) == (384, Unit.KPA)
    assert d.fuel_pressure(m("FF")) == (765, Unit.KPA)

def test_pressure():
    assert d.pressure(m("00")) == (0, Unit.KPA)
    assert d.pressure(m("00")) == (0, Unit.KPA)

def test_fuel_pres_vac():
    assert d.fuel_pres_vac(m("0000")) == (0.0,      Unit.KPA)
    assert d.fuel_pres_vac(m("FFFF")) == (5177.265, Unit.KPA)

def test_fuel_pres_direct():
    assert d.fuel_pres_direct(m("0000")) == (0,      Unit.KPA)
    assert d.fuel_pres_direct(m("FFFF")) == (655350, Unit.KPA)

def test_evap_pressure():
    pass # TODO
    #assert d.evap_pressure(m("0000")) == (0.0, Unit.PA)

def test_abs_evap_pressure():
    assert d.abs_evap_pressure(m("0000")) == (0,       Unit.KPA)
    assert d.abs_evap_pressure(m("FFFF")) == (327.675, Unit.KPA)

def test_evap_pressure_alt():
    assert d.evap_pressure_alt(m("0000")) == (-32767, Unit.PA) 
    assert d.evap_pressure_alt(m("7FFF")) == (0,      Unit.PA)
    assert d.evap_pressure_alt(m("FFFF")) == (32768,  Unit.PA)

def test_rpm():
    assert d.rpm(m("0000")) == (0.0,      Unit.RPM)
    assert d.rpm(m("FFFF")) == (16383.75, Unit.RPM)

def test_speed():
    assert d.speed(m("00")) == (0,   Unit.KPH)
    assert d.speed(m("FF")) == (255, Unit.KPH)

def test_timing_advance():
    assert d.timing_advance(m("00")) == (-64.0, Unit.DEGREES)
    assert d.timing_advance(m("FF")) == (63.5,  Unit.DEGREES)

def test_inject_timing():
    assert              d.inject_timing(m("0000")) == (-210, Unit.DEGREES)
    assert float_equals(d.inject_timing(m("FFFF")),   (302,  Unit.DEGREES))

def test_maf():
    assert d.maf(m("0000")) == (0.0,    Unit.GPS)
    assert d.maf(m("FFFF")) == (655.35, Unit.GPS)

def test_max_maf():
    assert d.max_maf(m("00000000")) == (0,    Unit.GPS)
    assert d.max_maf(m("FF000000")) == (2550, Unit.GPS)
    assert d.max_maf(m("00ABCDEF")) == (0,    Unit.GPS) # last 3 bytes are unused (should be disregarded)

def test_seconds():
    assert d.seconds(m("0000")) == (0,     Unit.SEC)
    assert d.seconds(m("FFFF")) == (65535, Unit.SEC)

def test_minutes():
    assert d.minutes(m("0000")) == (0,     Unit.MIN)
    assert d.minutes(m("FFFF")) == (65535, Unit.MIN)

def test_distance():
    assert d.distance(m("0000")) == (0,     Unit.KM)
    assert d.distance(m("FFFF")) == (65535, Unit.KM)

def test_fuel_rate():
    assert d.fuel_rate(m("0000")) == (0.0,     Unit.LPH)
    assert d.fuel_rate(m("FFFF")) == (3276.75, Unit.LPH)

def test_fuel_status():
    assert d.fuel_status(m("0100")) == ("Open loop due to insufficient engine temperature", Unit.NONE)
    assert d.fuel_status(m("0800")) == ("Open loop due to system failure",                  Unit.NONE)
    assert d.fuel_status(m("0300")) == (None,                                               Unit.NONE)

def test_air_status():
    assert d.air_status(m("01")) == ("Upstream",                          Unit.NONE)
    assert d.air_status(m("08")) == ("Pump commanded on for diagnostics", Unit.NONE)
    assert d.air_status(m("03")) == (None,                                Unit.NONE)

def test_elm_voltage():
    # these aren't parsed as standard hex messages, so manufacture our own
    assert d.elm_voltage([ Message([ Frame("12.875") ]) ]) == (12.875, Unit.VOLT)
    assert d.elm_voltage([ Message([ Frame("12") ]) ]) == (12, Unit.VOLT)
    assert d.elm_voltage([ Message([ Frame("12ABCD") ]) ]) == (None, Unit.NONE)

def test_dtc():
    assert d.dtc(m("0104")) == ([
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
    ], Unit.NONE)

    # multiple codes
    assert d.dtc(m("010480034123")) == ([
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
        ("C0123", "Unknown error code"),
    ], Unit.NONE)

    # invalid code lengths are dropped
    assert d.dtc(m("0104800341")) == ([
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
    ], Unit.NONE)

    # 0000 codes are dropped
    assert d.dtc(m("000001040000")) == ([
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
    ], Unit.NONE)

    # test multiple messages
    assert d.dtc(m("0104") + m("8003") + m("0000")) == ([
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
    ], Unit.NONE)
