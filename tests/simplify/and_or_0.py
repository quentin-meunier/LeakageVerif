#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


a = symbol('a', 'P', 8)
b = symbol('b', 'P', 8)
c = symbol('c', 'P', 8)
d = symbol('d', 'P', 8)
e = symbol('e', 'P', 8)


n0 = (~a & b) | (~a & ~b & c) | (~a & ~b & ~c & d) | (a + b + c) | (~a & ~b & ~c & ~d & e) | a
res = b | c | d | e | (a + b + c) | a

checkResults(n0, res)

n0.dump('graph.dot')


