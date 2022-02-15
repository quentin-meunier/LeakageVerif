#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m0 = symbol('m0', 'M', 8)
m1 = symbol('m1', 'M', 8)
k1 = symbol('k1', 'S', 8)



exp_0 = ((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(27, 5)) ^ Concat(Extract(Const(3, 2), Const(0, 0), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))) & SignExt(Const(7, 5), (Extract(Const(4, 3), Const(4, 3), m1) ^ Extract(Const(4, 3), Const(4, 3), k1)))


exp_1 = (Concat((Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0)), (Extract(Const(7, 3), Const(7, 3), m0) ^ Extract(Const(3, 2), Const(3, 2), m0))) & Const(27, 8)) ^ Concat(((Concat(Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0), Extract(Const(4, 3), Const(4, 3), m0)) & Const(27, 7)) ^ Concat(((Concat(Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0), Extract(Const(5, 3), Const(5, 3), m0)) & Const(27, 6)) ^ Concat(((Concat(Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0), Extract(Const(6, 3), Const(6, 3), m0)) & Const(27, 5)) ^ Concat(((Concat(Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0), Extract(Const(7, 3), Const(7, 3), m0)) & Const(11, 4)) ^ Concat(Extract(Const(2, 2), Const(0, 0), m0), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))), Const(0, 1))

rud, sid = getDistribWithExev(exp_0)
print('LV exp 0')
print('RUD: %r' % rud)
print('SID: %r' % sid)


rud, sid = getDistribWithExev(exp_1)
print('LV exp 1')
print('RUD: %r' % rud)
print('SID: %r' % sid)


rud, sid = getDistribWithExev(exp_0 ^ exp_1)
print('LV exp 0 ^ exp 1')
print('RUD: %r' % rud)
print('SID: %r' % sid)




