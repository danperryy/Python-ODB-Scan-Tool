
from obd.utils import Unit
import obd.decoders as d


def test_count():
	assert d.count("0")   == (0,    Unit.COUNT)
	assert d.count("F")   == (15,   Unit.COUNT)
	assert d.count("3E8") == (1000, Unit.COUNT)

def test_percent():
	assert d.percent("00")  == (0.0,   Unit.PERCENT)
	assert d.percent("FF")  == (100.0, Unit.PERCENT)

def test_percent_centered():
	assert d.percent_centered("00")   == (-100.0, Unit.PERCENT)
	assert d.percent_centered("80")   == (0.0,    Unit.PERCENT)
	#assert d.percent_centered("FF")   == (100.0,  Unit.PERCENT) # returns 99.21875, need float checking or better math

def test_temp():
	assert d.temp("00")  == (-40, Unit.C)
	assert d.temp("FF")  == (215, Unit.C)
	assert d.temp("3E8") == (960, Unit.C)

def test_catalyst_temp():
	assert d.catalyst_temp("0000") == (-40.0,  Unit.C)
	assert d.catalyst_temp("FFFF") == (6513.5, Unit.C)

def test_current_centered():
	assert d.current_centered("00000000") == (-128.0, Unit.MA)
	assert d.current_centered("00008000") == (0.0,    Unit.MA)
	#assert d.current_centered("0000FFFF") == (128.0,  Unit.MA) # returns 127.99609375, need float checking or better math
	assert d.current_centered("ABCD8000") == (0.0,    Unit.MA) # first 2 bytes are unused (should be disregarded)

def test_sensor_voltage():
	assert d.sensor_voltage("0000") == (0.0,   Unit.VOLT)
	assert d.sensor_voltage("FFFF") == (1.275, Unit.VOLT)

def test_sensor_voltage_big():
	assert d.sensor_voltage_big("00000000") == (0.0, Unit.VOLT)
	#assert d.sensor_voltage_big("00008000") == (4.0, Unit.VOLT) # returns 127.99609375, need float checking or better math
	assert d.sensor_voltage_big("0000FFFF") == (8.0, Unit.VOLT)
	assert d.sensor_voltage_big("ABCD0000") == (0.0, Unit.VOLT) # first 2 bytes are unused (should be disregarded)

def test_fuel_pressure():
	assert d.fuel_pressure("00") == (0, Unit.KPA)
	assert d.fuel_pressure("80") == (384, Unit.KPA)
	assert d.fuel_pressure("FF") == (765, Unit.KPA)

def test_pressure():
	assert d.pressure("00") == (0, Unit.KPA)
	assert d.pressure("00") == (0, Unit.KPA)

def test_fuel_pres_vac():
	assert d.fuel_pres_vac("0000") == (0.0,      Unit.KPA)
	assert d.fuel_pres_vac("FFFF") == (5177.265, Unit.KPA)

def test_fuel_pres_direct():
	assert d.fuel_pres_direct("0000") == (0,      Unit.KPA)
	assert d.fuel_pres_direct("FFFF") == (655350, Unit.KPA)

def test_evap_pressure():
	pass
	#assert d.evap_pressure("0000") == (0.0, Unit.PA)

def test_abs_evap_pressure():
	assert d.abs_evap_pressure("0000") == (0,   Unit.KPA)
	assert d.abs_evap_pressure("FFFF") == (327, Unit.KPA)

def test_evap_pressure_alt():
	assert d.evap_pressure_alt("0000") == (-32767, Unit.PA)	
	assert d.evap_pressure_alt("7FFF") == (0,      Unit.PA)
	assert d.evap_pressure_alt("FFFF") == (32768,  Unit.PA)

def test_rpm():
	assert d.rpm("0000") == (0.0,      Unit.RPM)
	assert d.rpm("FFFF") == (16383.75, Unit.RPM)

def test_speed():
	assert d.speed("00") == (0,   Unit.KPH)
	assert d.speed("FF") == (255, Unit.KPH)

def test_timing_advance():
	assert d.timing_advance("00") == (-64.0, Unit.DEGREES)
	assert d.timing_advance("FF") == (63.5,  Unit.DEGREES)

def test_inject_timing():
	assert d.inject_timing("0000") == (-210, Unit.DEGREES)
	#assert d.inject_timing("FFFF") == (301,  Unit.DEGREES)

def test_maf():
	assert d.maf("0000") == (0.0,    Unit.GPS)
	assert d.maf("FFFF") == (655.35, Unit.GPS)

def test_max_maf():
	assert d.max_maf("00000000") == (0,    Unit.GPS)
	assert d.max_maf("FF000000") == (2550, Unit.GPS)
	assert d.max_maf("00ABCDEF") == (0,    Unit.GPS) # last 3 bytes are unused (should be disregarded)

def test_seconds():
	assert d.seconds("0000") == (0,     Unit.SEC)
	assert d.seconds("FFFF") == (65535, Unit.SEC)

def test_minutes():
	assert d.minutes("0000") == (0,     Unit.MIN)
	assert d.minutes("FFFF") == (65535, Unit.MIN)

def test_distance():
	assert d.distance("0000") == (0,     Unit.KM)
	assert d.distance("FFFF") == (65535, Unit.KM)

def test_fuel_rate():
	assert d.fuel_rate("0000") == (0.0,     Unit.LPH)
	assert d.fuel_rate("FFFF") == (3276.75, Unit.LPH)
