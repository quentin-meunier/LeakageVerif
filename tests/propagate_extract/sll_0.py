#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(26, 20, a << 10)

wres = Extract(16, 10, a)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


