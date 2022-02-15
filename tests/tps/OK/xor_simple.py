#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


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

n6 = n5 ^ n2
n7 = n6 ^ n0

#n7.dump('graph.dot')

checkTpsResult(n7, True)





