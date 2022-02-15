#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k = symbol('k', 'S', 32)
k0 = Extract(15, 8, k)
p = symbol('p', 'P', 8)
n = k0 ^ p


n.dump('graph.dot')


