#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k0', 'S', 3)
k1 = symbol('k1', 'S', 3)

p0 = symbol('p0', 'M', 3)
p1 = symbol('p1', 'M', 3)
p2 = symbol('p2', 'M', 3)
p3 = symbol('p3', 'M', 3)

n0 = k0 ^ p0 ^ p1
n1 = n0 & p2

n2 = p0 ^ p1 ^ k0
n3 = n2 & p2

n4 = n1 ^ n3 ^ p3
n5 = n4 + k1

wres = k1 + p3


checkResults(n5, wres)

n5.dump('graph.dot')


