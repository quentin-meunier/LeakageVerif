#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
n = Extract(0, 0, Extract(0, 0, Extract(0, 0, Extract(0, 0, Extract(0, 0, a)))
                              ^ Extract(0, 0, Extract(0, 0, Extract(0, 0, b)))))

wres = Extract(0, 0, a ^ b)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


