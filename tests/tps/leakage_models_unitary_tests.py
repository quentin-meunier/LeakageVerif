#!/usr/bin/python

from __future__ import print_function

from leakage_verif import *


numTests = 9
leakageModels = ['value', 'trans', 'transBit', 'transXor', 'transXorBit']


def analyse(results, testNum, e0, e1):
    res0, resW, tpsTime = checkTpsVal(e0)
    res1, resW, tpsTime = checkTpsVal(e1)
    results['value'][testNum] = res0 and res1
    
    res, resW, tpsTime = checkTpsTrans(e0, e1)
    results['trans'][testNum] = res
        
    res, tpsTime = checkTpsTransBit(e0, e1)
    results['transBit'][testNum] = res
 
    res, resW, tpsTime = checkTpsTransXor(e0, e1)
    results['transXor'][testNum] = res

    res, tpsTime = checkTpsTransXorBit(e0, e1)
    results['transXorBit'][testNum] = res


def printResults(results):
    maxLen = 0
    for leakageModel in leakageModels:
        if len(leakageModel) > maxLen:
            maxLen = len(leakageModel)
    for leakageModel in leakageModels:
        print('%s' % leakageModel + ' ' * (maxLen - len(leakageModel)) + ' ', end = '')
        for testNum in range(1, numTests + 1):
            if results[leakageModel][testNum]:
                print('1', end = '')
            else:
                print('0', end = '')
            print(' ', end = '')
        print('')

    
   
def initializeRefResults(refResults, refText):
    global numTests

    idx = 0
    testNum = 1
    for leakageModel in leakageModels:

        while True:
            while refText[idx] == ' ':
                idx += 1
 
            c = refText[idx]
            idx += 1
            if c == '\n':
                assert(testNum == numTests + 1)
                testNum = 1
                break
            elif c == '0':
                refResults[leakageModel][testNum] = False
            else:
                assert(c == '1')
                refResults[leakageModel][testNum] = True
            testNum += 1


m0 = Symb('m0', 'M', 1)
m1 = Symb('m1', 'M', 1)
m2 = Symb('m2', 'M', 1)
m3 = Symb('m3', 'M', 1)

k0 = Symb('k0', 'S', 1)
k1 = Symb('k1', 'S', 1)
k2 = Symb('k2', 'S', 1)
k3 = Symb('k3', 'S', 1)


results = {}
refResults = {}
for leakageModel in leakageModels:
    refResults[leakageModel] = {}
    results[leakageModel] = {}



# 0 means leakage, 1 means no leakage
refText = '''0 0 0 0 1 1 1 1 1
             0 0 0 0 0 0 0 1 1
             0 0 1 1 0 1 1 1 1
             0 1 0 1 0 0 1 1 1
             1 1 1 1 0 1 1 1 1
'''

initializeRefResults(refResults, refText)
 

# 1
e0 = Concat(k1, k0)
e1 = Concat(m0, m0)
analyse(results, 1, e0, e1)

# 2
e0 = Concat(k1, k0)
e1 = Concat(m1, m0)
analyse(results, 2, e0, e1)

# 3
e0 = Concat(k1 ^ m0, k0 ^ m0)
e1 = Concat(m1, m1)
analyse(results, 3, e0, e1)

# 4
e0 = Concat(k1 ^ m0, k0 ^ m0)
e1 = Concat(m1, m2)
analyse(results, 4, e0, e1)

# 5
e0 = Concat(k1 ^ m1, k0 ^ m0)
e1 = Concat(m1, m0)
analyse(results, 5, e0, e1)

# 6
e0 = Concat(k1 ^ m1, k0 ^ m0)
e1 = Concat(m0, m1)
analyse(results, 6, e0, e1)

# 7
e0 = Concat(k1 ^ m1, k0 ^ m0)
e1 = Concat(k3 ^ m0, k2 ^ m2)
analyse(results, 7, e0, e1)

# 8
e0 = Concat(k0 ^ m0, k0 ^ m0)
e1 = Concat(m1, m1)
analyse(results, 8, e0, e1)

# 9
e0 = Concat(k1 ^ m1, k0 ^ m0)
e1 = Concat(k3 ^ m3, k2 ^ m2)
analyse(results, 9, e0, e1)



for leakageModel in leakageModels:
    for testNum in range(1, numTests + 1):
        res0 = results[leakageModel][testNum]
        res1 = refResults[leakageModel][testNum]
        if res0 != res1:
            print('### Expected result and obtained result differ: leakage %s, test %d' % (leakageModel, testNum))

print('Result Array:')
printResults(results)

print('Reference Result Array:')
printResults(refResults)







