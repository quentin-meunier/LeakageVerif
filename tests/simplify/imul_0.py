#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)


r = a ** b + a ** c


res = a ** (b + c)

checkResults(r, res)



