#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
n0 = k ^ k
n1 = k ^ k

if equivalence(n0, n1):
    print('OK')
else:
    print('KO')


