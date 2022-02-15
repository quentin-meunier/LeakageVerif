#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



a = symbol('a', 'S', 2)
b = symbol('b', 'S', 2)
c = symbol('c', 'S', 2)
d = symbol('d', 'S', 2)
f = symbol('f', 'S', 2)
z = constant(0, 2)

n1 = a ^ b ^ c ^ a ^ b # c
n2 = c ^ c             # 0
n3 = z + c + n2        # c
n4 = n1 & n3 & c       # c

n5 = c ^ d ^ f ^ d     # c ^ f
n6 = a ^ a             # 0
n7 = n5 + n6           # c ^ f
n8 = c ^ f             # c ^ f
n9 = c ^ f             # c ^ f
n10 = n8 & n9          # c ^ f
n11 = n7 | n10         # c ^ f
n12 = n4 ^ n11         # f

# Result is f
wres = f

n12.dump('graph.dot')

checkResults(n12, wres)



