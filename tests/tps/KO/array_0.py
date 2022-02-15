#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

m = Symb('m', 'M', 3)
k = Symb('k', 'S', 3)
a = ArrayExp('a', 3, 3)

e = m ^ a[k ^ m]

checkTpsResult(e, False)

