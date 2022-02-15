#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 1)

n = Extract(7, 0, SignExt(31, p))

wres = SignExt(7, p)

checkResults(n, wres)

n.dump('graph.dot')


