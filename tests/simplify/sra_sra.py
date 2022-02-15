#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)

n = LShR(LShR(LShR(p, 1), 2), 3) + LShR(LShR(LShR(LShR(p, 1), 0), 3), 1)


res = LShR(p, 6) + LShR(p, 5)

checkResults(n, res)

n.dump('graph.dot')


