#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 7)
c = symbol('c', 'P', 8)
n = Concat(Extract(14, 7, Concat(a, b, c, b)), Extract(14, 8, Concat(a, b, c, a)), Extract(22, 8, Concat(a, b, c, a)), Extract(24, 8, Concat(a, b, c, a, b)))

wres = Concat(c, Extract(6, 0, c), Concat(b, c), Concat(Extract(1, 0, b), c, Extract(7, 1, a)))

checkResults(n, wres, pei = True)

n.dump('graph.dot')


