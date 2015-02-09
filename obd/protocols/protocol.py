
"""

Protocol objects are stateless factories for Frames and Messages.
They are __called__ with the raw string response, and
return a list of Messages.

"""

from frame import Frame
from message import Message
import re



class Protocol(object):
    def __init__(self, baud=38400):
        self.baud = baud        


    def __call__(self, raw):

        # split by lines into frames, and remove empty lines
        lines = filter(bool, re.split("[\r\n]", raw))

        # ditch spaces
        lines = [line.replace(' ', '') for line in lines]

        # create frame objects for each line
        frames = [Frame(line) for line in lines]

        # subclass function to load the frame parameters
        for frame in frames:
            self.parse_frame(frame)

        # group frames by transmitting ECU (tx_id)
        ecus = {}
        for frame in frames:
            if frame.tx_id not in ecus:
                ecus[frame.tx_id] = [frame]
            else:
                ecus[frame.tx_id].append(frame)

        messages = []

        for ecu in ecus:
            message = Message(ecus[ecu], ecu)
            # subclass function to assemble frames into data_bytes
            self.parse_message(message)
            messages.append(message)

        return messages


    def parse_frame(self, frame):
        """ override in subclass for each protocol """
        raise NotImplementedError()

    def parse_message(self, message):
        """ override in subclass for each protocol """
        raise NotImplementedError()
