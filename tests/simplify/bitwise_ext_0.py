#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)
m = symbol('m', 'M', 8)

n0 = Extract(7, 0, ZeroExt(24, k) ^ ZeroExt(24, p) ^ ZeroExt(24, m))
n1 = Extract(7, 0, SignExt(24, k) ^ SignExt(24, p) ^ SignExt(24, m))
n = n0 ^ n1

wres = constant(0, 8)

checkResults(n, wres)



