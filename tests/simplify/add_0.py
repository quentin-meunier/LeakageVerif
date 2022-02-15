#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k0', 'S', 8)
c0 = constant(0, 8)

n0 = k0 + c0

checkResults(n0, k0)

n0.dump('graph.dot')


