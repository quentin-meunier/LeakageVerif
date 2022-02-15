#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(-1, 8)
c1 = constant(-5, 8)

c = -c0 - -c1

res = constant(0xFC, 8) # -(-1) - -(-5) = -4


if equivalence(c, res):
    print('OK')
else:
    print('KO')


