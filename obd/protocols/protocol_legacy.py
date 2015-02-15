
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2015 Brendan Whitfield (bcw7044@rit.edu)                   #
#                                                                      #
########################################################################
#                                                                      #
# protocols/protocol_legacy.py                                         #
#                                                                      #
# This file is part of python-OBD (a derivative of pyOBD)              #
#                                                                      #
# python-OBD is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 2 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# python-OBD is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with python-OBD.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                      #
########################################################################

from protocol import *


class LegacyProtocol(Protocol):

	PRIMARY_ECU = 0x10

	def __init__(self, baud):
		Protocol.__init__(self, baud)

	def create_frame(self, raw):

		frame = Frame(raw)
		raw_bytes = ascii_to_bytes(raw)

		if len(raw_bytes) < 5:
			return None

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
