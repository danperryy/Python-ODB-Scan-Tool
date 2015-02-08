

from protocol import Protocol
from frame import Frame


class LegacyProtocol(Protocol):
	def __init__(self, baud):
		Protocol.__init__(baud)

	def create_frame(self, raw_bytes):

		frame = Frame(self, raw_bytes)

		frame.data_bytes = raw_bytes[3:-1] # exclude trailing checksum (handled by ELM adapter)

		# read header information
		frame.priority = raw_bytes[0]
		frame.rx_id    = raw_bytes[1]
		frame.tx_id    = raw_bytes[2]

		return frame

	def parse_frames(self, frames):
		pass



##############################################
#                                            #
# Here lie the class stubs for each protocol #
#                                            #
##############################################



class SAE_J1850_PWM(LegacyProtocol):

	def __init__(self):
		LegacyProtocol.__init__(baud=41600)


class SAE_J1850_VPW(LegacyProtocol):

	def __init__(self):
		LegacyProtocol.__init__(baud=10400)


class ISO_9141_2(LegacyProtocol):

	def __init__(self):
		LegacyProtocol.__init__(baud=10400)


class ISO_14230_4_5baud(LegacyProtocol):
	def __init__(self):
		LegacyProtocol.__init__(baud=10400)


class ISO_14230_4_fast(LegacyProtocol):
	def __init__(self):
		LegacyProtocol.__init__(baud=10400)
