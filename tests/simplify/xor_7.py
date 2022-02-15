#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


# &          &
#  \          \
#   \     ->   \
#    \          \
#     ^          \
#    /|\          \
#   m m k          k



k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
k2 = symbol('k2', 'S', 8)

n0 = k0 ^ k0 ^ k1
n1 = n0 & k2

wres = k1 & k2

checkResults(n1, wres)

n1.dump('graph.dot')


