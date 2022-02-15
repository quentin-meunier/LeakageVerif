#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)
u = symbol('u', 'P', 8)
v = symbol('v', 'P', 8)
z = symbol('z', 'P', 8)
w = symbol('w', 'P', 8)


r = a & (u & (v | z) | d) | a & (d | u & (w | z))

res = a & (u & (v | w | z) | d)

checkResults(r, res)



