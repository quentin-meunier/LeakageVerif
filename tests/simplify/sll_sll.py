#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)

n = (((p << 1) << 2) << 3) + ((((p << 1) << 0) << 3) << 1)


res = (p << 6) + (p << 5)

checkResults(n, res)

n.dump('graph.dot')


