#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


s0 = symbol('s0', 'S', 4)
m0 = symbol('m0', 'M', 4)
n1 = s0 ^ m0

m1 = symbol('m1', 'M', 4)
n2 = m0 ^ m1

e2 = n1 ^ n2

e2.dump('graph0.dot')

e2 = simplify(e2)

e2.dump('graph1.dot')


