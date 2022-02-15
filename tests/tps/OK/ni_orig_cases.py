#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)
k2 = symbol('k2', 'S', 8)

m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)
m2 = symbol('m2', 'M', 8)

p0 = symbol('p0', 'P', 8)
p1 = symbol('p1', 'P', 8)
p2 = symbol('p2', 'P', 8)



setSimplifyStrategy('FAIL')

def check(n, val):
    res = tps(n)
    #if res == val:
    #    print('[OK]')
    #else:
    #    print('[KO] %s' % n)

#n = (m0 & k0)
#check(n, False)
#
#n = (~m0 & k0)
#check(n, False)
#
#n = (~~m0 & k0)
#check(n, False)
#
#n = (~~~m0 & k0)
#check(n, False)
#
#n = (k0 & (p0 ^ m0))
#check(n, False)
#
#n = (k0 & (p0 ^ ~m0))
#check(n, False)
#
#n = (k0 & (p0 ^ ~~m0))
#check(n, False)
#
#
#
#n = (m0 ^ k0)
#check(n, True)
#
#n = (~m0 ^ k0)
#check(n, True)
#
#n = (~~m0 ^ k0)
#check(n, True)
#
#n = (~~~m0 ^ k0)
#check(n, True)
#
#n = (k0 ^ (p0 ^ m0))
#check(n, True)
#
#n = (k0 ^ (p0 ^ ~m0))
#check(n, True)
#
#n = (k0 ^ (p0 ^ ~~m0))
#check(n, True)
#
#
#
#n = (m1 ^ k1) & (m0 ^ k0)
#check(n, True)
#
#n = (m1 ^ k1) & (~m0 ^ k0)
#check(n, True)
#
#n = (m1 ^ k1) & (~~m0 ^ k0)
#check(n, True)
#
#n = (m1 ^ k1) & (~~~m0 ^ k0)
#check(n, True)
#
#n = (m1 ^ k1) & (k0 ^ (p0 ^ m0))
#check(n, True)
#
#n = (m1 ^ k1) & (k0 ^ (p0 ^ ~m0))
#check(n, True)
#
#n = (m1 ^ k1) & (k0 ^ (p0 ^ ~~m0))
#check(n, True)
#
#
#
#n = ((m0 ^ k0) & p0) & k2
#check(n, False)


#n = (~((m0 ^ k0) + (k1 & m1)) & p1) ^ (m1 ^ k2)
#check(n, True)

#n = (~((m0 ^ k0) + (k1 & m0)) & p1) ^ (m0 ^ k2)
#check(n, False)

while True:
    n = (~((m0 ^ k0) + (k1 & m1)) & p1) ^ (m0 ^ k0)
    check(n, False)

#n = (~((m0 ^ k0) + (k1 ^ m1)) & p1) ^ (m0 ^ k0)
#check(n, True)




