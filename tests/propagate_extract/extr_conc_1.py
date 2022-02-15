#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 7)
c = symbol('c', 'P', 8)
n = Extract(7, 7, Concat(a, b, Extract(0, 0, Extract(0, 0, Extract(7, 7, Concat(b, a ^ c, b)))), b))

wres = Extract(0, 0, a) ^ Extract(0, 0, c)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


