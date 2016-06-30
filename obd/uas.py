
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
# uac.py                                                               #
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

from .utils import *
from .OBDResponse import Unit


class UAS():
    """
    Class for representing a Unit and Scale conversion
    Used in the decoding of Mode 06 monitor responses
    """

    def __init__(self, signed, scale, unit):
        self.signed = signed
        self.scale = scale
        self.unit = unit

    def __call__(self, _bytes):
        value = bytes_to_int(_bytes)

        if self.signed:
            value = twos_comp(value, len(_bytes) * 8)

        value *= self.scale

        return Unit.Quantity(value, self.unit)


# dict for looking up standardized UAS IDs with conversion objects
UAS_IDS = {
    0x01 : UAS(False, 1,          Unit.count),
    0x02 : UAS(False, 0.1,        Unit.count),
    0x03 : UAS(False, 0.01,       Unit.count),
    0x04 : UAS(False, 0.001,      Unit.count),
    0x05 : UAS(False, 0.0000305,  Unit.count),
    0x06 : UAS(False, 0.000305,   Unit.count),
    0x07 : UAS(False, 0.25,       Unit.rpm),
    0x08 : UAS(False, 0.01,       Unit.kph),
    0x09 : UAS(False, 1,          Unit.kph),
    0x0A : UAS(False, 0.122,      Unit.millivolt),
    0x0B : UAS(False, 0.001,      Unit.volt),
    0x0C : UAS(False, 0.01,       Unit.volt),
    0x0D : UAS(False, 0.00390625, Unit.milliampere),
    0x0E : UAS(False, 0.001,      Unit.ampere),
    0x0F : UAS(False, 0.01,       Unit.ampere),
    0x10 : UAS(False, 1,          Unit.millisecond),
    0x11 : UAS(False, 100,        Unit.millisecond),
    0x12 : UAS(False, 1,          Unit.second),
    0x13 : UAS(False, 1,          Unit.milliohm),
    0x14 : UAS(False, 1,          Unit.ohm),
    0x15 : UAS(False, 1,          Unit.kiloohm),
    0x16 : None, # TODO
    0x17 : UAS(False, 0.01,       Unit.kilopascal),
    0x18 : UAS(False, 0.0117,     Unit.kilopascal),
    0x19 : UAS(False, 0.079,      Unit.kilopascal),
    0x1A : UAS(False, 1,          Unit.kilopascal),
    0x1B : UAS(False, 10,         Unit.kilopascal),
    0x1C : UAS(False, 0.01,       Unit.degree),
    0x1D : UAS(False, 0.5,        Unit.degree),
    0x1E : None, # TODO
    0x1F : UAS(False, 0.05,       Unit.ratio),
    0x20 : UAS(False, 0.00390625, Unit.ratio),
    0x21 : UAS(False, 1,          Unit.millihertz),
    0x22 : UAS(False, 1,          Unit.hertz),
    0x23 : UAS(False, 1,          Unit.kilohertz),
    0x24 : UAS(False, 1,          Unit.count),
    0x25 : UAS(False, 1,          Unit.kilometer),
    0x26 : UAS(False, 0.1,        Unit.millivolt / Unit.millisecond),
    0x27 : UAS(False, 0.1,        Unit.grams_per_second),
    0x28 : UAS(False, 1,          Unit.grams_per_second),
}
