#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

# Concrete Evaluation

from __future__ import print_function

from utils import *
from node import *

def getExevRec(node, m):

    if isinstance(node, SymbNode):
        if node not in m.keys():
            if '#' not in node.symb:
                print('*** Error: Value for symbol %s not specified' % node.symb)
                sys.exit(1)
            else:
                import re
                n, b = re.split(r'#', node.symb)
                wordNode = Node.symb2node[n]
                bit = int(b)
                if wordNode not in m.keys():
                    print('*** Error: Value for symbol %s not specified' % wordNode.symb)
                    sys.exit(1)
                return Extract(bit, bit, m[wordNode])
        return m[node]

    if isinstance(node, ConstNode):
        return node

    newChildren = []
    op = node.op
    for child in node.children:
        newChildren.append(getExevRec(child, m))
 
    if op == 'E':
        return Extract(*newChildren)
    elif op == 'ZE':
        return ZeroExt(*newChildren)
    elif op == 'SE':
        return SignExt(*newChildren)
    elif op == 'C':
        return Concat(*newChildren[::-1])
    elif op == 'LS':
        return LShR(*newChildren)
    elif op == '>>':
        return newChildren[0] >> newChildren[1]
    elif op == '<<':
        return newChildren[0] << newChildren[1]
    elif op == '-':
        return -newChildren[0]

    if op == '&':
        res = ~0
    else:
        res = 0
    for child in newChildren:
        if op == '^':
            res = res ^ child.cst
        elif op == '&':
            res = res & child.cst
        elif op == '|':
            res = res | child.cst
        elif op == '~':
            res = (1 << node.width) - 1 - child.cst
        elif op == '+':
            res = (res + child.cst) % (1 << node.width)
        elif op == 'A':
            # FIXME
            res = child.cst
        else:
            assert(False)

    return Const(res, node.width)




def compareExpsWithExevRec(e0, e1, allVars, idx, m):
    if idx < len(allVars):
        var = allVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            res, v0, v1 = compareExpsWithExevRec(e0, e1, allVars, idx + 1, m)
            if res != None:
                return res, v0, v1
            m[var] = None
        return None, None, None
    else:
        v0 = getExevRec(e0, m)
        v1 = getExevRec(e1, m)
        if v0.cst == v1.cst and v0.width == v1.width:
            return None, None, None
        else:
            return dict(m), v0.cst, v1.cst


def getVarsList(*exps):
    allVars = set()
    for e in exps:
        allVars.update(e.maskingMaskOcc.keys() + e.otherMaskOcc.keys() + e.secretVarOcc.keys() + e.publicVarOcc.keys())
    allVarsNoBits = set()
    for n in allVars:
        if '#' in n.symb:
            import re
            varName, b = re.split(r'#', n.symb)
            allVarsNoBits.add(Node.symb2node[varName])
        else:
            allVarsNoBits.add(n)

    allVarsList = sorted(list(allVarsNoBits), key = lambda x: x.symb)
    return allVarsList
    

def getSecretVarsSet(*exps):
    allVars = set()
    for e in exps:
        allVars.update(e.secretVarOcc.keys())
    secretVarsSet  = set()
    for n in allVars:
        if '#' in n.symb:
            import re
            varName, b = re.split(r'#', n.symb)
            secretVarsSet.add(Node.symb2node[varName])
        else:
            secretVarsSet.add(n)

    return secretVarsSet
    


def compareExpsWithExev(e0, e1):

    allVarsList = getVarsList(e0, e1)
    return compareExpsWithExevRec(e0, e1, allVarsList, 0, {})



def compareExpsWithRandev(e0, e1, nbEval):
    # Random Evaluations
    import random

    allVarsList = getVarsList(e0, e1)
    for i in range(nbEval):
        m = {}
        for v in allVarsList:
            m[v] = Const(random.randrange(0, (1 << v.width)), v.width)

        v0 = getExevRec(e0, m)
        v1 = getExevRec(e1, m)
        if v0.cst != v1.cst or v0.width != v1.width:
            return m, v0, v1
    return None, None, None






def getDistribRefBis(e0, distribRef, nonSecretVars, idx, m):
    if idx < len(nonSecretVars):
        var = nonSecretVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            getDistribRefBis(e0, distribRef, nonSecretVars, idx + 1, m)
    else:
        v = getExevRec(e0, m).cst
        distribRef[v] += 1


def getDistribRef(e0, secretVars, nonSecretVars):
    m = {}
    for k in secretVars:
        m[k] = Const(0, k.width)

    distribRef = {}
    for v in range(1 << e0.width):
        distribRef[v] = 0
    getDistribRefBis(e0, distribRef, nonSecretVars, 0, m)
    return distribRef


def getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, idx, m):
    if idx < len(nonSecretVars):
        var = nonSecretVars[idx]
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, idx + 1, m)
    else:
        v = getExevRec(e0, m).cst
        distrib[v] += 1


def getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, idx, m):
    if idx < len(secretVars):
        var = secretVars[idx]
        allRud = True
        for val in range(1 << var.width):
            m[var] = Const(val, var.width)
            rud, sid = getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, idx + 1, m)
            if not sid:
                return False, False
            allRud = allRud and rud
        return allRud, True
    else:
        distrib = {}
        for v in range(1 << e0.width):
            distrib[v] = 0
        getDistribWithExevRecBis(e0, distrib, distribRef, nonSecretVars, 0, m)
        rud = True
        for v in range(1 << e0.width):
            if distrib[v] != distribRef[0]:
                rud = False
            if distrib[v] != distribRef[v]:
                return False, False
        return rud, True



def getDistribWithExev(e0):
    allVarsList = getVarsList(e0)

    secretVars = filter(lambda x: x.symbType == 'S', allVarsList)
    nonSecretVars = filter(lambda x: x.symbType != 'S', allVarsList)

    distribRef = getDistribRef(e0, secretVars, nonSecretVars)
    rud, sid = getDistribWithExevRec(e0, distribRef, secretVars, nonSecretVars, 0, {})

    return rud, sid




