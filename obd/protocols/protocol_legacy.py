
from protocol import *


class LegacyProtocol(Protocol):

	PRIMARY_ECU = 0x10

	def __init__(self, baud):
		Protocol.__init__(self, baud)

	def create_frame(self, raw):

		frame = Frame(raw)
		raw_bytes = ascii_to_bytes(raw)

		frame.data_bytes = raw_bytes[3:-1] # exclude trailing checksum (handled by ELM adapter)

		# read header information
		frame.priority = raw_bytes[0]
		frame.rx_id    = raw_bytes[1]
		frame.tx_id    = raw_bytes[2]

		return frame

	def create_message(self, frames, tx_id):

		message = Message(frames, tx_id)

		if len(frames) == 1:
			message.data_bytes = message.frames[0].data_bytes
		else:
			debug("Recieved multi-frame response. Can't parse those yet")
			return None

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
