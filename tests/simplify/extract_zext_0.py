#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)
e = ZeroExt(24, p)

n = Extract(30, 23, e)

wres = constant(0, 8)

checkResults(n, wres)

n.dump('graph.dot')


