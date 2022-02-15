#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


s = symbol('s', 'S', 3)
m = symbol('m', 'M', 3)
p = symbol('p', 'P', 3)


n = (s ^ m) + p

n.dump('graph.dot')



