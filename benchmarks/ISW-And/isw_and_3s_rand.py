
from leakage_verif import *


nbExps = 0
nbLeak = 0

firstOrder = True
secondOrder = True

def checkExpLeakageFirstOrder(e0):
    global nbExps
    global nbLeak
    #print('# checkExpLeakage: %s' % e)
    res, usedBitExp, tpsTime = checkTpsVal(e0)
    nbExps += 1
    if not res:
        nbLeak += 1

    if not res:
        print('# Leakage in value for exp num %d' % (nbExps))


def checkExpLeakageSecondOrder(e0, e1):
    global nbExps
    global nbLeak
    #print('# checkExpLeakage: %s' % e)
    res, usedBitExp, tpsTime = checkTpsTrans(e0, e1)
    nbExps += 1
    if not res:
        nbLeak += 1

    if not res:
        print('# Leakage in value for exp num %d' % (nbExps))



def isw_and_3s_norand(m0, m1, m2, m3, z12, z13, z23, r0, r1, r2, r3, r4, r5, k0, k1):
    global nbExps
    global nbLeak

    # computing shares
    a1 = m0
    a2 = m1
    a3 = m0 ^ m1 ^ k0

    b1 = m2
    b2 = m3
    b3 = m2 ^ m3 ^ k1;

    signals = []
    signals.append(a1)
    signals.append(a2)
    signals.append(a3)
    signals.append(b1)
    signals.append(b2)
    signals.append(b3)

    # output c = c1 ^ c2 ^ c3 = a & b

    # a1b1
    a1b1 = a1 & b1
    a1b1 = simplify(a1b1)
    signals.append(a1b1)

    # a1b2 (r0)
    a1r0 = a1 ^ r0
    a1r0 = simplify(a1r0)
    signals.append(a1r0)

    r0b2 = r0 & b2
    r0b2 = simplify(r0b2)
    signals.append(r0b2)

    a1r0b2 = a1r0 & b2
    a1r0b2 = simplify(a1r0b2)
    signals.append(a1r0b2)

    a1b2 = a1r0b2 ^ r0b2
    a1b2 = simplify(a1b2)
    signals.append(a1b2)

    # a1b3 (r1)
    a1r1 = a1 ^ r1
    a1r1 = simplify(a1r1)
    signals.append(a1r1)

    r1b3 = r1 & b3
    r1b3 = simplify(r1b3)
    signals.append(r1b3)

    a1r1b3 = a1r1 & b3
    a1r1b3 = simplify(a1r1b3)
    signals.append(a1r1b3)

    a1b3 = a1r1b3 ^ r1b3
    a1b3 = simplify(a1b3)
    signals.append(a1b3)

    # a2b1 (r2)
    a2r2 = a2 ^ r2
    a2r2 = simplify(a2r2)
    signals.append(a2r2)

    r2b1 = r2 & b1
    r2b1 = simplify(r2b1)
    signals.append(r2b1)

    a2r2b1 = a2r2 & b1
    a2r2b1 = simplify(a2r2b1)
    signals.append(a2r2b1)

    a2b1 = a2r2b1 ^ r2b1
    a2b1 = simplify(a2b1)
    signals.append(a2b1)

    # a2b2
    a2b2 = a2 & b2
    a2b2 = simplify(a2b2)
    signals.append(a2b2)

    # a2b3 (r3)
    a2r3 = a2 ^ r3
    a2r3 = simplify(a2r3)
    signals.append(a2r3)

    r3b3 = r3 & b3
    r3b3 = simplify(r3b3)
    signals.append(r3b3)

    a2r3b3 = a2r3 & b3
    a2r3b3 = simplify(a2r3b3)
    signals.append(a2r3b3)

    a2b3 = a2r3b3 ^ r3b3
    a2b3 = simplify(a2b3)
    signals.append(a2b3)

    # a3b1 (r4)
    a3r4 = a3 ^ r4
    a3r4 = simplify(a3r4)
    signals.append(a3r4)

    r4b1 = r4 & b1
    r4b1 = simplify(r4b1)
    signals.append(r4b1)

    a3r4b1 = a3r4 & b1
    a3r4b1 = simplify(a3r4b1)
    signals.append(a3r4b1)

    a3b1 = a3r4b1 ^ r4b1
    a3b1 = simplify(a3b1)
    signals.append(a3b1)

    # a3b2 (r5)
    a3r5 = a3 ^ r5
    a3r5 = simplify(a3r5)
    signals.append(a3r5)

    r5b2 = r5 & b2
    r5b2 = simplify(r5b2)
    signals.append(r5b2)

    a3r5b2 = a3r5 & b2
    a3r5b2 = simplify(a3r5b2)
    signals.append(a3r5b2)

    a3b2 = a3r5b2 ^ r5b2
    a3b2 = simplify(a3b2)
    signals.append(a3b2)

    # a3b3
    a3b3 = a3 & b3
    a3b3 = simplify(a3b3)
    signals.append(a3b3)

    # zji
    z21i = z12 ^ a1b2
    z21i = simplify(z21i)
    signals.append(z21i)

    z21 = z21i ^ a2b1
    z21 = simplify(z21)
    signals.append(z21)

    z31i = z13 ^ a1b3
    z31i = simplify(z31i)
    signals.append(z31i)

    z31 = z31i ^ a3b1
    z31 = simplify(z31)
    signals.append(z31)

    z32i = z23 ^ a2b3
    z32i = simplify(z32i)
    signals.append(z32i)

    z32 = z32i ^ a3b2
    z32 = simplify(z32)
    signals.append(z32)

    # ci
    c1i = a1b1 ^ z12
    c1i = simplify(c1i)
    signals.append(c1i)

    c1 = c1i ^ z13
    c1 = simplify(c1)
    signals.append(c1)

    c2i = a2b2 ^ z21
    c2i = simplify(c2i)
    signals.append(c2i)

    c2 = c2i ^ z23
    c2 = simplify(c2)
    signals.append(c2)

    c3i = a3b3 ^ z31
    c3i = simplify(c3i)
    signals.append(c3i)

    c3 = c3i ^ z32
    c3 = simplify(c3)
    signals.append(c3)


    if firstOrder:
        print('# First Order Analysis')
        for s0idx in range(len(signals)):
            checkExpLeakageFirstOrder(signals[s0idx])

        print('# Nb. expressions analysed: %d' % nbExps)
        print('# Nb. expressions leaking: %d' % nbLeak)



    if secondOrder:
        nbExps = 0
        nbLeak = 0
        print('# Second Order Analysis')
        for s0idx in range(len(signals)):
            for s1idx in range(s0idx + 1, len(signals)):
                checkExpLeakageSecondOrder(signals[s0idx], signals[s1idx])

        print('# Nb. expressions analysed: %d' % nbExps)
        print('# Nb. expressions leaking: %d' % nbLeak)


    return c1, c2, c3




