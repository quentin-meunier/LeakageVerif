#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

#    root       root
#     ^          m
#    /|\   ->
#   k m k


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

n0 = k0 ^ k1 ^ k0

wres = k1

checkResults(n0, wres)

n0.dump('graph.dot')


