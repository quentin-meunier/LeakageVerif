#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 2)
q = symbol('q', 'P', 2)
r = symbol('r', 'P', 2)

n = -q + -p + q - r + p + (p - q) + r - p

wres = -q

checkResults(n, wres)

n.dump('graph.dot')


