#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c1 = constant(0x84, 8)

c = SignExt(8, c1)

res = constant(0xFF84, 16)

if equivalence(c, res):
    print('OK')
else:
    print('KO')



c = SignExt(7, constant(1, 1))
res = constant(0xFF, 8)
if equivalence(c, res):
    print('OK')
else:
    print('KO')


