#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(-2, 8)
c1 = constant(2, 8)
k0 = symbol('k0', 'S', 8)

n0 = c0 + c1
n1 = k0 | n0

# result is k0
wres = k0

checkResults(n1, wres)

n1.dump('graph.dot')


