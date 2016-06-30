
from binascii import unhexlify

from obd.UnitsAndScaling import Unit
from obd.protocols.protocol import Frame, Message
from obd.codes import TEST_IDS
import obd.decoders as d


# returns a list with a single valid message,
# containing the requested data
def m(hex_data, frames=[]):
    # most decoders don't look at the underlying frame objects
    message = Message(frames)
    message.data = bytearray(unhexlify(hex_data))
    return [message]


FLOAT_EQUALS_TOLERANCE = 0.025

# comparison for pint floating point values
def float_equals(va, vb):
    units_match = (va.u == vb.u)
    values_match = (abs(va.magnitude - vb.magnitude) < FLOAT_EQUALS_TOLERANCE)
    return values_match and units_match





def test_noop():
    assert d.noop(m("00010203")) == bytearray([0, 1, 2, 3])

def test_drop():
    assert d.drop(m("deadbeef")) == None

def test_raw_string():
    assert d.raw_string([ Message([]) ]) == ""
    assert d.raw_string([ Message([ Frame("NO DATA") ]) ]) == "NO DATA"
    assert d.raw_string([ Message([ Frame("A"), Frame("B") ]) ]) == "A\nB"
    assert d.raw_string([ Message([ Frame("A") ]), Message([ Frame("B") ]) ]) == "A\nB"

def test_pid():
    assert d.pid(m("00000000")) == "00000000000000000000000000000000"
    assert d.pid(m("F00AA00F")) == "11110000000010101010000000001111"
    assert d.pid(m("11")) == "00010001"

def test_count():
    assert d.count(m("00"))   == 0 * Unit.count
    assert d.count(m("0F"))   == 15 * Unit.count
    assert d.count(m("03E8")) == 1000 * Unit.count

def test_percent():
    assert d.percent(m("00"))  == 0.0 * Unit.percent
    assert d.percent(m("FF"))  == 100.0 * Unit.percent

def test_percent_centered():
    assert              d.percent_centered(m("00")) == -100.0 * Unit.percent
    assert              d.percent_centered(m("80")) == 0.0 * Unit.percent
    assert float_equals(d.percent_centered(m("FF")), 99.2 * Unit.percent)

def test_temp():
    assert d.temp(m("00"))   == Unit.Quantity(-40, Unit.celsius)
    assert d.temp(m("FF"))   == Unit.Quantity(215, Unit.celsius)
    assert d.temp(m("03E8")) == Unit.Quantity(960, Unit.celsius)

def test_catalyst_temp():
    assert d.catalyst_temp(m("0000")) == Unit.Quantity(-40.0, Unit.celsius)
    assert d.catalyst_temp(m("FFFF")) == Unit.Quantity(6513.5, Unit.celsius)

def test_current_centered():
    assert              d.current_centered(m("00000000")) == -128.0 * Unit.milliampere
    assert              d.current_centered(m("00008000")) == 0.0 * Unit.milliampere
    assert              d.current_centered(m("ABCD8000")) == 0.0 * Unit.milliampere # first 2 bytes are unused (should be disregarded)
    assert float_equals(d.current_centered(m("0000FFFF")), 128.0 * Unit.milliampere)

def test_sensor_voltage():
    assert d.sensor_voltage(m("0000")) == 0.0 * Unit.volt
    assert d.sensor_voltage(m("FFFF")) == 1.275 * Unit.volt

def test_sensor_voltage_big():
    assert              d.sensor_voltage_big(m("00000000")) == 0.0 * Unit.volt
    assert float_equals(d.sensor_voltage_big(m("00008000")),   4.0 * Unit.volt)
    assert              d.sensor_voltage_big(m("0000FFFF")) == 8.0 * Unit.volt
    assert              d.sensor_voltage_big(m("ABCD0000")) == 0.0 * Unit.volt # first 2 bytes are unused (should be disregarded)

def test_fuel_pressure():
    assert d.fuel_pressure(m("00")) == 0 * Unit.kilopascal
    assert d.fuel_pressure(m("80")) == 384 * Unit.kilopascal
    assert d.fuel_pressure(m("FF")) == 765 * Unit.kilopascal

def test_pressure():
    assert d.pressure(m("00")) == 0 * Unit.kilopascal
    assert d.pressure(m("00")) == 0 * Unit.kilopascal

def test_fuel_pres_vac():
    assert d.fuel_pres_vac(m("0000")) == 0.0 * Unit.kilopascal
    assert d.fuel_pres_vac(m("FFFF")) == 5177.265 * Unit.kilopascal

def test_fuel_pres_direct():
    assert d.fuel_pres_direct(m("0000")) == 0 * Unit.kilopascal
    assert d.fuel_pres_direct(m("FFFF")) == 655350 * Unit.kilopascal

def test_evap_pressure():
    pass # TODO
    #assert d.evap_pressure(m("0000")) == 0.0 * Unit.PA)

def test_abs_evap_pressure():
    assert d.abs_evap_pressure(m("0000")) == 0 * Unit.kilopascal
    assert d.abs_evap_pressure(m("FFFF")) == 327.675 * Unit.kilopascal

def test_evap_pressure_alt():
    assert d.evap_pressure_alt(m("0000")) == -32767 * Unit.pascal
    assert d.evap_pressure_alt(m("7FFF")) == 0 * Unit.pascal
    assert d.evap_pressure_alt(m("FFFF")) == 32768 *  Unit.pascal

def test_rpm():
    assert d.rpm(m("0000")) == 0.0 * Unit.rpm
    assert d.rpm(m("FFFF")) == 16383.75 * Unit.rpm

def test_speed():
    assert d.speed(m("00")) == 0 * Unit.kph
    assert d.speed(m("FF")) == 255 * Unit.kph

