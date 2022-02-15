#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


p = symbol('p', 'P', 8)
m = symbol('m', 'M', 1)

n = Extract(7, 0, ZeroExt(24, p) ^ ZeroExt(31, m))

n = simplify(n)



# FIXME: how to check the result?



