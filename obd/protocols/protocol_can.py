

from protocol import Protocol
from frame import Frame


class CANProtocol(Protocol):
	def __init__(self, baud, id_bits):
		Protocol.__init__(baud)
		self.id_bits = id_bits


	def create_frame(self, raw_bytes):
		frame = Frame(self, raw_bytes)
		return frame


	def parse_frames(self, frames):
		pass



##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################


class ISO_15765_4_11bit_500k(CANProtocol):
	def __init__(self):
		CANProtocol.__init__(baud=500000, id_bits=11)


class ISO_15765_4_29bit_500k(CANProtocol):
	def __init__(self):
		CANProtocol.__init__(baud=500000, id_bits=29)


class ISO_15765_4_11bit_250k(CANProtocol):
	def __init__(self):
		CANProtocol.__init__(baud=250000, id_bits=11)


class ISO_15765_4_29bit_250k(CANProtocol):
	def __init__(self):
		CANProtocol.__init__(baud=250000, id_bits=29)


class SAE_J1939(CANProtocol):
	def __init__(self):
		CANProtocol.__init__(baud=250000, id_bits=29)
