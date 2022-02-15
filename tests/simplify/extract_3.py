#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
n0 = SignExt(24, k)
n1 = Extract(7, 0, n0)

checkResults(n1, k)

n1.dump('graph.dot')


