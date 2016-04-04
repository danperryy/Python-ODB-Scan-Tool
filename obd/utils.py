
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2015 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# utils.py                                                             #
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

import serial
import errno
import string
import glob
import sys
from .debug import debug


class OBDStatus:
    """ Values for the connection status flags """

    NOT_CONNECTED = "Not Connected"
    ELM_CONNECTED = "ELM Connected"
    CAR_CONNECTED = "Car Connected"




def num_bits_set(n):
    return bin(n).count("1")

def unhex(_hex):
    _hex = "0" if _hex == "" else _hex
    return int(_hex, 16)

def unbin(_bin):
    return int(_bin, 2)

def bytes_to_int(bs):
    """ converts a big-endian byte array into a single integer """
    v = 0
    p = 0
    for b in reversed(bs):
        v += b * (2**p)
        p += 8
    return v

def bytes_to_bits(bs):
    bits = ""
    for b in bs:
        v = bin(b)[2:]
        bits += ("0" * (8 - len(v))) + v # pad it with zeros
    return bits

def bytes_to_hex(bs):
    h = ""
    for b in bs:
        bh = hex(b)[2:]
        h += ("0" * (2 - len(bh))) + bh
    return h

def bitstring(_hex, bits=None):
    b = bin(unhex(_hex))[2:]
    if bits is not None:
        b = ('0' * (bits - len(b))) + b
    return b

def bitToBool(_bit):
    return (_bit == '1')

def twos_comp(val, num_bits):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(num_bits-1))) != 0 ):
        val = val - (1<<num_bits)
    return val

def isHex(_hex):
    return all([c in string.hexdigits for c in _hex])

def contiguous(l, start, end):
    """ checks that a list of integers are consequtive """
    if not l:
        return False
    if l[0] != start:
        return False
    if l[-1] != end:
        return False

    # for consequtiveness, look at the integers in pairs
    pairs = zip(l, l[1:])
    if not all([p[0]+1 == p[1] for p in pairs]):
        return False

    return True


def try_port(portStr):
    """returns boolean for port availability"""
    try:
        s = serial.Serial(portStr)
        s.close() # explicit close 'cause of delayed GC in java
        return True

    except serial.SerialException:
        pass
    except OSError as e:
        if e.errno != errno.ENOENT: # permit "no such file or directory" errors
            raise e

    return False


def scan_serial():
    """scan for available ports. return a list of serial names"""
    available = []

    possible_ports = []

    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        possible_ports += glob.glob("/dev/rfcomm[0-9]*")
        possible_ports += glob.glob("/dev/ttyUSB[0-9]*")

    elif sys.platform.startswith('win'):
        possible_ports += ["\\.\COM%d" % i for i in range(256)]

    elif sys.platform.startswith('darwin'):
        exclude = [
            '/dev/tty.Bluetooth-Incoming-Port',
            '/dev/tty.Bluetooth-Modem'
        ]
        possible_ports += [port for port in glob.glob('/dev/tty.*') if port not in exclude]

    # possible_ports += glob.glob('/dev/pts/[0-9]*') # for obdsim

    for port in possible_ports:
        if try_port(port):
            available.append(port)

    return available

# TODO: deprecated, remove later
def scanSerial():
    print("scanSerial() is deprecated, use scan_serial() instead")
    return scan_serial()
