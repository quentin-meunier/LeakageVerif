#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0xF0, 8)

c = LShR(c0, 2)

res = constant(0x3C, 8)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


