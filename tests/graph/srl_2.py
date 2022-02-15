#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 4)
q = symbol('q', 'P', 4)
r = symbol('r', 'P', 4)

c0 = Const(1, 4)
c1 = Const(2, 4)

n0 = p ^ q
n1 = LShR(n0, c1)
n2 = n1 ^ r
n3 = LShR(n0, c0)
n4 = n2 ^ n3

n4.dump('graph.dot')

