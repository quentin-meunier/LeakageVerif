#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
c = symbol('c', 'P', 8)
n = Extract(7, 0, ZeroExt(10, Extract(7, 0, ZeroExt(10, a ^ c))))

wres = a ^ c

checkResults(n, wres, pei = True)

n.dump('graph.dot')


