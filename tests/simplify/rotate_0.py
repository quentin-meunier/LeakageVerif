#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0x12345678, 32)
n = RotateRight(c0, 8)

res = constant(0x78123456, 32)

checkResults(n, res)

n.dump('graph.dot')


