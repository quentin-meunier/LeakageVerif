# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LIP6DROMEL project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function

from leakage_verif import *


nbExps = 0
nbLeak = 0

def checkExpLeakage(e):
    global nbExps
    global nbLeak

    nbExps += 1

    res, wordRes, niTime = checkTpsVal(e)
    if not res:
        nbLeak += 1
        print('# Leakage in value for exp num %d (Total leaks : %d)' % (nbExps, nbLeak))



def gmul(a, b):
    p = constant(0, 8) # the product of the multiplication
    for i in range(8):
        # p = (((unsigned char) (((signed char) ((b & 1) << 7)) >> 7)) & a) ^ p;
        e0 = b & constant(1, 8)
        e0 = simplify(e0)
        checkExpLeakage(e0)
        e1 = e0 << 7
        e1 = simplify(e1)
        checkExpLeakage(e1)
        e2 = e1 >> 7
        e2 = simplify(e2)
        checkExpLeakage(e2)
        e3 = e2 & a
        e3 = simplify(e3)
        checkExpLeakage(e3)
        e4 = e3 ^ p
        e4 = simplify(e4)
        checkExpLeakage(e4)
        p = e4

        # a = (a << 1) ^ (((unsigned char) (((signed char) (a & 0x80)) >> 7)) & 0x11b);
        e0 = a << 1
        e0 = simplify(e0)
        checkExpLeakage(e0)
        e1 = a & constant(0x80, 8)
        e1 = simplify(e1)
        checkExpLeakage(e1)
        e2 = e1 >> 7
        e2 = simplify(e2)
        checkExpLeakage(e2)
        e3 = e2 & constant(0x1b, 8)
        e3 = simplify(e3)
        checkExpLeakage(e3)
        e4 = e0 ^ e3
        e4 = simplify(e4)
        checkExpLeakage(e4)
        a = e4

        if i != 7:
            # b >>= 1;
            e0 = b >> 1
            e0 = simplify(e0)
            checkExpLeakage(e0)
            b = e0

    return p



def secmult():

    testLitteral = False

    if not testLitteral:
        m0 = symbol('m0', 'M', 8)
        m1 = symbol('m1', 'M', 8)
        m01 = symbol('m01', 'M', 8)

        k0 = symbol('k0', 'S', 8)
        k1 = symbol('k1', 'S', 8)
    else:
        m0 = constant(0xb9, 8)
        m1 = constant(0x66, 8)
        m01 = constant(0x37, 8)

        k0 = constant(0xa1, 8)
        k1 = constant(0x0f, 8)

    
    a1 = m0 ^ k0
    b1 = m1 ^ k1

    # start analysis
    
    e0 = m01 ^ gmul(m0, b1)
    e0 = simplify(e0)
    checkExpLeakage(e0)
    e1 = gmul(a1, m1)
    e1 = simplify(e1)
    checkExpLeakage(e1)
    m10 = e0 ^ e1
    m10 = simplify(m10)
    checkExpLeakage(m10)

    c0 = gmul(m0, m1)
    c0 = simplify(c0)
    checkExpLeakage(c0)
    c0 = c0 ^ m01
    c0 = simplify(c0)
    checkExpLeakage(c0)

    c1 = gmul(a1, b1)
    c1 = simplify(c1)
    checkExpLeakage(c1)
    c1 = c1 ^ m10
    c1 = simplify(c1)
    checkExpLeakage(c1)

    # end analysis

    if testLitteral:
        print('c0 = 0x%x' % int(str(c0)))
        print('c1 = 0x%x' % int(str(c1)))
        print('c0 ^ c1 = 0x%x' % (int(str(simp(c0 ^ c1)))))
        print('k0 * k1 = 0x%x' % (int(str(gmul(k0, k1)))))


if __name__ == '__main__':
    nbExps = 0
    nbLeak = 0
    secmult()
    print('# Total Nb. of expression analysed: %d' % nbExps)
    print('# Total Nb. of potential leakages found: %d' % nbLeak)




