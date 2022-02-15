#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


s = symbol('s', 'S', 8)
m = symbol('m', 'M', 8)


n = (s ^ m) >> 4

n.dump('graph.dot')



