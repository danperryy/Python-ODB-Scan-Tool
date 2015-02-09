

class Message(object):
	def __init__(self, raw, frames, tx_id):
		self.raw        = raw
		self.frames     = frames
		self.tx_id      = tx_id
		self.data_bytes = []
