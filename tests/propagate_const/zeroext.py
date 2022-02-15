#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c1 = constant(0x84, 8)

c = ZeroExt(8, c1)

res = constant(0x84, 16)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


