
import re
from obd.utils import ascii_to_bytes
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
        self.seq_id     = 0
        self.msg_len    = None


class Message(object):
    def __init__(self, frames, tx_id):
        self.frames     = frames
        self.tx_id      = tx_id
        self.data_bytes = []




"""

Protocol objects are stateless factories for Frames and Messages.
They are __called__ with the raw string response, and return a
list of Messages.

"""

class Protocol(object):

    PRIMARY_ECU = None

    def __init__(self, baud=38400):
        self.baud = baud


    def __call__(self, raw):

        # split by lines into frames, and remove empty lines
        lines = filter(bool, re.split("[\r\n]", raw))

        # ditch spaces
        lines = [line.replace(' ', '') for line in lines]

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

            Function recieves the raw string data for a frame.

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
