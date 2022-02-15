#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

p0 = symbol('p0', 'S', 3)
p1 = symbol('p1', 'S', 3)
p2 = symbol('p2', 'S', 3)
p3 = symbol('p3', 'S', 3)
a = ArrayExp('a', 3, 3)

f = p0 ^ p1 ^ p2 ^ p0
e = a[f]

res = a[p1 ^ p2]

checkResults(e, res)


