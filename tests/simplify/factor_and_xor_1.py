#!/usr/bin/python

from leakage_verif import *


a = symbol('a', 'P', 1)
b = symbol('b', 'P', 1)
c = symbol('c', 'P', 1)
d = symbol('d', 'P', 1)

e = (a & c) ^ d ^ (a & (b ^ c)) ^ (a & b)


checkResults(e, d)

