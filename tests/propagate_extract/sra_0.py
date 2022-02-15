#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 32)

n = Extract(19, 5, a >> 10)

wres = Extract(29, 15, a)

checkResults(n, wres, pei = True)

a.dump('graph.dot')


