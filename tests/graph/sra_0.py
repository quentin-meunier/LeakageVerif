#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s0 = symbol('s', 'S', 4)
c1 = Const(1, 4)
c2 = Const(2, 4)
c3 = Const(3, 4)

n0 = s0 >> c1
n1 = s0 >> c2
n2 = s0 >> c3

n3 = s0 & n0 & n1 & n2

n3.dump('graph.dot')


