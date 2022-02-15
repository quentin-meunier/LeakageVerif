#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(5, 8)
c1 = constant(0, 8)

n0 = c0 + c1

# result is 5
checkResults(n0, c0)

n0.dump('graph.dot')


