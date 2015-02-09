

class Message(object):
	def __init__(self, frames, tx_id):
		self.frames     = frames
		self.tx_id      = tx_id
		self.data_bytes = []
