#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
n = Extract(6, 1, ZeroExt(10, a))

wres = Extract(6, 1, a)

checkResults(n, wres, pei = True)

n.dump('graph.dot')


