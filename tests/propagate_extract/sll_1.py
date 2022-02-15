#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(9, 0, a << 10)

wres = constant(0, 10)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


