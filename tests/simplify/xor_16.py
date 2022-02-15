#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

# (3 | (e ^ e)) ^ (4 | (f ^ f))

p = symbol('p', 'P', 4)
q = symbol('q', 'P', 4)

c0 = constant(15, 4)
c1 = constant(12, 4)


n = (c0 | (p ^ p)) ^ (c1 | (q ^ q))

wres = constant(3, 4)

checkResults(n, wres)

n.dump('graph.dot')


