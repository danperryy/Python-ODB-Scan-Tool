
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
# protocols/protocol.py                                                #
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

from obd.utils import ascii_to_bytes, isHex
from obd.debug import debug


"""

Basic data models for all protocols to use

"""


class Frame(object):
    def __init__(self, raw):
        self.raw        = raw
        self.data_bytes = []
        self.priority   = None
        self.addr_mode  = None
        self.rx_id      = None
        self.tx_id      = None
        self.type       = None
        self.seq_index  = 0 # only used when type = CF
        self.data_len   = None


class Message(object):
    def __init__(self, frames, tx_id):
        self.frames     = frames
        self.tx_id      = tx_id
        self.data_bytes = []

    def __eq__(self, other):
        if isinstance(other, Message):
            for attr in ["frames", "tx_id", "data_bytes"]:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        else:
            return False




"""

Protocol objects are stateless factories for Frames and Messages.
They are __called__ with the raw string response, and return a
list of Messages.

"""

class Protocol(object):

    PRIMARY_ECU = None

    def __init__(self, baud=38400):
        self.baud = baud


    def __call__(self, lines):

        # ditch spaces
        lines = [line.replace(' ', '') for line in lines]

        # ditch frames without valid hex (trashes "NO DATA", etc...)
        lines = filter(isHex, lines)

        frames = []
        for line in lines:
            # subclass function to parse the lines into Frames
            frame = self.create_frame(line)

            # drop frames that couldn't be parsed
            if frame is not None:
                frames.append(frame)

        # group frames by transmitting ECU (tx_id)
        ecus = {}
        for frame in frames:
            if frame.tx_id not in ecus:
                ecus[frame.tx_id] = [frame]
            else:
                ecus[frame.tx_id].append(frame)

        messages = []
        for ecu in ecus:
            # subclass function to assemble frames into Messages
            message = self.create_message(ecus[ecu], ecu)

            # drop messages that couldn't be assembled
            if message is not None:
                messages.append(message)

        return messages


    def create_frame(self, raw):
        """
            override in subclass for each protocol

            Function recieves a list of byte values for a frame.

            Function should return a Frame instance. If fatal errors were
            found, this function should return None (the Frame is dropped).
        """
        raise NotImplementedError()


    def create_message(self, frames):
        """
            override in subclass for each protocol

            Function recieves a list of Frame objects.

            Function should return a Message instance. If fatal errors were
            found, this function should return None (the Message is dropped).
        """
        raise NotImplementedError()
