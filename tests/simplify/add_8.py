#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(-2, 8)
c1 = constant(2, 8)
c2 = constant(4, 8)
c3 = constant(-4, 8)

k0 = symbol('k0', 'S', 8)

n0 = (c0 + c1 + c2 + c3) ^ k0 ^ (c2 + c3) ^ k0

# result is 0
wres = constant(0, 8)

checkResults(n0, wres)

n0.dump('graph.dot')


