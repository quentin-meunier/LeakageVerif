#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 2)
q = symbol('q', 'P', 2)
r = symbol('r', 'P', 2)

n = -p + q - r + p + (p - q) + r - p

c = constant(0, 2)

# result is 0
wres = c

checkResults(n, wres)

n.dump('graph.dot')


