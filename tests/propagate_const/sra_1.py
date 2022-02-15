#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0x78, 8)

c = c0 >> 1

res = constant(0x3C, 8)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


