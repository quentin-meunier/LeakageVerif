#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

k = symbol('k', 'S', 4)
m = symbol('m', 'M', 4)

e = (m ^ k) & m

e.dump('graph.dot')



