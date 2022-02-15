#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 4)

e = a - a

print('%s' % getBitDecomposition(e))



