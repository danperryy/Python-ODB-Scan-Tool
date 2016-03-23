
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
#                                                                      #
########################################################################
#                                                                      #
# decoders.py                                                          #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

import math
from .utils import *
from .codes import *
from .debug import debug
from .OBDResponse import Unit, Status, Test

'''
All decoders take the form:

def <name>(<list_of_messages>):
    ...
    return (<value>, <unit>)

'''


# drop all messages, return None
def drop(messages):
    return (None, Unit.NONE)


# data in, data out
def noop(messages):
    return (messages[0].data, Unit.NONE)


# hex in, bitstring out
def pid(messages):
    d = messages[0].data
    v = bytes_to_bits(d)
    return (v, Unit.NONE)

# returns the raw strings from the ELM
def raw_string(messages):
    return ("\n".join([m.raw() for m in messages]), Unit.NONE)

'''
Sensor decoders
Return Value object with value and units
'''

def count(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    return (v, Unit.COUNT)

# 0 to 100 %
def percent(messages):
    d = messages[0].data
    v = d[0]
    v = v * 100.0 / 255.0
    return (v, Unit.PERCENT)

# -100 to 100 %
def percent_centered(messages):
    d = messages[0].data
    v = d[0]
    v = (v - 128) * 100.0 / 128.0
    return (v, Unit.PERCENT)

# -40 to 215 C
def temp(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v - 40
    return (v, Unit.C)

# -40 to 6513.5 C
def catalyst_temp(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = (v / 10.0) - 40
    return (v, Unit.C)

# -128 to 128 mA
def current_centered(messages):
    d = messages[0].data
    v = bytes_to_int(d[2:4])
    v = (v / 256.0) - 128
    return (v, Unit.MA)

# 0 to 1.275 volts
def sensor_voltage(messages):
    d = messages[0].data
    v = d[0]
    v = v / 200.0
    return (v, Unit.VOLT)

# 0 to 8 volts
def sensor_voltage_big(messages):
    d = messages[0].data
    v = bytes_to_int(d[2:4])
    v = (v * 8.0) / 65535
    return (v, Unit.VOLT)

# 0 to 765 kPa
def fuel_pressure(messages):
    d = messages[0].data
    v = d[0]
    v = v * 3
    return (v, Unit.KPA)

# 0 to 255 kPa
def pressure(messages):
    d = messages[0].data
    v = d[0]
    return (v, Unit.KPA)

# 0 to 5177 kPa
def fuel_pres_vac(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v * 0.079
    return (v, Unit.KPA)

# 0 to 655,350 kPa
def fuel_pres_direct(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v * 10
    return (v, Unit.KPA)

# -8192 to 8192 Pa
def evap_pressure(messages):
    # decode the twos complement
    d = messages[0].data
    a = twos_comp(unhex(d[0]), 8)
    b = twos_comp(unhex(d[1]), 8)
    v = ((a * 256.0) + b) / 4.0
    return (v, Unit.PA)

# 0 to 327.675 kPa
def abs_evap_pressure(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v / 200.0
    return (v, Unit.KPA)

# -32767 to 32768 Pa
def evap_pressure_alt(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v - 32767
    return (v, Unit.PA)

# 0 to 16,383.75 RPM
def rpm(messages):
    d = messages[0].data
    v = bytes_to_int(d) / 4.0
    return (v, Unit.RPM)

# 0 to 255 KPH
def speed(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    return (v, Unit.KPH)

# -64 to 63.5 degrees
def timing_advance(messages):
    d = messages[0].data
    v = d[0]
    v = (v - 128) / 2.0
    return (v, Unit.DEGREES)

# -210 to 301 degrees
def inject_timing(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = (v - 26880) / 128.0
    return (v, Unit.DEGREES)

# 0 to 655.35 grams/sec
def maf(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v / 100.0
    return (v, Unit.GPS)

# 0 to 2550 grams/sec
def max_maf(messages):
    d = messages[0].data
    v = d[0]
    v = v * 10
    return (v, Unit.GPS)

# 0 to 65535 seconds
def seconds(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    return (v, Unit.SEC)

# 0 to 65535 minutes
def minutes(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    return (v, Unit.MIN)

# 0 to 65535 km
def distance(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    return (v, Unit.KM)

# 0 to 3212 Liters/hour
def fuel_rate(messages):
    d = messages[0].data
    v = bytes_to_int(d)
    v = v * 0.05
    return (v, Unit.LPH)


def elm_voltage(messages):
    # doesn't register as a normal OBD response,
    # so access the raw frame data
    v = messages[0].frames[0].raw

    try:
        return (float(v), Unit.VOLT)
    except ValueError:
        debug("Failed to parse ELM voltage", True)
        return (None, Unit.NONE)


'''
Special decoders
Return objects, lists, etc
'''



def status(messages):
    d = messages[0].data
    bits = bytes_to_bits(d)

    output = Status()
    output.MIL           = bitToBool(bits[0])
    output.DTC_count     = unbin(bits[1:8])
    output.ignition_type = IGNITION_TYPE[unbin(bits[12])]

    output.tests.append(Test("Misfire", \
                             bitToBool(bits[15]), \
                             bitToBool(bits[11])))

    output.tests.append(Test("Fuel System", \
                             bitToBool(bits[14]), \
                             bitToBool(bits[10])))

    output.tests.append(Test("Components", \
                             bitToBool(bits[13]), \
                             bitToBool(bits[9])))


    # different tests for different ignition types 
    if(output.ignition_type == IGNITION_TYPE[0]): # spark
        for i in range(8):
            if SPARK_TESTS[i] is not None:

                t = Test(SPARK_TESTS[i], \
                         bitToBool(bits[(2 * 8) + i]), \
                         bitToBool(bits[(3 * 8) + i]))

                output.tests.append(t)

    elif(output.ignition_type == IGNITION_TYPE[1]): # compression
        for i in range(8):
            if COMPRESSION_TESTS[i] is not None:

                t = Test(COMPRESSION_TESTS[i], \
                         bitToBool(bits[(2 * 8) + i]), \
                         bitToBool(bits[(3 * 8) + i]))
                
                output.tests.append(t)

    return (output, Unit.NONE)



def fuel_status(messages):
    d = messages[0].data
    v = d[0] # todo, support second fuel system

    if v <= 0:
        debug("Invalid fuel status response (v <= 0)", True)
        return (None, Unit.NONE)

    i = math.log(v, 2) # only a single bit should be on

    if i % 1 != 0:
        debug("Invalid fuel status response (multiple bits set)", True)
        return (None, Unit.NONE)

    i = int(i)

    if i >= len(FUEL_STATUS):
        debug("Invalid fuel status response (no table entry)", True)
        return (None, Unit.NONE)

    return (FUEL_STATUS[i], Unit.NONE)


def air_status(messages):
    d = messages[0].data
    v = d[0]

    if v <= 0:
        debug("Invalid air status response (v <= 0)", True)
        return (None, Unit.NONE)

    i = math.log(v, 2) # only a single bit should be on

    if i % 1 != 0:
        debug("Invalid air status response (multiple bits set)", True)
        return (None, Unit.NONE)

    i = int(i)

    if i >= len(AIR_STATUS):
        debug("Invalid air status response (no table entry)", True)
        return (None, Unit.NONE)

    return (AIR_STATUS[i], Unit.NONE)


def obd_compliance(_hex):
    d = messages[0].data
    i = d[0]

    v = "Error: Unknown OBD compliance response"

    if i < len(OBD_COMPLIANCE):
        v = OBD_COMPLIANCE[i]

    return (v, Unit.NONE) 


def fuel_type(_hex):
    d = messages[0].data
    i = d[0] # todo, support second fuel system

    v = "Error: Unknown fuel type response"

    if i < len(FUEL_TYPES):
        v = FUEL_TYPES[i]

    return (v, Unit.NONE)


def single_dtc(_bytes):
    """ converts 2 bytes into a DTC code """

    # check validity (also ignores padding that the ELM returns)
    if (len(_bytes) != 2) or (_bytes == (0,0)):
        return None

    # BYTES: (16,      35      )
    # HEX:    4   1    2   3
    # BIN:    01000001 00100011
    #         [][][  in hex   ]
    #         | / /
    # DTC:    C0123

    dtc  = ['P', 'C', 'B', 'U'][ _bytes[0] >> 6 ] # the last 2 bits of the first byte
    dtc += str( (_bytes[0] >> 4) & 0b0011 ) # the next pair of 2 bits. Mask off the bits we read above
    dtc += bytes_to_hex(_bytes)[1:4]

    return dtc


def dtc(messages):
    """ converts a frame of 2-byte DTCs into a list of DTCs """
    codes = []
    d = []
    for message in messages:
        d += message.data

    # look at data in pairs of bytes
    # looping through ENDING indices to avoid odd (invalid) code lengths
    for n in range(1, len(d), 2):

        # parse the code
        dtc = single_dtc( (d[n-1], d[n]) )

        if dtc is not None:
            # pull a description if we have one
            if dtc in DTC:
                desc = DTC[dtc]
            else:
                desc = "Unknown error code"

            codes.append( (dtc, desc) )

    return (codes, Unit.NONE)
