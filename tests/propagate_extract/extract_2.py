#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

a = symbol('a', 'P', 8)
n = Extract(0, 0, Extract(0, 0, Extract(0, 0, Extract(0, 0, ~a))))

wres = ~Extract(0, 0, a)


checkResults(n, wres, pei = True)



