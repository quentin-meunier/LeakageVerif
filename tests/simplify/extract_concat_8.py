#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)
p0 = Extract(0, 0, p)
n1 = Extract(6, 0, Concat(p0, p0, p0, p0, p0, p0, p0, p0))

res = Concat(p0, p0, p0, p0, p0, p0, p0)

checkResults(n1, res)

n1.dump('graph.dot')


