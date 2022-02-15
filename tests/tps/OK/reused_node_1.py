#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k0 = symbol('k0', 'S', 1)

m0 = symbol('m0', 'M', 1)
m1 = symbol('m1', 'M', 1)
m2 = symbol('m2', 'M', 1)
m3 = symbol('m3', 'M', 1)
m4 = symbol('m4', 'M', 1)

n0 = k0 ^ m0

n1 = n0 & m1
n2 = n0 & m2
n3 = n0 & m3

n4 = n1 ^ n2 ^ n3

#n4.dump('graph.dot')

checkTpsResult(n4, True)


