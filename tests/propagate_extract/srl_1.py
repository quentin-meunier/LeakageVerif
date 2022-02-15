#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(29, 22, LShR(a, 10))

wres = Const(0, 8)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


