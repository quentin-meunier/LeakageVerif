#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0x12345678, 32)
c1 = constant(8, 8)
c3 = Extract(15, c1, c0)

# result is 0x56
wres = constant(0x56, 8)

checkResults(c3, wres)

c3.dump('graph.dot')


