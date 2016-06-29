
########################################################################
#                                                                      #
# python-OBD: A python OBD-II serial module derived from pyobd         #
#                                                                      #
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)                 #
# Copyright 2009 Secons Ltd. (www.obdtester.com)                       #
# Copyright 2009 Peter J. Creath                                       #
# Copyright 2016 Brendan Whitfield (brendan-w.com)                     #
#                                                                      #
########################################################################
#                                                                      #
# OBDResponse.py                                                       #
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



import time
import pint


# export the unit registry
Unit = pint.UnitRegistry()
Unit.define("percent = [] = %")
Unit.define("gps = gram / second = GPS = grams_per_second")
Unit.define("lph = liter / hour = LPH = liters_per_hour")


class OBDResponse():
    """ Standard response object for any OBDCommand """

    def __init__(self, command=None, messages=None):
        self.command  = command
        self.messages = messages if messages else []
        self.value    = None
        self.time     = time.time()

    @property
    def unit(self):
        # for backwards compatibility
        if isinstance(self.value, Unit.Quantity):
            return str(self.value.u)
        elif self.value == None:
            return None
        else:
            return str(type(self.value))

    def is_null(self):
        return (not self.messages) or (self.value == None)

    def __str__(self):
        return str(self.value)



"""
    Special value types used in OBDResponses
    instantiated in decoders.py
"""


class Status():
    def __init__(self):
        self.MIL           = False
        self.DTC_count     = 0
        self.ignition_type = ""
        self.tests         = []


class Test():
    def __init__(self, name, available, incomplete):
        self.name       = name
        self.available  = available
        self.incomplete = incomplete

    def __str__(self):
        a = "Available" if self.available else "Unavailable"
        c = "Incomplete" if self.incomplete else "Complete"
        return "Test %s: %s, %s" % (self.name, a, c)
