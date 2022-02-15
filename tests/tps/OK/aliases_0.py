#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

k0 = symbol('k0', 'S', 1)

m0 = symbol('m0', 'M', 1)

p0 = symbol('p0', 'P', 1)
p1 = symbol('p1', 'P', 1)
p2 = symbol('p2', 'P', 1)

n0 = k0 ^ m0

n1 = n0 & p0
n2 = ~n0
n3 = n0 | p2
n4 = n1 + n2 + n3

checkTpsResult(n4, True)


