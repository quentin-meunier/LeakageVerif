#!/usr/bin/python

from leakage_verif import *


a = symbol('a', 'P', 1)
b = symbol('b', 'P', 1)
c = symbol('c', 'P', 1)
d = symbol('d', 'P', 1)

e = (a & b) ^ (a & c)
res = a & (b ^ c)

checkResults(e, res)

