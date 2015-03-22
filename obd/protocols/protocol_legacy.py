
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
# protocols/protocol_legacy.py                                         #
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

from obd.utils import contiguous
from .protocol import *


class LegacyProtocol(Protocol):

    PRIMARY_ECU = 0x10

    def __init__(self, baud):
        Protocol.__init__(self, baud)

    def create_frame(self, raw):

        frame = Frame(raw)
        raw_bytes = ascii_to_bytes(raw)

        if len(raw_bytes) < 6:
            debug("Dropped frame for being too short")
            return None

        if len(raw_bytes) > 11:
            debug("Dropped frame for being too long")
            return None

        # Ex.
        # [Header] [     Frame     ]
        # 48 6B 10 41 00 BE 7F B8 13 ck
        # ck = checksum byte

        # exclude header and trailing checksum (handled by ELM adapter)
        frame.data_bytes = raw_bytes[3:-1]

        # read header information
        frame.priority = raw_bytes[0]
        frame.rx_id    = raw_bytes[1]
        frame.tx_id    = raw_bytes[2]

        return frame

    def create_message(self, frames, tx_id):

        message = Message(frames, tx_id)

        # len(frames) will always be >= 1 (see the caller, protocol.py)
        mode = frames[0].data_bytes[0]
        
        # test that all frames are responses to the same Mode (SID)
        if len(frames) > 1:
            if not all([mode == f.data_bytes[0] for f in frames[1:]]):
                debug("Recieved frames from multiple commands")
                return None

        # legacy protocols have different re-assembly
        # procedures for different Modes 

        if mode == 0x43:
            # GET_DTC requests return frames with no PID or order bytes
            # accumulate all of the data, minus the Mode bytes of each frame

            # Ex.
            #          [       Frame      ]
            # 48 6B 10 43 03 00 03 02 03 03 ck
            # 48 6B 10 43 03 04 00 00 00 00 ck
            #             [     Data      ]

            for f in frames:
                message.data_bytes += f.data_bytes[1:]

        else:
            if len(frames) == 1:
                # return data, excluding the mode/pid bytes

                # Ex.
                #          [     Frame     ]
                # 48 6B 10 41 00 BE 7F B8 13 ck
                #                [  Data   ]

                message.data_bytes = frames[0].data_bytes[2:]

            else: # len(frames) > 1:
                # generic multiline requests carry an order byte

                # Ex.
                #          [      Frame       ]
                # 48 6B 10 49 02 01 00 00 00 31 ck
                # 48 6B 10 49 02 02 44 34 47 50 ck
                # 48 6B 10 49 02 03 30 30 52 35 ck
                # etc...         [] [  Data   ]

                # sort the frames by the order byte
                frames = sorted(frames, key=lambda f: f.data_bytes[2])

                # check contiguity
                indices = [f.data_bytes[2] for f in frames]
                if not contiguous(indices, 1, len(frames)):
                    debug("Recieved multiline response with missing frames")
                    return None

                # now that they're in order, accumulate the data from each frame
                for f in frames:
                    message.data_bytes += f.data_bytes[3:] # loose the mode/pid/seq bytes

        return message



##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################



class SAE_J1850_PWM(LegacyProtocol):
    def __init__(self):
        LegacyProtocol.__init__(self, baud=41600)


class SAE_J1850_VPW(LegacyProtocol):
    def __init__(self):
        LegacyProtocol.__init__(self, baud=10400)


class ISO_9141_2(LegacyProtocol):
    def __init__(self):
        LegacyProtocol.__init__(self, baud=10400)


class ISO_14230_4_5baud(LegacyProtocol):
    def __init__(self):
        LegacyProtocol.__init__(self, baud=10400)


class ISO_14230_4_fast(LegacyProtocol):
    def __init__(self):
        LegacyProtocol.__init__(self, baud=10400)
