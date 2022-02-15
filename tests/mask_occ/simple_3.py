#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m = symbol('m', 'M', 8)
k = symbol('k', 'S', 8)

n0 = k ^ m
n0.printMaskOcc()

n1 = ~n0
n1.printMaskOcc()

e = n1 + n1

e.printMaskOcc()
e.dump('graph.dot')



