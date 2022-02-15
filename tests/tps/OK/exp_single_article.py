#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

# Example from he MaskVerif article (page 14)

s0 = symbol('s0', 'S', 1)
s1 = symbol('s1', 'S', 1)
s2 = symbol('s2', 'S', 1)
s3 = symbol('s3', 'S', 1)
s5 = symbol('s5', 'S', 1)
s6 = symbol('s6', 'S', 1)
s7 = symbol('s7', 'S', 1)

r0 = symbol('r0', 'M', 1)
r1 = symbol('r1', 'M', 1)
r2 = symbol('r2', 'M', 1)
r3 = symbol('r3', 'M', 1)
r4 = symbol('r4', 'M', 1)
r5 = symbol('r5', 'M', 1)
r6 = symbol('r6', 'M', 1)
r7 = symbol('r7', 'M', 1)

n0 = r7 ^ r6 ^ r5 ^ r2 ^ r1 ^ r0 ^ r6 ^ r5 ^ r4 ^ r0
n1 = r3 ^ s6 ^ r1 ^ s7 ^ r0 ^ s0 ^ r7 ^ s3 ^ r4 ^ s7 ^ r0
n2 = r7 ^ r6 ^ r5 ^ r2 ^ r1 ^ r0
n3 = r3 ^ s6 ^ r1 ^ s7 ^ r0 ^ s0 ^ r7 ^ s3 ^ r4
n4 = r7 ^ r6 ^ r5 ^ r2 ^ r1 ^ r0 ^ r6 ^ r5 ^ r1 ^ r0
n5 = r6 ^ r5 ^ r4 ^ r0 ^ r7 ^ r6 ^ r5 ^ r0
n6 = r3 ^ s6 ^ r1 ^ s7 ^ r0 ^ s0 ^ r7 ^ s3 ^ r4 ^ s1 ^ r6 ^ s2 ^ r5 ^ s7 ^ r0
n7 = s7 ^ r0 ^ s5 ^ r2 ^ s6 ^ r1 ^ s7 ^ r0 ^ s1 ^ r6 ^ r3
n8 = r6 ^ r5 ^ r4 ^ r0 ^ r7 ^ r6 ^ r5 ^ r0
n9 = s7 ^ r0 ^ s5 ^ r2 ^ s6 ^ r1 ^ s7 ^ r0 ^ s1 ^ r6 ^ r3

n10 = n0 & n1
n11 = n2 & n3
n12 = n4 ^ n5
n13 = n6 ^ n7
n14 = n8 & n9
n15 = n12 & n13
n16 = n14 & n15
e   = n10 ^ n11 ^ n16

checkTpsResult(e, True)



