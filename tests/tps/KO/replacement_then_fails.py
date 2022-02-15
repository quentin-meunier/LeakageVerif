#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s = symbol('s', 'S', 1)
t = symbol('t', 'S', 1)
u = symbol('u', 'S', 1)

r = symbol('r', 'M', 1)

n = (s ^ r ^ t) & u

checkTpsResult(n, False)





