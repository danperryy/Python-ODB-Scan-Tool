
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
# protocols/protocol_can.py                                            #
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

from protocol import *


class CANProtocol(Protocol):

    PRIMARY_ECU = 0

    FRAME_TYPE_SF = 0x00  # single frame
    FRAME_TYPE_FF = 0x10  # first frame of multi-frame message
    FRAME_TYPE_CF = 0x20  # consecutive frame(s) of multi-frame message


    def __init__(self, baud, id_bits):
        Protocol.__init__(self, baud)
        self.id_bits = id_bits

    def create_frame(self, raw):

        # pad 11-bit CAN headers out to 32 bits for consistency,
        # since ELM already does this for 29-bit CAN headers
        if self.id_bits == 11:
            raw = "00000" + raw

        frame = Frame(raw)
        raw_bytes = ascii_to_bytes(raw)

        # read header information
        if self.id_bits == 11:
            frame.priority = raw_bytes[2] & 0x0F  # always 7
            frame.addr_mode = raw_bytes[3] & 0xF0  # 0xD0 = functional, 0xE0 = physical

            if frame.addr_mode == 0xD0:
                #untested("11-bit functional request from tester")
                frame.rx_id = raw_bytes[3] & 0x0F  # usually (always?) 0x0F for broadcast
                frame.tx_id = 0xF1  # made-up to mimic all other protocols
            elif raw_bytes[3] & 0x08:
                frame.rx_id = 0xF1  # made-up to mimic all other protocols
                frame.tx_id = raw_bytes[3] & 0x07
            else:
                #untested("11-bit message header from tester (functional or physical)")
                frame.tx_id = 0xF1  # made-up to mimic all other protocols
                frame.rx_id = raw_bytes[3] & 0x07

        else: # self.id_bits == 29:
            frame.priority  = raw_bytes[0]  # usually (always?) 0x18
            frame.addr_mode = raw_bytes[1]  # DB = functional, DA = physical
            frame.rx_id     = raw_bytes[2]  # 0x33 = broadcast (functional)
            frame.tx_id     = raw_bytes[3]  # 0xF1 = tester ID


        frame.data_bytes = raw_bytes[4:]


        # extra frame info in data section
        frame.type = frame.data_bytes[0] & 0xF0
        if frame.type not in [self.FRAME_TYPE_CF,
                                 self.FRAME_TYPE_FF,
                                 self.FRAME_TYPE_SF]:
            return None

        return frame


    def create_message(self, frames, tx_id):

        message = Message(frames, tx_id)

        if len(message.frames) == 1:
            message.data_bytes = message.frames[0].data_bytes[1:] # ignore PCI byte
        else:
            debug("Recieved multi-frame response. Can't parse those yet")
            return None

        return message


##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################



class ISO_15765_4_11bit_500k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=500000, id_bits=11)


class ISO_15765_4_29bit_500k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=500000, id_bits=29)


class ISO_15765_4_11bit_250k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=11)


class ISO_15765_4_29bit_250k(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=29)


class SAE_J1939(CANProtocol):
    def __init__(self):
        CANProtocol.__init__(self, baud=250000, id_bits=29)
