
from leakage_verif import *


nbExps = 0
nbLeak = 0

firstOrder = True
secondOrder = True

def checkExpLeakageFirstOrder(e0):
    global nbExps
    global nbLeak
    #print('# checkExpLeakage: %s' % e0)
    res, usedBitExp, tpsTime = checkTpsVal(e0)
    nbExps += 1
    if not res:
        nbLeak += 1

    if not res:
        print('# Leakage exp num %d' % (nbExps))


def checkExpLeakageSecondOrder(e0, e1):
    global nbExps
    global nbLeak
    #print('# checkExpLeakage: (%s, %s)' % (e0, e1))
    res, usedBitExp, tpsTime = checkTpsTrans(e0, e1)
    nbExps += 1
    if not res:
        nbLeak += 1

    if not res:
        print('# Leakage for exp num %d' % (nbExps))



def isw_and_2s_norand(m0, m1, z12, k0, k1):
    global nbExps
    global nbLeak

    # computing shares
    a1 = m0
    a2 = m0 ^ k0

    b1 = m1
    b2 = m1 ^ k1;

    signals = []
    signals.append(a1)
    signals.append(a2)
    signals.append(b1)
    signals.append(b2)

    # output c = c1 ^ c2 = a & b

    # start analysis
    a1b1 = a1 & b1
    a1b1 = simplify(a1b1)
    signals.append(a1b1)

    a1b2 = a1 & b2
    a1b2 = simplify(a1b2)
    signals.append(a1b2)

    a2b1 = a2 & b1
    a2b1 = simplify(a2b1)
    signals.append(a2b1)

    a2b2 = a2 & b2
    a2b2 = simplify(a2b2)
    signals.append(a2b2)


    z21i = z12 ^ a1b2
    z21i = simplify(z21i)
    signals.append(z21i)

    z21 = z21i ^ a2b1
    z21 = simplify(z21)
    signals.append(z21)


    c1 = a1b1 ^ z12
    c1 = simplify(c1)
    signals.append(c1)

    c2 = a2b2 ^ z21
    c2 = simplify(c2)
    signals.append(c2)


    if firstOrder:
        nbExps = 0
        nbLeak = 0
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


    return c1, c2




if __name__ == '__main__':

    testLitteral = False

    if not testLitteral:
        m0 = symbol('m0', 'M', 1)
        m1 = symbol('m1', 'M', 1)

        z12 = symbol('z12', 'M', 1)

        k0 = symbol('k0', 'S', 1)
        k1 = symbol('k1', 'S', 1)
        
        c1, c2 = isw_and_2s_norand(m0, m1, z12, k0, k1)

    else:
        def enumerate_values(t, currIdx):
            if currIdx == len(t):
                m0 = constant(t[0], 1)
                m1 = constant(t[1], 1)
                z12 = constant(t[2], 1)
                k0 = constant(t[3], 1)
                k1 = constant(t[4], 1)

                c1, c2 = isw_and_2s_norand(m0, m1, z12, k0, k1)
 
                r_ref = k0 & k1
                r_ref = simplify(r_ref)
                r = c1 ^ c2
                r = simplify(r)

                # Comparing strings ('0' or '1')  because of the two different implementations (either use 'is' or '==')
                if '%s' % r_ref != '%s' % r:
                    print('*** Error for values (%s, %s, %s, %s, %s): result is %s instead of %s' % (m0, m1, z12, k0, k1, r, r_ref))
                    sys.exit(0)
            else:
                t[currIdx] = 0
                enumerate_values(t, currIdx + 1)
                t[currIdx] = 1
                enumerate_values(t, currIdx + 1)

        t = [0] * 5
        enumerate_values(t, 0)
        print('[OK]')