def test_timing_advance():
    assert d.timing_advance(m("00")) == -64.0 * Unit.degrees
    assert d.timing_advance(m("FF")) == 63.5 *  Unit.degrees

def test_inject_timing():
    assert              d.inject_timing(m("0000")) == -210 * Unit.degrees
    assert float_equals(d.inject_timing(m("FFFF")),   302 * Unit.degrees)

def test_maf():
    assert d.maf(m("0000")) == 0.0 * Unit.grams_per_second
    assert d.maf(m("FFFF")) == 655.35 * Unit.grams_per_second

def test_max_maf():
    assert d.max_maf(m("00000000")) == 0 * Unit.grams_per_second
    assert d.max_maf(m("FF000000")) == 2550 * Unit.grams_per_second
    assert d.max_maf(m("00ABCDEF")) == 0 * Unit.grams_per_second # last 3 bytes are unused (should be disregarded)

def test_seconds():
    assert d.seconds(m("0000")) == 0 * Unit.second
    assert d.seconds(m("FFFF")) == 65535 * Unit.second

def test_minutes():
    assert d.minutes(m("0000")) == 0 * Unit.minute
    assert d.minutes(m("FFFF")) == 65535 * Unit.minute

def test_distance():
    assert d.distance(m("0000")) == 0 * Unit.kilometer
    assert d.distance(m("FFFF")) == 65535 * Unit.kilometer

def test_fuel_rate():
    assert d.fuel_rate(m("0000")) == 0.0 * Unit.liters_per_hour
    assert d.fuel_rate(m("FFFF")) == 3276.75 * Unit.liters_per_hour

def test_fuel_status():
    assert d.fuel_status(m("0100")) == "Open loop due to insufficient engine temperature"
    assert d.fuel_status(m("0800")) == "Open loop due to system failure"
    assert d.fuel_status(m("0300")) == None

def test_air_status():
    assert d.air_status(m("01")) == "Upstream"
    assert d.air_status(m("08")) == "Pump commanded on for diagnostics"
    assert d.air_status(m("03")) == None

def test_elm_voltage():
    # these aren't parsed as standard hex messages, so manufacture our own
    assert d.elm_voltage([ Message([ Frame("12.875") ]) ]) == 12.875 * Unit.volt
    assert d.elm_voltage([ Message([ Frame("12") ]) ]) == 12 * Unit.volt
    assert d.elm_voltage([ Message([ Frame("12ABCD") ]) ]) == None

def test_dtc():
    assert d.dtc(m("0104")) == [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
    ]

    # multiple codes
    assert d.dtc(m("010480034123")) == [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
        ("C0123", "Unknown error code"),
    ]

    # invalid code lengths are dropped
    assert d.dtc(m("0104800341")) == [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
    ]

    # 0000 codes are dropped
    assert d.dtc(m("000001040000")) == [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
    ]

    # test multiple messages
    assert d.dtc(m("0104") + m("8003") + m("0000")) == [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", "Unknown error code"),
    ]

def test_monitor():
    # single test -----------------------------------------
    #                [      test      ]
    v = d.monitor(m("01010A0BB00BB00BB0"))
    assert len(v) == 1 # 1 test result

    # make sure we can look things up by name and TID
    assert v[0x01] == v.rtl_threshold_voltage

    # make sure we got information
    assert not v[0x01].is_null()

    assert float_equals(v[0x01].value, 365 * Unit.millivolt)
    assert float_equals(v[0x01].min,   365 * Unit.millivolt)
    assert float_equals(v[0x01].max,   365 * Unit.millivolt)

    # multiple tests --------------------------------------
    #                [      test      ][      test      ][      test      ]
    v = d.monitor(m("01010A0BB00BB00BB00105100048000000640185240096004BFFFF"))
    assert len(v) == 3 # 3 test results

    # make sure we can look things up by name and TID
    assert v[0x01] == v.rtl_threshold_voltage
    assert v[0x05] == v.rtl_switch_time

    # make sure we got information
    assert not v[0x01].is_null()
    assert not v[0x05].is_null()
    assert not v[0x85].is_null()

    assert float_equals(v[0x01].value, 365 * Unit.millivolt)
    assert float_equals(v[0x01].min,   365 * Unit.millivolt)
    assert float_equals(v[0x01].max,   365 * Unit.millivolt)

    assert float_equals(v[0x05].value, 72 * Unit.millisecond)
    assert float_equals(v[0x05].min,   0 * Unit.millisecond)
    assert float_equals(v[0x05].max,   100 * Unit.millisecond)

    assert float_equals(v[0x85].value, 150 * Unit.count)
    assert float_equals(v[0x85].min,   75 * Unit.count)
    assert float_equals(v[0x85].max,   65535 * Unit.count)

    # truncate incomplete tests ----------------------------
    #                [      test      ][junk]
    v = d.monitor(m("01010A0BB00BB00BB0ABCDEF"))
    assert len(v) == 1 # 1 test result

    # make sure we can look things up by name and TID
    assert v[0x01] == v.rtl_threshold_voltage

    # make sure we got information
    assert not v[0x01].is_null()

    assert float_equals(v[0x01].value, 365 * Unit.millivolt)
    assert float_equals(v[0x01].min,   365 * Unit.millivolt)
    assert float_equals(v[0x01].max,   365 * Unit.millivolt)

    # truncate incomplete tests ----------------------------
    v = d.monitor(m("01010A0BB00BB00B"))
    assert len(v) == 0 # no valid tests

    # make sure that the standard tests are null
    for tid in TEST_IDS:
        name = TEST_IDS[tid][0]
        assert v[tid].is_null()
