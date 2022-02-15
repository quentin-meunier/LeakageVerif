#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k', 'S', 3)
c0 = constant(0, 3)

n0 = k0 - c0
# result is k
wres = k0

checkResults(n0, wres)

n0.dump('graph.dot')


