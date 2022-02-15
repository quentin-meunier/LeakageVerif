#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)

k = symbol('k', 'S', 8)

n0 = m0 ^ k
n0.printMaskOcc()

n1 = m1 + n0
n1.printMaskOcc()

e = n1 + m0

e.printMaskOcc()
e.dump('graph.dot')



