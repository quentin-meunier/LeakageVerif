#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)
m = symbol('m', 'M', 8)

n = ZeroExt(24, k) ^ ZeroExt(24, p) ^ ZeroExt(24, m)

wres = ZeroExt(24, k ^ p ^ m)

checkResults(n, wres)



