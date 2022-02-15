#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


#  &       &
#  |       |
#  ~   ->  |
#  |       |
#  ~       |
#  |       |
#  k       k


k0 = symbol('k0', 'S', 8)

n0 = ~k0
n1 = ~n0

wres = k0

checkResults(n1, wres)

n1.dump('graph.dot')


