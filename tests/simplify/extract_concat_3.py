#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'S', 9)
b = symbol('b', 'S', 7)
c = symbol('c', 'S', 10)
d = symbol('d', 'S', 6)
n0 = Concat(d, c, b, a)

n1 = Extract(15, 0, n0)

res = Concat(b, a)
checkResults(n1, res)

n1.dump('graph.dot')


