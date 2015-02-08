
"""

Protocol objects are factories for Frames.
They are __called__ with a byte array, and return the parsed frame objects.
They are stateless

"""


class Protocol(object):
	def __init__(self, baud=38400):
		self.baud = baud

	def create_frame(self, raw_bytes):
		""" override in subclass for each protocol """
		raise NotImplementedError()

	def parse_frames(self, frames):
		""" override in subclass for each protocol """
		raise NotImplementedError()
