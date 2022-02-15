#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 32)
n = Extract(2, 1, Extract(15, 8, p))

wres = Extract(10, 9, p)

checkResults(n, wres)

n.dump('graph.dot')


