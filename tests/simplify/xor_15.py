#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

#      /        /
#     ^        /  
#    / \   -> /
#   ~a  1    a


k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)

c = constant(255, 8)

n0 = ~k ^ c
n1 = n0 & p

wres = k & p

checkResults(n1, wres)

n1.dump('graph.dot')


