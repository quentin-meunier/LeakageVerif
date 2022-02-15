#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m = symbol('m', 'M', 8)

e = m + m

e.printMaskOcc()




