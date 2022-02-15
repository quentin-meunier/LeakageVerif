#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

#    root       root
#     ^          1
#    /|\   ->
#   m 1 m


k0 = symbol('k0', 'S', 8)

c0 = constant(255, 8)

n0 = k0 ^ c0 ^ k0

wres = c0

checkResults(n0, wres)

n0.dump('graph.dot')


