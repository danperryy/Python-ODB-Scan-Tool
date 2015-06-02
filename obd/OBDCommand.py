
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
# OBDCommand.py                                                        #
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

from .utils import *
from .debug import debug
from .OBDResponse import OBDResponse


class OBDCommand():
    def __init__(self, name, desc, command, returnBytes, decoder, ecu, supported=False):
        self.name      = name        # human readable name (also used as key in commands dict)
        self.desc      = desc        # human readable description
        self.command   = command     # command string
        self.bytes     = returnBytes # number of bytes expected in return
        self.decode    = decoder     # decoding function
        self.ecu       = ecu         # ECU ID from which this command expects messages from
        self.supported = supported   # bool for support

    def clone(self):
        return OBDCommand(self.name,
                          self.desc,
                          self.command,
                          self.bytes,
                          self.decode,
                          self.ecu)

    @property
    def mode_int(self):
        if len(self.command) >= 2:
            return unhex(self.command[:2])
        else:
            return 0

    @property
    def pid_int(self):
        if len(self.command) > 2:
            return unhex(self.command[2:])
        else:
            return 0

    def __call__(self, messages):

        # create the response object with the raw data recieved
        # and reference to original command
        r = OBDResponse(self, messages)
        
        # combine the bytes back into a hex string
        # TODO: rewrite decoders to handle raw byte arrays
        _data = ""

        # filter for applicable messages
        for message in messages:

            # if this command accepts messages from this ECU
            if self.ecu & message.ecu > 0:
                for b in message.data:
                    h = hex(b)[2:].upper()
                    h = "0" + h if len(h) < 2 else h
                    _data += h

        # constrain number of bytes in response
        if (self.bytes > 0): # zero bytes means flexible response
            _data = constrainHex(_data, self.bytes)

        # decoded value into the response object
        d = self.decode(_data)
        r.value = d[0]
        r.unit  = d[1]

        return r

    def __str__(self):
        return "%s: %s" % (self.command, self.desc)

    def __hash__(self):
        # needed for using commands as keys in a dict (see async.py)
        return hash(self.command)

    def __eq__(self, other):
        if isinstance(other, OBDCommand):
            return (self.command == other.command)
        else:
            return False
