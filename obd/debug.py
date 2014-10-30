
class Debug():
	def __init__(self):
		self.console = False
		self.handler = None

	def __call__(self, msg):
		if self.console:
			print msg
		if hasattr(self.handler, '__call__'):
			self.handler(msg)

debug = Debug()