if __name__ == '__main__':

    testLitteral = False

    if not testLitteral:
        m0 = symbol('m0', 'M', 1)
        m1 = symbol('m1', 'M', 1)
        m2 = symbol('m2', 'M', 1)
        m3 = symbol('m3', 'M', 1)

        z12 = symbol('z12', 'M', 1)
        z13 = symbol('z13', 'M', 1)
        z23 = symbol('z23', 'M', 1)

        r0 = symbol('r0', 'M', 1)
        r1 = symbol('r1', 'M', 1)
        r2 = symbol('r2', 'M', 1)
        r3 = symbol('r3', 'M', 1)
        r4 = symbol('r4', 'M', 1)
        r5 = symbol('r5', 'M', 1)

        k0 = symbol('k0', 'S', 1)
        k1 = symbol('k1', 'S', 1)
 
        c1, c2, c3 = isw_and_3s_norand(m0, m1, m2, m3, z12, z13, z23, r0, r1, r2, r3, r4, r5, k0, k1)

    else:
        def enumerate_values(t, currIdx):
            if currIdx == len(t):
                m0 = constant(t[0], 1)
                m1 = constant(t[1], 1)
                m2 = constant(t[2], 1)
                m3 = constant(t[3], 1)
                z12 = constant(t[4], 1)
                z13 = constant(t[5], 1)
                z23 = constant(t[6], 1)
                r0 = constant(t[7], 1)
                r1 = constant(t[8], 1)
                r2 = constant(t[9], 1)
                r3 = constant(t[10], 1)
                r4 = constant(t[11], 1)
                r5 = constant(t[12], 1)
                k0 = constant(t[13], 1)
                k1 = constant(t[14], 1)

                c1, c2, c3 = isw_and_3s_norand(m0, m1, m2, m3, z12, z13, z23, r0, r1, r2, r3, r4, r5, k0, k1)
 
                r_ref = k0 & k1
                r_ref = simplify(r_ref)
                r = c1 ^ c2 ^ c3
                r = simplify(r)

                # Comparing strings ('0' or '1')  because of the two different implementations (either use 'is' or '==')
                if '%s' % r_ref != '%s' % r:
                    print('*** Error for values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s): result is %s instead of %s' % (m0, m1, m2, m3, z12, z13, z23, r0, r1, r2, r3, r4, r5, k0, k1, r, r_ref))
                    sys.exit(0)
            else:
                t[currIdx] = 0
                enumerate_values(t, currIdx + 1)
                t[currIdx] = 1
                enumerate_values(t, currIdx + 1)

        t = [0] * 15
        enumerate_values(t, 0)
        print('[OK]')


