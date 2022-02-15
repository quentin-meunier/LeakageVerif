#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)
e = symbol('e', 'P', 8)
f = symbol('f', 'P', 8)


n0 = (~a & ~b & ~c & ~d & e) | (~a & ~b & ~c & d) | (~a & ~b & ~c & ~d & ~e & f) | (~a & ~b & c) | (~a & b) | a | ~f
res = constant(0xff, 8)

checkResults(n0, res)

n0.dump('graph.dot')


