#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

setBitExpEnable(True)

k = symbol('k', 'S', 32)
p = symbol('p', 'P', 32)

n0 = k ^ p

e0 = Extract(7, 0, n0)
e1 = Extract(15, 8, n0)
e2 = Extract(23, 16, n0)
e3 = Extract(31, 24, n0)

n1 = Concat(e3, e2, e1, e0)

checkResults(n1, n0)

n1.dump('graph.dot')


