#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k = symbol('k', 'S', 8)
c = constant(0, 7)
d = constant(0, 10)
n0 = Concat(d, c, k, c)
n1 = Extract(14, 7, n0)

checkResults(n1, k)

n1.dump('graph.dot')


