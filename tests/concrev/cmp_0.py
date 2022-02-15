#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m0 = Symb('m0', 'M', 8)



e0 = Extract(Const(7, 3), Const(0, 0), (ZeroExt(Const(24, 5), m0) << Const(1, 1)))
e1 = Concat(Extract(6, 0, m0), Const(0, 1))

r, v0, v1 = compareExpsWithExev(e0, e1)
if r == None:
    print('OK')
else:
    print('KO')



