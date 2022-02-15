#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k = symbol('k', 'S', 8)
n0 = ZeroExt(24, k)
n1 = Extract(7, 7, n0)

n2 = Extract(7, 7, k)
checkResults(n1, n2)

n1.dump('graph.dot')


