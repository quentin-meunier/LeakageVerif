#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s0 = symbol('s', 'S', 4)
m0 = symbol('m', 'M', 4)

c1 = Const(1, 4)

n0 = s0 >> c1
n1 = n0 ^ m0

n1.dump('graph.dot')

