#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



c0 = constant(0, 8)
c1 = constant(5, 8)
c2 = constant(251, 8)

n0 = c0 - c1
# result is -5 or 251
wres = c2

checkResults(n0, wres)

n0.dump('graph.dot')


