#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

p0 = symbol('p0', 'S', 3)
p1 = symbol('p1', 'S', 3)
p2 = symbol('p2', 'S', 3)
p3 = symbol('p3', 'S', 3)

f = p0 & p1 & p2 & p3
e = p0 ^ p0 ^ f
n = ~e | (e >> 1)

n.dump('graph.dot')

res = checkTpsVal(n)


