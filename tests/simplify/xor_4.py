#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


# &          &
#  \          \
#   \     ->   ~
#    \          \
#     ^          ^
#    /|\         |\
#   1          



k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

c0 = constant(255, 8)

n0 = k0 ^ k1 ^ c0
n1 = n0 & k0

res0 = k0 ^ k1
res1 = ~res0
wres = res1 & k0

checkResults(n1, wres)

n1.dump('graph.dot')


