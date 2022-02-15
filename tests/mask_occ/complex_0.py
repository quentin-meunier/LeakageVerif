#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

p0 = symbol('p0', 'P', 8)
p1 = symbol('p1', 'P', 8)


#                       +
#                    __/ \___
#                   / \   \  \ 
#                  /   &  |   p0
#                  ~  / \/
#                  | /  /\
#                  \ | or \___
#                   \|/ \     \
#                    ^   p1    +
#                   / \       / \
#                 m0   k0    m1  k1

n0 = m0 ^ k0

n1 = ~n0

n2 = n0 | p1

n3 = m1 ^ k1

n4 = n0 & n3

n5 = n1 + n4

n6 = n2 + p0

e = n5 + n6

e.printMaskOcc()
e.dump('graph.dot')



