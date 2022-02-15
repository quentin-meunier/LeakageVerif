#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
c = constant(0, 7)
d = constant(0, 10)
n1 = Extract(7, 0, Concat(d, c, c, k))

checkResults(n1, k)

n1.dump('graph.dot')


