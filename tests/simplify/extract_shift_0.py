#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k = symbol('k', 'S', 8)
n1 = Extract(7, 7, k >> 1)

r = Extract(7, 7, k)
checkResults(n1, r)



