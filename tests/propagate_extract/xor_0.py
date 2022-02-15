#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)

b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
bxc = Extract(1, 1, b ^ c)

n = Extract(0, 0, Extract(0, 0, Extract(0, 0, bxc ^ Extract(0, 0, Extract(0, 0, Extract(0, 0, a)) ^ bxc))))

wres = Extract(0, 0, a)

checkResults(n, wres, pei = True)



