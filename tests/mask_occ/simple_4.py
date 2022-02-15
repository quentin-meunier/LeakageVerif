#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

n0 = ~m0
n0.printMaskOcc()

n1 = n0 ^ k0
n1.printMaskOcc()

n2 = ~n1
n2.printMaskOcc()

n3 = m1 ^ n2
n3.printMaskOcc()

e = k1 ^ n3

e.printMaskOcc()
e.dump('graph.dot')



