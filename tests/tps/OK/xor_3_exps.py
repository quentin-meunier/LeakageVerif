#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

# 3 exps:
# m0 ^ k0
# m0 ^ m1 ^ k1
# m0 ^ m1 ^ m2 ^ k2

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
k2 = symbol('k2', 'S', 8)

m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)
m2 = symbol('m2', 'M', 8)

n0 = k0 ^ m0

n1 = k1 ^ m0
n2 = n1 ^ m1

n3 = k2 ^ m0
n4 = n3 ^ m1
n5 = n4 ^ m2

e = Concat(n0, n2, n5)

#e.dump('graph.dot', True)

checkTpsStrategies(e, True)


