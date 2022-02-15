#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k = symbol('k', 'S', 8)
c = constant(0, 7)
d = constant(0, 10)
n0 = Concat(k, c, c, d)
n1 = Extract(31, 24, n0)

checkResults(n1, k)

n1.dump('graph.dot')


