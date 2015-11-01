
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

from obd.utils import ascii_to_bytes, isHex, numBitsSet
from obd.debug import debug


"""

Basic data models for all protocols to use

"""


class ECU:
    """ constant flags used for marking and filtering messages """

    ALL          = 0b11111111 # used by OBDCommands to accept messages from any ECU
    ALL_KNOWN    = 0b11111110 # used to ignore unknown ECUs, since this lib probably can't handle them

    # each ECU gets its own bit for ease of making OR filters
    UNKNOWN      = 0b00000001 # unknowns get their own bit, since they need to be accepted by the ALL filter
    ENGINE       = 0b00000010
    TRANSMISSION = 0b00000100


class Frame(object):
    def __init__(self, raw):
        self.raw       = raw
        self.data      = []
        self.priority  = None
        self.addr_mode = None
        self.rx_id     = None
        self.tx_id     = None
        self.type      = None
        self.seq_index = 0 # only used when type = CF
        self.data_len  = None


class Message(object):
    def __init__(self, raw, frames):
        self.raw    = raw
        self.frames = frames
        self.ecu    = ECU.UNKNOWN
        self.data   = []

    @property
    def tx_id(self):
        if len(self.frames) == 0:
            return None
        else:
            return self.frames[0].tx_id

    def __eq__(self, other):
        if isinstance(other, Message):
            for attr in ["raw", "frames", "ecu", "data"]:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        else:
            return False




"""

Protocol objects are stateless factories for Frames and Messages.
They are __called__ with a list of string responses, and return a
list of Messages.

"""

class Protocol(object):

    # override in subclass for each protocol

    ELM_NAME = ""
    ELM_ID = ""

    TX_ID_ENGINE = None


    def __init__(self, lines_0100):
        """
            constructs a protocol object

            uses a list of raw strings from the
            car to determine the ECU layout.
        """

        # create the default map
        # for example: self.TX_ID_ENGINE : ECU.ENGINE
        self.ecu_map = {}

        # parse the 0100 data into messages
        # NOTE: at this point, their "ecu" property will be UNKNOWN
        messages = self(lines_0100)

        # read the messages and assemble the map
        # subsequent runs will now be tagged correctly
        self.populate_ecu_map(messages)


    def __call__(self, lines):
        """
            Main function

            accepts a list of raw strings from the car, split by lines
        """

        # ditch spaces
        filtered_lines = [line.replace(' ', '') for line in lines]

        # ditch frames without valid hex (trashes "NO DATA", etc...)
        filtered_lines = filter(isHex, filtered_lines)

        # parse each frame (each line)
        frames = []
        for line in filtered_lines:

            frame = Frame(line)

            # subclass function to parse the lines into Frames
            # drop frames that couldn't be parsed
            if self.parse_frame(frame):
                frames.append(frame)


        # group frames by transmitting ECU
        # ecus[tx_id] = [Frame, Frame]
        ecus = {}
        for frame in frames:
            if frame.tx_id not in ecus:
                ecus[frame.tx_id] = [frame]
            else:
                ecus[frame.tx_id].append(frame)

        # parse frames into whole messages
        messages = []
        for ecu in ecus:

            # new message object with a copy of the raw data
            # and frames addressed for this ecu
            message = Message(list(lines), ecus[ecu])

            # subclass function to assemble frames into Messages
            if self.parse_message(message):
                message.ecu = self.lookup_ecu(ecu) # mark with the appropriate ECU ID
                messages.append(message)

        return messages


    def lookup_ecu(self, tx_id):
        if tx_id in self.ecu_map:
            return self.ecu_map[tx_id]
        else:
            return ECU.UNKNOWN


    def populate_ecu_map(self, messages):
        """
            Given a list of messages from different ECUS,
            (in response to the 0100 PID listing command)
            associate each tx_id to an ECU ID constant.

            This is mostly concerned with finding the engine.
        """

        if len(messages) == 0:
            pass
        elif len(messages) == 1:
            # if there's only one response, mark it as the engine regardless
            self.ecu_map[messages[0].tx_id] = ECU.ENGINE
        else:

            # the engine is important
            # if we can't find it, we'll use a fallback
            found_engine = False

            # if any tx_ids are exact matches to the expected values, record them
            for m in messages:
                if m.tx_id == self.TX_ID_ENGINE:
                    self.ecu_map[m.tx_id] = ECU.ENGINE
                    found_engine = True
                # TODO: program more of these when we figure out their constants
                # elif m.tx_id == self.TX_ID_TRANSMISSION:
                    # self.ecu_map[m.tx_id] = ECU.TRANSMISSION

            if not found_engine:
                # last resort solution, choose ECU with the most bits set
                # (most PIDs supported) to be the engine
                best = 0
                tx_id = None

                for message in messages:
                    bits = sum([numBitsSet(b) for b in message.data])

                    if bits > best:
                        best = bits
                        tx_id = message.tx_id

                self.ecu_map[tx_id] = ECU.ENGINE

            # any remaining tx_ids are unknown
            for m in messages:
                if m.tx_id not in self.ecu_map:
                    self.ecu_map[m.tx_id] = ECU.UNKNOWN


    def parse_frame(self, frame):
        """
            override in subclass for each protocol

            Function recieves a Frame object preloaded
            with the raw string line from the car.

            Function should return a boolean. If fatal errors were
            found, this function should return False, and the Frame will be dropped.
        """
        raise NotImplementedError()


    def parse_message(self, message):
        """
            override in subclass for each protocol

            Function recieves a Message object
            preloaded with a list of Frame objects.

            Function should return a boolean. If fatal errors were
            found, this function should return False, and the Message will be dropped.
        """
        raise NotImplementedError()
