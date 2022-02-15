#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

# m0 ^ m0

m0 = symbol('m0', 'M', 8)
n0 = m0 ^ m0

# result is 0
wres = constant(0, 8)

checkResults(n0, wres)


