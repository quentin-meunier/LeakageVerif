#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)
e = SignExt(24, p)

n = Extract(30, 23, e)

wres = SignExt(7, Extract(7, 7, p))

checkResults(n, wres)

n.dump('graph.dot')


