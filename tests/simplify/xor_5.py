#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

#    root       root
#     ^          ~
#    /|\   ->    |
#   1            ^
#                |\


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

c0 = constant(255, 8)

n0 = k0 ^ k1 ^ c0

res0 = k0 ^ k1
wres = ~res0

checkResults(n0, wres)

n0.dump('graph.dot')


