#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

p = symbol('p', 'P', 8)
q = symbol('q', 'P', 8)

c0 = constant(0xA0, 8)
c1 = constant(0x0A, 8)
c2 = constant(0xAA, 8)

n = c0 & p & c1 & q & c2

wres = constant(0, 8)

checkResults(n, wres)


