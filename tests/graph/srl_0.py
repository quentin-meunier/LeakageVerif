#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s0 = symbol('s', 'S', 4)
c0 = Const(1, 4)
c1 = Const(2, 4)
c2 = Const(3, 4)

n0 = LShR(s0, c0)
n1 = LShR(s0, c1)
n2 = LShR(s0, c2)

n3 = s0 & n0 & n1 & n2
n3.dump('graph.dot')


