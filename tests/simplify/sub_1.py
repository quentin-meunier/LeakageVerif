#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k', 'S', 2)
c0 = constant(0, 2)

n0 = k0 - k0

# result is 0
wres = c0

checkResults(n0, wres)

n0.dump('graph.dot')


