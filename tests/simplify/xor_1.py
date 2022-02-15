#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


# k0 ^ k0 ^ m0

k0 = symbol('k0', 'S', 8)

m0 = symbol('m0', 'M', 8)

n0 = k0 ^ m0
n1 = n0 ^ k0

# Result is m0
checkResults(n1, m0)


