#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
n = Extract(8, 0, ZeroExt(10, a))

wres = Concat(constant(0, 1), a)

checkResults(n, wres, pei = True)

n.dump('graph.dot')


