#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)

n = Concat(a, Concat(b, c), d)

res = Concat(a, b, c, d)

checkResults(n, res)



