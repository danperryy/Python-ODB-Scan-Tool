
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



class Unit:
    """ All unit constants used in python-OBD """

    NONE    = None
    RATIO   = "Ratio"
    COUNT   = "Count"
    PERCENT = "%"
    RPM     = "RPM"
    VOLT    = "Volt"
    F       = "F"
    C       = "C"
    SEC     = "Second"
    MIN     = "Minute"
    PA      = "Pa"
    KPA     = "kPa"
    PSI     = "psi"
    KPH     = "kph"
    MPH     = "mph"
    DEGREES = "Degrees"
    GPS     = "Grams per Second"
    MA      = "mA"
    KM      = "km"
    LPH     = "Liters per Hour"



class OBDResponse():
    """ Standard response object for any OBDCommand """

    def __init__(self, command=None, messages=None):
        self.command  = command
        self.messages = messages if messages else []
        self.value    = None
        self.unit     = Unit.NONE
        self.time     = time.time()

    def is_null(self):
        return (not self.messages) or (self.value == None)

    def __str__(self):
        if self.unit != Unit.NONE:
            return "%s %s" % (str(self.value), str(self.unit))
        else:
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
