#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

m = symbol('m', 'M', 8)
n = ~m

n.printMaskOcc()

e = n + n

e.printMaskOcc()




