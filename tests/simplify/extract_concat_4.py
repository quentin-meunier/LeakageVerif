#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'S', 7)
b = symbol('b', 'S', 9)
c = symbol('c', 'S', 10)
d = symbol('d', 'S', 6)
n0 = Concat(d, c, b, a)

n1 = Extract(25, 7, n0)

res = Concat(c, b)
checkResults(n1, res)

n1.dump('graph.dot')


