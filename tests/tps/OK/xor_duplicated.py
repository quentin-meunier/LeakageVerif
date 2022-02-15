#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


s0 = symbol('s0', 'S', 1)
r0 = symbol('r0', 'M', 1)

n0 = s0 ^ r0
n1 = s0 ^ r0
n2 = s0 ^ r0
n3 = s0 ^ r0
n4 = s0 ^ r0
n5 = s0 ^ r0
n6 = s0 ^ r0
n7 = s0 ^ r0

e = Concat(n0, n1, n2, n3, n4, n5, n6, n7)

checkTpsResult(e, True)




