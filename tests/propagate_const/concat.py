#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

c0 = constant(0x12, 8)
c1 = constant(0x34, 8)
c2 = constant(0x56, 8)
c3 = constant(0x78, 8)

c = Concat(c0, c1, c2, c3)

res = constant(0x12345678, 32)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


