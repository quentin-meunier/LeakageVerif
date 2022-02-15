#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s = Symb('s', 'S', 1)

r = Symb('r', 'M', 1)

n = s ^ r ^ r

checkTpsStrategies(n.wordGraph, False, TpsOrig = True)
checkTpsStrategies(n.wordGraph, False)





