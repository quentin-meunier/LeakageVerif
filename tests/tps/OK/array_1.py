#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

m = symbol('m', 'M', 3)
k = symbol('k', 'S', 3)
p = symbol('p', 'P', 3)
a = ArrayExp('a', 3, 3)

e = m ^ a[((k ^ m) << 1) ^ (m << 1) ^ p]

checkTpsResult(e, True)

