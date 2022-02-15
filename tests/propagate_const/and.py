#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0xA5, 8)
c1 = constant(0xF0, 8)

c = c0 & c1

res = constant(0xA0, 8)

if equivalence(c, res):
    print('OK')
else:
    print('KO')


