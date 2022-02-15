#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *



k0 = symbol('k0', 'S', 8)
k1 = symbol('k1', 'S', 8)

m1 = symbol('m1', 'M', 8)


e0 = ZeroExt(24, k0)
e1 = SignExt(31, (Extract(0, 0, m1) ^ Extract(0, 0, k1)))


res, time = checkTpsTransXorBit(e0, e1)

print('TPS : %r' % res)


