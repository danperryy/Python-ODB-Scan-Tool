

class Frame(object):
	def __init__(self, protocol, raw_bytes):
		self.protocol   = protocol
		self.raw_bytes  = raw_bytes

		self.data_bytes = []
		self.priority   = None
		self.rx_id      = None
		self.tx_id      = None
