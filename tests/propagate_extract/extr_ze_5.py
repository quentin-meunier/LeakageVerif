#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
n = Extract(17, 8, ZeroExt(10, a))

wres = constant(0, 10)

checkResults(n, wres, pei = True)

n.dump('graph.dot')


