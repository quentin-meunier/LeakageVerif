#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0x78, 8)
c1 = constant(0x56, 8)
c2 = constant(0x34, 8)
c3 = constant(0x12, 8)
c4 = constant(0x12345678, 32)
n = Concat(c3, c2, c1, c0)

# result is 0x12345678
wres = c4

checkResults(n, wres)

n.dump('graph.dot')


