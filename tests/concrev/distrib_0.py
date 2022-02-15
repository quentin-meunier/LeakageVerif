#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


m0 = symbol('m0', 'M', 4)
m1 = symbol('m1', 'M', 4)
m2 = symbol('m2', 'M', 2)
k0 = symbol('k0', 'S', 4)


e0 = k0 ^ m0

rud, sid = getDistribWithExev(e0)
if rud and sid:
    print('OK')
else:
    print('KO')



e0 = k0 & m0

rud, sid = getDistribWithExev(e0)
if not rud and not sid:
    print('OK')
else:
    print('KO')



e0 = k0 ^ m0 ^ m1

rud, sid = getDistribWithExev(e0)
if rud and sid:
    print('OK')
else:
    print('KO')



e0 = k0 ^ m0 ^ (ZeroExt(2, m2))

rud, sid = getDistribWithExev(e0)
if rud and sid:
    print('OK')
else:
    print('KO')



e0 = (k0 ^ m0) & m1

rud, sid = getDistribWithExev(e0)
if not rud and sid:
    print('OK')
else:
    print('KO')



e0 = k0

rud, sid = getDistribWithExev(e0)
if not rud and not sid:
    print('OK')
else:
    print('KO')



