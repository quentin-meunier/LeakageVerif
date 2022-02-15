#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0xA5, 8)

c = ~c0

res = constant(0x5A, 8)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


