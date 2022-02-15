#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(26, 5, a << 10)

wres = Concat(Extract(16, 0, a), Const(0, 5))

checkResults(n, wres, pei = True)

a.dump('graph.dot')


