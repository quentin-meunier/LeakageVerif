#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)

n = Concat(a, Concat(Concat(d, b), c, Concat(Concat(a, b), b, Concat(c, d))), d, Concat(a, d))

res = Concat(a, d, b, c, a, b, b, c, d, d, a, d)

checkResults(n, res)



