#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *

s0 = symbol('s0', 'S', 4)
m0 = symbol('m0', 'M', 4)
p0 = symbol('p0', 'P', 4)

c0 = Const(-8, 4)
c1 = Const(8, 4)

x = c0 ^ c1
a = p0 & m0
o = x | s0
n = a ^ o

n.dump('graph.dot')

print('OK')

