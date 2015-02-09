

class Frame(object):
	def __init__(self, raw):
		self.raw        = raw
		self.data_bytes = []
		self.priority   = None
		self.addr_mode  = None
		self.rx_id      = None
		self.tx_id      = None
