#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


s = symbol('s', 'S', 4)
m = symbol('m', 'M', 4)

n = SignExt(8, s ^ m)

n.dump('graph.dot')



