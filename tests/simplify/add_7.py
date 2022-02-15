#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
t = constant(0, 8)
p = constant(0, 8)

n = (k ^ t) + p

wres = k

checkResults(n, wres)

n.dump('graph.dot')


