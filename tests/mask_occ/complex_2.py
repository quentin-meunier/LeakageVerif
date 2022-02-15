#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m0 = symbol('m0', 'M', 8)

k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

p0 = symbol('p0', 'P', 8)

#                     &
#                    / \
#                    \   +
#                     \ / \
#                      ^   p0
#                     / \
#                    /   k1
#                    ~
#                    |
#                    ^
#                   / \
#                 m0   k0

n0 = m0 ^ k0

n1 = ~n0

n2 = n1 ^ k1

n3 = n2 + p0

e = n3 & n2

e.printMaskOcc()

res = tps(e)

print(res)




