#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


# &          &
#  \          \
#   \     ->   \
#    \          \
#     ^          ~
#    /|\         |
#   0 k 1        k


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

c0 = constant(0, 8)
c1 = constant(255, 8)

n0 = c0 ^ k0 ^ c1
n1 = n0 & k1

res0 = ~k0
wres = res0 & k1

checkResults(n1, wres)

n1.dump('graph.dot')


