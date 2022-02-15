#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 4)
q = symbol('q', 'P', 4)
r = symbol('r', 'P', 4)

c0 = Const(1, 4)

n0 = p ^ q
n1 = n0 >> c0
n2 = n1 ^ r

n2.dump('graph.dot')

