#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(26, 5, a >> 10)

a31 = Extract(31, 31, a)

wres = Concat(a31, a31, a31, a31, a31, Extract(31, 15, a))

checkResults(n, wres, pei = True)



