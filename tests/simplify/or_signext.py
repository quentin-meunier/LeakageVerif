#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


k = symbol('k', 'S', 8)
p = symbol('p', 'P', 8)
m = symbol('m', 'M', 8)

n = SignExt(24, k) | SignExt(24, p) | SignExt(24, m)

wres = SignExt(24, k | p | m)

checkResults(n, wres)



