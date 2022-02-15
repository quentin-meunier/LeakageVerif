#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


c0 = constant(0xF0, 8)

c = c0 >> 2

res = constant(0xFC, 8)

c.dump('graph.dot')

if equivalence(c, res):
    print('OK')
else:
    print('KO')


