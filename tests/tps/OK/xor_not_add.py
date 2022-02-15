#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

m = symbol('m', 'M', 8)

n = ~(k0 ^ m) + k1

#n.dump('graph.dot', True)

checkTpsResult(n, True)





