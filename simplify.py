#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier


from __future__ import print_function

from utils import *
from node import *


# Trying to merge current node with its children if associative and children have the same op
def mergeWithChildrenIfPossible(op, children):
    assert(len(children) != 0)
    if op in Node.associativeOps:
        merge = False
        for child in children:
            if child.op == op:
                merge = True
                break
        if merge:
            newChildren = []
            for child in children:
                if child.op == op:
                    newChildren.extend(child.children)
                else:
                    newChildren.append(child)
            return newChildren, True
        else:
            return children, False
    else:
        return children, False


def ConstNodeAuto(v):
    return Const(v, v.bit_length())


def ConstNodeFromExtract(msb, lsb, n):
    # Extract bitfield from constant
    # FIXME: A lot of things for a shift and a mask...
    assert(isinstance(n, ConstNode))
    cst = n.cst
    width = n.width
    cstString = format(cst, '0%db' % width)[::-1]
    newCstString = cstString[lsb:msb + 1]
    newCst = int(newCstString[::-1], 2)
    return Const(newCst, msb - lsb + 1)
 

def defaultNode(node, op, newChildren, modified):
    if modified:
        # We do not use OpNode constructor for operations using cache
        if op == 'E':
            return Extract(newChildren[0], newChildren[1], newChildren[2])
        else:
            return OpNode(op, newChildren)
    else:
        return node



def getBitDecompositionVar(node, msb = None, lsb = None):
    if lsb == None:
        lsb = 0
    if msb == None:
        msb = node.width - 1

    if node.width == 1:
        assert(msb == 0 and lsb == 0)
        return node
    if msb == lsb:
        s = node.symb + '#%d' % lsb
        return SymbInternal(s, node.symbType, 1)
    # If several bits, concat the single bits
    newChildren0 = []
    for i in range(msb, lsb - 1, -1):
        symb = getBitDecompositionVar(node, i, i)
        newChildren0.append(symb)
    return Concat(*newChildren0)



def getBitDecomposition(node):
    if isinstance(node, ConstNode):
        return node

    if node.concatExtEq != None:
        return node.concatExtEq

    if isinstance(node, SymbNode):
        be = getBitDecompositionVar(node)
        node.concatExtEq = be
        return be

    if node.op == 'A':
        # For arrays, the root node of the decomposition is not a Concat but an array node,
        # whose child is a concat (or Array, or mult)
        be = getBitDecomposition(node.children[1])
        arr = ArrayExp.allArrays[node.children[0].strn]
        newA = arr[be]
        node.concatExtEq = newA
        return newA

    if node.op == '*' or node.op == '**':
        # For multiplications, the root node of the decomposition is not a Concat but a '*' or '**' node
        # whose children are concat nodes (or Array)
        newChildren = []
        for child in node.children:
            newChild = getBitDecomposition(child)
            newChildren.append(newChild)
        newNode = OpNode(node.op, newChildren)
        node.concatExtEq = newNode
        return newNode
 
    l = []
    for b in range(node.width - 1, -1, -1):
        l.append(simplifyCore(Extract(b, b, node), True, True))
    be = Concat(*l)
    node.concatExtEq = be
    return be



def factorize(mulOp, newChildren, width):
    hasChanged = True
    while hasChanged:
        hasChanged = False
        i = 0
        while i < len(newChildren):
            if newChildren[i].op == mulOp:
                firstMul = newChildren[i]
                j = 0
                while j < len(newChildren):
                    if i == j:
                        j += 1
                        continue
                    if newChildren[j].op == mulOp:
                        # case  a *  b  ^  a *  c  -> a *  (b ^ c)
                        # case  a ** b  +  a ** c  -> a ** (b + c)
                        # case  a &  b  |  a &  c  -> a &  (b | c)
                        # case (a |  b) & (a |  c) -> a |  (b & c)
                        secndMul = newChildren[j]
                        k = 0
                        while k < len(firstMul.children):
                            l = 0
                            while l < len(secndMul.children):
                                if equivalence(firstMul.children[k], secndMul.children[l]):
                                    hasChanged = True
                                    factor = firstMul.children[k]
                                    # Determining the add/or operands
                                    xorLeftChildren = list(firstMul.children)
                                    xorLeftChildren.pop(k)
                                    if len(xorLeftChildren) == 1:
                                        xorLeftNode = xorLeftChildren[0]
                                    else:
                                        xorLeftNode = OpNode(mulOp, xorLeftChildren)
                                    xorRighChildren = list(secndMul.children)
                                    xorRighChildren.pop(l)
                                    if len(xorRighChildren) == 1:
                                        xorRighNode = xorRighChildren[0]
                                    else:
                                        xorRighNode = OpNode(mulOp, xorRighChildren)

                                    if mulOp == '*':
                                        xorNode = simplify(xorLeftNode ^ xorRighNode)
                                    elif mulOp == '**':
                                        xorNode = simplify(xorLeftNode + xorRighNode)
                                    elif mulOp == '&':
                                        xorNode = simplify(xorLeftNode | xorRighNode)
                                    elif mulOp == '|':
                                        xorNode = simplify(xorLeftNode & xorRighNode)
                                    newGrandChildren = [factor, xorNode]
                                    break
                                l += 1
                            if hasChanged:
                                break
                            k += 1
                    else:
                        # case  a *  b  ^ a -> a *  (b ^ 1) / a * b * c ^ a -> a * (b * c ^ 1)
                        # case  a ** b  + a -> a ** (b + 1)
                        # case  a &  b  | a -> a            / a & b & c | a -> a
                        # case (a |  b) & a -> a
                        k = 0
                        while k < len(firstMul.children):
                            if equivalence(firstMul.children[k], newChildren[j]):
                                hasChanged = True
                                newGrandChildren = None
                                if mulOp == '*' or mulOp == '**':
                                    factor = newChildren[j]
                                    # Determining the xor operands
                                    xorLeftChildren = list(firstMul.children)
                                    xorLeftChildren.pop(k)
                                    if len(xorLeftChildren) == 1:
                                        xorLeftNode = xorLeftChildren[0]
                                    else:
                                        xorLeftNode = OpNode(mulOp, xorLeftChildren)
    
                                    if mulOp == '*':
                                        xorNode = simplify(xorLeftNode ^ Const(0x1, width))
                                    elif mulOp == '**':
                                        xorNode = simplify(xorLeftNode + Const(0x1, width))
                                    newGrandChildren = [factor, xorNode]
                                else:
                                    newChildren.pop(i)
                                break
                            k += 1
                    if hasChanged and newGrandChildren != None:
                        newChildren.pop(max(i, j))
                        newChildren.pop(min(i, j))
                        mulNode = simplify(OpNode(mulOp, newGrandChildren))
                        newChildren.append(mulNode)
                        break
                    j += 1
            if hasChanged:
                break
            i += 1




def simplify(node):
    return simplifyCore(node, True, False)


def simplifyAndNotPEI(node):
    return simplifyCore(node, False, False)


def simplifyCore(node, propagateExtractInwards, useSingleBitVariables):
    # Verify that using single-bit variables implies propagating Extract inwards
    assert(not useSingleBitVariables or propagateExtractInwards)

    def setSimpEqAndReturn(node, simpEq):
        #from concrev import compareExpsWithRandev
        #r, u, v = compareExpsWithRandev(node, simpEq, 100)
        #if r != None:
        #    print('*** Error: exp and simplified exp are different')
        #    print('exp           : %s' % node)
        #    print('simplified exp: %s' % simpEq)
        #    import sys
        #    sys.exit(1)

        if useSingleBitVariables:
            node.simpEqUsbv = simpEq
            simpEq.simpEq = simpEq
            simpEq.simpEqUsbv = simpEq
        else:
            node.simpEq = simpEq
            simpEq.simpEq = simpEq
        #print('# Simplify of :')
        #print('%s' % node)
        #print('# Returns:')
        #print('%s' % simpEq)
        #assert(node.width == simpEq.width)
        return simpEq


    if isinstance(node, ConstNode):
        return node

    if useSingleBitVariables:
        if node.simpEqUsbv != None:
            return node.simpEqUsbv
    else:
        if node.simpEq != None:
            return node.simpEq


    if isinstance(node, SymbNode):
        if useSingleBitVariables:
            s = getBitDecompositionVar(node)
            return setSimpEqAndReturn(node, s)
        else:
            return setSimpEqAndReturn(node, node)

    #print('# Simplifying node %s' % node)

    # After the "pre" recursive call part, the node to simplify is
    # defined with variable 'op' and list of children 'newChildren'
    newChildren0 = None
    op = node.op
    width = node.width

    if op == 'E':
        child = node.children[2]
        msbNode = node.children[0]
        lsbNode = node.children[1]
        #print('# Child of Extract to propagate inwards: %s' % child)

        # At this end of this while loop, the current node (defined by op and newChildren0)
        # must not be an Extract node if propagateExtractInwards is True
        while True:
            assert(op == 'E')
            #   child is the expression from which the extract occurs.
            #   For 2nd iteration onwards, it must be newChildren0[2]
            #   msbNode and lsbNode must also have the correct value
            # We do not look at child, msbNode and lsbNode in newChildren0
            # since it is not defined in 1st iteration and is used to detect a change later
            msb = msbNode.cst
            lsb = lsbNode.cst

            if op == 'E' and lsb == 0 and msb == child.width - 1:
                if isinstance(child, ConstNode):
                    return setSimpEqAndReturn(node, child)
                if isinstance(child, SymbNode):
                    if useSingleBitVariables:
                        s = getBitDecompositionVar(child)
                        return setSimpEqAndReturn(node, s)
                    else:
                        return setSimpEqAndReturn(node, child)
                op = child.op
                newChildren0 = child.children
                if op == 'E':
                    child = newChildren0[2]
                    msbNode = newChildren0[0]
                    lsbNode = newChildren0[1]
                    msb = msbNode.cst
                    lsb = lsbNode.cst
                    continue
                else:
                    break

            if isinstance(child, SymbNode):
                if useSingleBitVariables:
                    s = getBitDecompositionVar(child, msb, lsb)
                    return setSimpEqAndReturn(node, s)
                else:
                    if newChildren0 == None:
                        return setSimpEqAndReturn(node, node)
                    else:
                        return setSimpEqAndReturn(node, Extract(newChildren0[0], newChildren0[1], newChildren0[2]))
 
            elif isinstance(child, ConstNode):
                return setSimpEqAndReturn(node, ConstNodeFromExtract(msb, lsb, child))
           
            assert(isinstance(child, OpNode))
            if child.op == 'E':
                # Extract(m, l, Extract(v, u, e)) -> Extract(m + u, l + u, e)
                # Case is possible even if SimplifyExtract has been called (three or more nested Extract)
                gLsbNode = child.children[1]
                gLsb = gLsbNode.cst
                msbNode = ConstNodeAuto(msb + gLsb)
                lsbNode = ConstNodeAuto(lsb + gLsb)
                child = child.children[2]
                newChildren0 = [msbNode, lsbNode, child]
                op = 'E'
                #print('# Node after PE : %s' % OpNode(op, newChildren0))
                continue

            elif child.op == 'C':
                concatNode = child
                startBitIdx = lsb
                nbBitsOnRight = 0
                i = 0
                while concatNode.children[i].width <= startBitIdx:
                    concatChildWidth = concatNode.children[i].width
                    startBitIdx -= concatChildWidth
                    nbBitsOnRight += concatChildWidth
                    i += 1
            
                startChildIdx = i
            
                while nbBitsOnRight + concatNode.children[i].width <= msb:
                    nbBitsOnRight += concatNode.children[i].width
                    i += 1
                endChildIdx = i
                endBitIdx = msb - nbBitsOnRight
                assert(endChildIdx < len(concatNode.children))
        
                if startChildIdx == endChildIdx:
                    # Extract contained in a single element (resNode), we remove Concat in all cases
                    resNode = concatNode.children[startChildIdx]
                    if startBitIdx == 0 and endBitIdx == resNode.width - 1:
                        # Also Remove Extract
                        if isinstance(resNode, ConstNode):
                            return setSimpEqAndReturn(node, resNode)
                        if isinstance(resNode, SymbNode):
                            if useSingleBitVariables:
                                s = getBitDecompositionVar(resNode)
                                return setSimpEqAndReturn(node, s)
                            else:
                                return setSimpEqAndReturn(node, resNode)
                        newChildren0 = list(resNode.children)
                        op = resNode.op
                        if op == 'E':
                            msbNode = newChildren0[0]
                            lsbNode = newChildren0[1]
                            child = newChildren0[2]
                            continue
                        else:
                            break
                    else:
                        # Remove concat only, create new Extract with updated bounds and loop
                        msbNode = ConstNodeAuto(endBitIdx)
                        lsbNode = ConstNodeAuto(startBitIdx)
                        child = resNode
                        newChildren0 = [msbNode, lsbNode, resNode]
                        op = 'E'
                        continue

                # Extract covers 2 children or more
                lsConcatChild = concatNode.children[startChildIdx] # Least Significant child, on the right, at index 0 in list of concat children
                if startBitIdx == 0:
                    lsNode = lsConcatChild
                else:
                    lsNode = Extract(lsConcatChild.width - 1, startBitIdx, lsConcatChild)
                msConcatChild = concatNode.children[endChildIdx]
                if endBitIdx == msConcatChild.width - 1:
                    msNode = msConcatChild
                else:
                    msNode = Extract(endBitIdx, 0, msConcatChild)
                newChildren0 = concatNode.children[startChildIdx + 1:endChildIdx]
                newChildren0.insert(0, lsNode)
                newChildren0.append(msNode)
                op = 'C'
                break

            elif child.op == 'ZE' or child.op == 'SE':
                ## FIXME: replace these operations with concat at creation?
                extendNode = child
                extendValue = extendNode.children[0].cst
                exp = extendNode.children[1]
                if msb <= exp.width - 1:
                    # Remove SE or ZE
                    if lsb == 0 and msb == exp.width - 1:
                        # +---------+-------------+
                        # | Extend  |     exp     |
                        # +---------+-------------+
                        #           \-- Extract --/
                        if isinstance(exp, ConstNode):
                            return setSimpEqAndReturn(node, exp)
                        if isinstance(exp, SymbNode):
                            if useSingleBitVariables:
                                s = getBitDecompositionVar(exp)
                                return setSimpEqAndReturn(node, s)
                            else:
                                return setSimpEqAndReturn(node, exp)
                        newChildren0 = exp.children
                        op = exp.op
                        if op == 'E':
                            msbNode = newChildren0[0]
                            lsbNode = newChildren0[1]
                            child = newChildren0[2]
                            continue
                        else:
                            break
                    else:
                        # +------+----------------+
                        # | Ext  |      exp       |
                        # +------+----------------+
                        #           \- Extract -/
                        # msbNode and lsbNode unchanged
                        child = exp
                        newChildren0 = [msbNode, lsbNode, exp]
                        op = 'E'
                        continue
                elif lsb == 0:
                    # We also have msb > exp.width - 1
                    # We can remove the Extract if we modify the Extension length
                    # +---------------+-------+
                    # | Extend        |  exp  |
                    # +---------------+-------+
                    #           \-- Extract --/
                    extendWidth = node.width - exp.width
                    if extendNode.op == 'ZE':
                        newChildren0 = [exp, Const(0, extendWidth)]
                        op = 'C'
                        break
                    else:
                        # SE
                        expMsb = Extract(exp.width - 1, exp.width - 1, exp)
                        newChildren0 = [expMsb] * extendWidth
                        newChildren0.insert(0, exp)
                        op = 'C'
                        break
                elif lsb > exp.width - 1 and extendNode.op == 'ZE':
                    # +-----------------+-------+
                    # | ZExt            |  exp  |
                    # +-----------------+-------+
                    #   \-- Extract --/
                    return setSimpEqAndReturn(node, Const(0, msb - lsb + 1))
                elif lsb >= exp.width - 1 and extendNode.op == 'SE':
                    # Propagate Extract inwards
                    concatSize = msb - lsb + 1
                    # +-----------------+-------+
                    # | SExt            |  exp  |
                    # +-----------------+-------+
                    #   \-- Extract --/
                    if concatSize == 1:
                        msbNode = ConstNodeAuto(exp.width - 1)
                        lsbNode = msbNode
                        child = exp
                        newChildren0 = [msbNode, lsbNode, child]
                        op = 'E'
                        continue
                    else:
                        expMsb = Extract(exp.width - 1, exp.width - 1, exp)
                        newChildren0 = [expMsb] * concatSize
                        op = 'C'
                        break
                else:
                    # propagate Extract inwards
                    # +-----------------+-------+
                    # | SExt            |  exp  |
                    # +-----------------+-------+
                    #       \--- Extract ---/
                    newExtSize = node.width - (exp.width - lsb)
                    newExtractNode = Extract(exp.width - 1, lsb, exp) 
                    if extendNode.op == 'ZE':
                        newChildren0 = [newExtractNode, Const(0, newExtSize)]
                    else:
                        expMsb = Extract(exp.width - 1, exp.width - 1, exp)
                        newChildren0 = [expMsb] * newExtSize
                        newChildren0.insert(0, newExtractNode)
                    op = 'C'
                    break

            elif child.op == '<<':
                gchild = child.children[0]
                shNode = child.children[1]
                sh = shNode.cst
                if msb < sh:
                    return setSimpEqAndReturn(node, Const(0, msb - lsb + 1))
                else:
                    if lsb >= sh:
                        # Extract(m, l, e << sh) -> Extract(m - sh, l - sh, e)
                        child = gchild
                        msbNode = ConstNodeAuto(msb - sh)
                        lsbNode = ConstNodeAuto(lsb - sh)
                        newChildren0 = [msbNode, lsbNode, child]
                        op = 'E'
                        continue
                    else:
                        # We have lsb - sh < 0
                        # Extract(m, l, e << sh) -> Concat(Extract(m - sh, 0, e), 0 [sh - l])
                        newExtractNode = Extract(msb - sh, 0, gchild)
                        zeroNode = Const(0, sh - lsb)
                        newChildren0 = [zeroNode, newExtractNode]
                        op = 'C'
                        break
    
            elif child.op == 'LS':
                gchild = child.children[0]
                shNode = child.children[1]
                sh = shNode.cst
                if lsb >= gchild.width - sh:
                    return setSimpEqAndReturn(node, Const(0, msb - lsb + 1))
                else:
                    if msb < gchild.width - sh:
                        # Extract(m, l, LShR(e, sh)) -> Extract(m + sh, l + sh, e)
                        child = gchild
                        msbNode = ConstNodeAuto(msb + sh)
                        lsbNode = ConstNodeAuto(lsb + sh)
                        newChildren0 = [msbNode, lsbNode, child]
                        op = 'E'
                        continue
                    else:
                        # Extract(m, l, LShR(e, sh)) -> Concat(0  [m - (e.w - sh) + 1], Extract(e.w - 1, lsb + sh, e))
                        msbNode = ConstNodeAuto(gchild.width - 1)
                        lsbNode = ConstNodeAuto(lsb + sh)
                        newExtractNode = Extract(msbNode, lsbNode, gchild)
                        zeroNode = Const(0, msb - (gchild.width - sh) + 1)
                        newChildren0 = [newExtractNode, zeroNode]
                        op = 'C'
                        break
    
            elif child.op == '>>':
                gchild = child.children[0]
                shNode = child.children[1]
                sh = shNode.cst
                gchildMsb = Extract(gchild.width - 1, gchild.width - 1, gchild)
                if lsb >= gchild.width - sh - 1:
                    if msb == lsb:
                        # We avoid the Concat of a single node (gchildMsb)
                        # gchildMsb is reanalyzed
                        child = gchild
                        msbNode = ConstNodeAuto(gchild.width - 1)
                        lsbNode = msbNode
                        newChildren0 = [msbNode, lsbNode, child]
                        op = 'E'
                        continue
                    else:
                        newChildren0 = [gchildMsb] * (msb - lsb + 1)
                        op = 'C'
                        break
                else:
                    if msb < gchild.width - sh:
                        # Extract(m, l, e >> sh) -> Extract(m + sh, l + sh, e)
                        child = gchild
                        msbNode = ConstNodeAuto(msb + sh)
                        lsbNode = ConstNodeAuto(lsb + sh)
                        newChildren0 = [msbNode, lsbNode, gchild]
                        op = 'E'
                        continue
                    else:
                        # Extract(m, l, e >> sh) -> Concat(e[w - 1] [m - (e.w - sh) + 1], Extract(e.w - 1, lsb + sh, e))
                        msbNode = ConstNodeAuto(gchild.width - 1)
                        lsbNode = ConstNodeAuto(lsb + sh)
                        newExtractNode = Extract(msbNode, lsbNode, gchild)
                        newChildren0 = [gchildMsb] * (msb - (gchild.width - sh) + 1)
                        newChildren0.insert(0, newExtractNode)
                        op = 'C'
                        break
 
            elif propagateExtractInwards and child.op in Node.bitwiseOps:
                # Extract(m, l, e & f) -> Extract(m, l, e) & Extract(m, l, f)
                newChildren0 = []
                for gchild in child.children:
                    newExtractNode = Extract(msb, lsb, gchild)
                    newChildren0.append(newExtractNode)
                op = child.op
                break

            elif propagateExtractInwards and child.op == '~':
                gchild = child.children[0]
                newExtractNode = Extract(msbNode, lsbNode, gchild)
                newChildren0 = [newExtractNode]
                op = '~'
                break

            elif propagateExtractInwards and child.op == '+':
                if msb == lsb:
                    idx = 0
                    child0 = child.children[0]
                    child0Bits = []
                    for b in range(msb + 1):
                        child0Bits.append(Extract(b, b, child0))
                    while idx < len(child.children) - 1:
                        res = []
                        ci = Const(0, 1)
                        child1 = child.children[idx + 1]
                        for b in range(msb + 1):
                            ai = child0Bits[b]
                            bi = Extract(b, b, child1)
                            aiXorbi = ai ^ bi
                            if b != msb or idx != len(child.children) - 2:
                                si = aiXorbi ^ ci
                                res.append(si)
                            if b != msb:
                                ci = (aiXorbi & ci) | (ai & bi)
                        child0Bits = res
                        idx += 1
                    newChildren0 = [aiXorbi, ci]
                    op = '^'
                    break
                else:
                    idx = 0
                    child0 = child.children[0]
                    child0Bits = []
                    for b in range(msb + 1):
                        child0Bits.append(Extract(b, b, child0))
                    while idx < len(child.children) - 1:
                        res = []
                        ci = Const(0, 1)
                        child1 = child.children[idx + 1]
                        for b in range(msb + 1):
                            ai = child0Bits[b]
                            bi = Extract(b, b, child1)
                            aiXorbi = ai ^ bi
                            si = aiXorbi ^ ci
                            res.append(si)
                            if b != msb:
                                ci = (aiXorbi & ci) | (ai & bi)
                        child0Bits = res
                        idx += 1
                    newChildren0 = res[lsb:msb + 1]
                    op = 'C'
                    break

            elif propagateExtractInwards and child.op == '-':
                if msb == lsb:
                    ci = Const(1, 1)
                    child0 = child.children[0]
                    for b in range(msb + 1):
                        ai = ~Extract(b, b, child0)
                        if b != msb:
                            si = ai ^ ci
                            ci = ai & ci
                    newChildren0 = [ai, ci]
                    op = '^'
                    break
                else:
                    res = []
                    ci = Const(1, 1)
                    child0 = child.children[0]
                    for b in range(msb + 1):
                        ai = ~Extract(b, b, child0)
                        si = ai ^ ci
                        res.append(si)
                        if b != msb:
                            ci = ai & ci
                    newChildren0 = res[lsb:msb + 1]
                    op = 'C'
                    break

            elif propagateExtractInwards and child.op == 'A' or child.op == '*' or child.op == '**':
                # Particular case: we cannot propagate extract inwards but we need to remove the occurrences of multiple-bit variables
                # (otherwise the TPS algorithm can conclude no leakage and be wrong)
                if useSingleBitVariables:
                    decompNode = getBitDecomposition(child)
                    simplifiedNode = Extract(msbNode, lsbNode, decompNode)
                    return setSimpEqAndReturn(node, simplifiedNode)
                else:
                    return setSimpEqAndReturn(node, defaultNode(node, op, newChildren0, newChildren0 != None))

            else:
                assert(not propagateExtractInwards)
                break



    modified = (newChildren0 != None)
    if not modified:
        # A priori not necessary to copy the list since it is not modified
        # But still maybe safer to copy it?
        #print_level(2, '# Node not modified by prologue')
        newChildren0 = node.children

    newChildren = []
    for child in newChildren0:
        newChildren.append(simplifyCore(child, propagateExtractInwards, useSingleBitVariables))
    #print('All children simplified:')
    #for child in newChildren:
    #    print('   %s' % child)
    
    if not modified:
        for i in range(len(newChildren0)):
            if newChildren[i] is not newChildren0[i]:
                modified = True
                break

    # FIXME: Concat(a, b) ^ Concat(c, d) -> Concat(a ^ c, b ^ d) ?
    # Not done? Useful?
    # Yes: to replace at contruction SE and ZE by Concat(Const(0, w), ...)

    # ZeroExt(n, k) ^ ZeroExt(n, m) -> ZeroExt(n, k ^ m)
    if op == '^' or op == '&' or op == '|':
        allChildrenZeroExt = True
        allChildrenSignExt = True
        for child in newChildren:
            if not isinstance(child, OpNode):
                allChildrenZeroExt = False
                allChildrenSignExt = False
                break
            if child.op != 'ZE' or child.children[0].cst != newChildren[0].children[0].cst:
                allChildrenZeroExt = False
                if not allChildrenSignExt:
                    break
            if child.op != 'SE' or child.children[0].cst != newChildren[0].children[0].cst:
                allChildrenSignExt = False
                if not allChildrenZeroExt:
                    break
        if allChildrenZeroExt or allChildrenSignExt:
            extType = newChildren[0].op
            extWidthNode = newChildren[0].children[0]

            childrenList = []
            for child in newChildren:
                childrenList.append(child.children[1])
            opNode = simplify(OpNode(op, childrenList))

            # Not returning now: in order to allow simplifications of new ZE or SE node
            op = extType
            newChildren = [extWidthNode, opNode]
            modified = True


    if op == '^':
        # simplify e ^ 0 to e
        # simplify e ^ e to 0
        # simplify e ^ 1 to ~e
        # simplify ~a ^ ~b ^ ~c to ~(a ^ b ^ c)
        addNotNode = False
        # Necessary to cut into two while loops: the exp k0 ^ ~k0 will not be simplified in one pass
        # (the ~ would be removed when processing the second child and then the comparison with the first child would not be done)
        i = 0
        while i < len(newChildren):
            child0 = newChildren[i]
            if child0.op == '~':
                addNotNode = not addNotNode
                modified = True
                # Removing not node in child
                newChildren[i] = newChildren[i].children[0]
            i += 1

        # Calling mergeWithChildrenIfPossible
        # Done here because removing '~' node can make new '^' nodes as children
        # (Note those '^' nodes should not have any '~' children)
        if len(newChildren) > 0:
            tempNode = OpNode('^', newChildren)
            newChildren, m = mergeWithChildrenIfPossible('^', newChildren)
            modified = modified or m
            #print_level(4, 'modified: %s' % modified)

        i = 0
        while i < len(newChildren):
            child0 = newChildren[i]
            j = i + 1
            removed = False
            while j < len(newChildren):
                child1 = newChildren[j]
                if equivalence(child0, child1):
                    # Suppressing child0 and child1 from list starting
                    # with child1 in order not to modify child0 index
                    newChildren.pop(j)
                    newChildren.pop(i)
                    removed = True
                    modified = True
                    break
                j += 1
            if not removed:
                i += 1

        # Constant propagation
        # FIXME: modified is set to True in case there is only one constant and the expression does not change
        i = 0
        constVal = 0
        while i < len(newChildren):
            child = newChildren[i]
            if isinstance(child, ConstNode):
                constVal = constVal ^ child.cst
                newChildren.pop(i)
                modified = True
                continue
            i += 1
        if constVal != 0:
            if constVal == (1 << width) - 1:
                addNotNode = not addNotNode
            else:
                if addNotNode:
                    newChildren.append(Const(constVal ^ ((1 << width) - 1), width))
                    addNotNode = False
                else:
                    newChildren.append(Const(constVal, width))


        # a * b ^ a * c -> a * (b ^ c)
        # Remark: the factorisation is not unique (is it a problem?)
        #   a * b ^ a * c ^ b * c
        # = a * (b ^ c) ^ b * c
        # = b * (a ^ c) ^ a * c
        # = c * (a ^ b) ^ a * b
        if node.hasWordOp:
            factorize('*', newChildren, width)

        # Final considerations
        if len(newChildren) == 0:
            if addNotNode:
                return setSimpEqAndReturn(node, Const((1 << width) - 1, width))
            else:
                return setSimpEqAndReturn(node, Const(0, width))
        elif len(newChildren) == 1:
            if addNotNode:
                return setSimpEqAndReturn(node, OpNode('~', newChildren))
            else:
                return setSimpEqAndReturn(node, newChildren[0])
        else:
            if modified:
                xorNode = OpNode('^', newChildren)
                if addNotNode:
                    return setSimpEqAndReturn(node, OpNode('~', [xorNode]))
                else:
                    return setSimpEqAndReturn(node, xorNode)
            else:
                return setSimpEqAndReturn(node, node)


    elif op == '+':
        newChildren, m = mergeWithChildrenIfPossible('+', newChildren)
        modified = modified or m

        # Constant propagation
        i = 0
        constVal = 0
        while i < len(newChildren):
            child = newChildren[i]
            if isinstance(child, ConstNode):
                constVal = (constVal + child.cst) % (1 << width)
                newChildren.pop(i)
                modified = True
                continue
            i += 1
        if constVal != 0:
            newChildren.append(Const(constVal, width))

        # 2nd pass: equivalence: removing opposite expressions
        i = 0
        while i < len(newChildren):
            child0 = newChildren[i]
            j = i + 1
            removed = False
            while j < len(newChildren):
                child1 = newChildren[j]
                if child0.op == '-' and equivalence(child0.children[0], child1) or child1.op == '-' and equivalence(child0, child1.children[0]):
                    # Suppressing child0 and child1 starting from child1
                    newChildren.pop(j)
                    newChildren.pop(i)
                    removed = True
                    modified = True
                    break
                j += 1
            if not removed:
                i += 1

        # Factorization
        if node.hasWordOp:
            factorize('**', newChildren, width)


        if len(newChildren) == 0:
            return setSimpEqAndReturn(node, Const(0, width))
        if len(newChildren) == 1:
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))
     

    elif op == '-':
        assert(len(newChildren) == 1)
        assert(not isinstance(newChildren[0], ConstNode))
        # -(-e) -> e
        child = newChildren[0]
        if child.op == '-':
            return setSimpEqAndReturn(node, child.children[0])
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))

    elif op == '&' or op == '|':
        if op == '&':
            #print('simp & [ ' + ', '.join(map(lambda x: '%s' % x, newChildren)) + ' ]')
            op1 = '|'
            cst0 = Const(0, width)
            cst1 = Const(((1 << width) - 1), width)
        else:
            #print('simp | [ ' + ', '.join(map(lambda x: '%s' % x, newChildren)) + ' ]')
            op1 = '&'
            cst0 = Const(((1 << width) - 1), width)
            cst1 = Const(0, width)

        newChildren, m = mergeWithChildrenIfPossible(op, newChildren)
        modified = modified or m
        
        # simplify a | (~a & b) to a | b
        #          a & (~a | b) to a & b
        # an iteration loop is necessary, until no change is made...
        # e.g.                (~a & ~b & c) | (~a & b) | a
        # after 1 iteration:  (~b & c) | b | a
        # after 2 iterations: c | b | a
        hasChanged = True
        while hasChanged:
            hasChanged = False
            i = 0
            while i < len(newChildren):
                child0 = newChildren[i]
                if child0.op == op1:
                    j = 0
                    idxToRemove = set()
                    while j < len(child0.children):
                        k = 0
                        while k < len(newChildren):
                            if i == k:
                                k += 1
                                continue
                            child1 = newChildren[k]
                            if child1.op == '~' and equivalence(child1.children[0], child0.children[j]) or child0.children[j].op == '~' and equivalence(child1, child0.children[j].children[0]):
                                idxToRemove.add(j)
                                break
                            k += 1
                        j += 1
                    if len(idxToRemove) != 0:
                        newGrandChildren = list()
                        for idx in range(len(child0.children)):
                            if idx not in idxToRemove:
                                newGrandChildren.append(child0.children[idx])
                        if len(newGrandChildren) == 0:
                            newChild = cst1
                        elif len(newGrandChildren) == 1:
                            newChild = newGrandChildren[0]
                        else:
                            newChild = OpNode(op1, newGrandChildren)
                        newChildren[i] = newChild
                        newChildren, m = mergeWithChildrenIfPossible(op, newChildren)
                        hasChanged = True
                        modified = True
                i += 1

        # simplify e & e and e | e to e
        i = 0
        while i < len(newChildren):
            child0 = newChildren[i]
            j = i + 1
            while j < len(newChildren):
                child1 = newChildren[j]
                if equivalence(child0, child1):
                    # Suppressing child1
                    newChildren.pop(j)
                    modified = True
                else:
                    j += 1
            i += 1

        # simplify e & ~e to 0 and e | ~e to 1
        i = 0
        while i < len(newChildren):
            child0 = newChildren[i]
            j = i + 1
            while j < len(newChildren):
                child1 = newChildren[j]
                if child0.op == '~' and equivalence(child0.children[0], child1) or child1.op == '~' and equivalence(child0, child1.children[0]):
                    return setSimpEqAndReturn(node, cst0)
                else:
                    j += 1
            i += 1

        # simplify e | 0 to e, e | 1 to 1
        # simplify e & 0 to 0, e & 1 to e
        i = 0
        constVal = cst1.cst
        while i < len(newChildren):
            child = newChildren[i]
            if isinstance(child, ConstNode):
                if op == '&':
                    constVal = constVal & child.cst
                else:
                    constVal = constVal | child.cst
                newChildren.pop(i)
                modified = True
                continue
            i += 1

        # Factorization
        factorize(op1, newChildren, width)

        if constVal == cst0.cst:
            return setSimpEqAndReturn(node, cst0)
        if constVal != cst1.cst:
            # modified already set to True in while loop
            newChildren.append(Const(constVal, width))

        # Final considerations
        if len(newChildren) == 0:
            return setSimpEqAndReturn(node, Const(0, width))
        if len(newChildren) == 1:
            # Suppressing '&' or '|' node
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == '~':
        assert(len(newChildren) == 1)
        child = newChildren[0]
        if child.op == '~':
            return setSimpEqAndReturn(node, child.children[0])
        elif isinstance(child, ConstNode) and child.cst == 0:
            return setSimpEqAndReturn(node, Const((1 << width) - 1, width))
        elif isinstance(child, ConstNode) and child.cst == (1 << width) - 1:
            return setSimpEqAndReturn(node, Const(0, width))
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == '<<':
        exp = newChildren[0]
        sh0 = newChildren[1]
        if sh0.cst == 0:
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            if exp.op == '<<':
                gChild = exp.children[0]
                sh1 = exp.children[1]
                return setSimpEqAndReturn(node, gChild << (sh0.cst + sh1.cst))
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == '>>':
        exp = newChildren[0]
        sh0 = newChildren[1]
        if sh0.cst == 0:
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            if exp.op == '>>':
                gChild = exp.children[0]
                sh1 = exp.children[1]
                return setSimpEqAndReturn(node, gChild >> (sh0.cst + sh1.cst))
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == 'LS':
        exp = newChildren[0]
        sh0 = newChildren[1]
        if sh0.cst == 0:
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            if exp.op == 'LS':
                gChild = exp.children[0]
                sh1 = exp.children[1]
                return setSimpEqAndReturn(node, LShR(gChild, sh0.cst + sh1.cst))
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == 'E':
        if modified:
            newNode = Extract(newChildren[0], newChildren[1], newChildren[2])
            return setSimpEqAndReturn(node, simplifyExtract(newNode))
        else:
            return setSimpEqAndReturn(node, simplifyExtract(node))


    elif op == 'C':
        # Case all children constants
        allChildrenCst = True
        for child in newChildren:
            if not isinstance(child, ConstNode):
                allChildrenCst = False
                break
        if allChildrenCst:
            cstRes = 0
            currNbBits = 0
            for child in newChildren:
                cstRes += child.cst << currNbBits
                currNbBits += child.width
            return setSimpEqAndReturn(node, Const(cstRes, currNbBits))

        # Concat(e, Concat(f, g))
        mergeConcat = False
        for child in newChildren:
            if child.op == 'C':
                modified = True
                mergeConcat = True
                break
        if mergeConcat:
            newChildrenMerged = []
            for child in newChildren:
                if child.op == 'C':
                    for gChild in child.children:
                        newChildrenMerged.append(gChild)
                else:
                    newChildrenMerged.append(child)
            newChildren = newChildrenMerged


        # Case all children are Extract nodes with corresponding bit indexes
        # Checking first child in advance in order to get its indexes
        if newChildren[0].op == 'E':
            firstBit = newChildren[0].children[1].cst
            currentBit = newChildren[0].children[0].cst + 1

            for childNum in range(1, len(newChildren)):
                child = newChildren[childNum]
                if child.op == 'E' and child.children[1].cst == currentBit:
                    currentBit = child.children[0].cst + 1
                else:
                    return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))
            # Checking if all children are equivalent expressions
            for childNum in range(1, len(newChildren)):
                if not equivalence(newChildren[0].children[2], newChildren[childNum].children[2]):
                    return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))

            if firstBit == 0 and currentBit == newChildren[0].children[2].width:
                return setSimpEqAndReturn(node, newChildren[0].children[2])
            else:
                return setSimpEqAndReturn(node, Extract(currentBit - 1, firstBit, newChildren[0].children[2]))

        return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == 'ZE':
        if isinstance(newChildren[1], ConstNode):
            numZeros = newChildren[0]
            child = newChildren[1]
            cst = child.cst
            childNbBits = child.width
            if cst < 0:
                cst = cst % (1 << childNbBits)
            assert(width == childNbBits + numZeros.cst)
            return setSimpEqAndReturn(node, Const(cst, width))
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))


    elif op == '*' or op == '**':
        newChildren, m = mergeWithChildrenIfPossible(op, newChildren)
        modified = modified or m

        # Constant propagation
        i = 0
        constVal = 1
        while i < len(newChildren):
            child = newChildren[i]
            if isinstance(child, ConstNode):
                constVal = gmulInt(constVal, child.cst)
                newChildren.pop(i)
                modified = True
                continue
            i += 1
        if constVal == 0:
            return setSimpEqAndReturn(node, Const(0, width))
        if constVal != 1:
            newChildren.append(Const(constVal, width))

        if len(newChildren) == 0:
            return setSimpEqAndReturn(node, Const(0, width))
        if len(newChildren) == 1:
            return setSimpEqAndReturn(node, newChildren[0])
        else:
            return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))
     

    # Default case
    else:
        return setSimpEqAndReturn(node, defaultNode(node, op, newChildren, modified))




def simplifyExtract(node):
    # No recursion
    child = node.children[2]
    msbNode = node.children[0]
    msb = msbNode.cst
    lsbNode = node.children[1]
    lsb = lsbNode.cst
    if isinstance(child, ConstNode):
        return ConstNodeFromExtract(msb, lsb, child)
    elif child.op == 'SE' or child.op == 'ZE':
        extendNode = child
        extendValue = extendNode.children[0].cst
        gchild = extendNode.children[1]
        if msb <= gchild.width - 1:
            # Remove SE or ZE
            if lsb == 0 and msb == gchild.width - 1:
                # +---------+-------------+
                # | Extend  |      e      |
                # +---------+-------------+
                #           \-- Extract --/
                return gchild
            else:
                # +------+----------------+
                # | Ext  |        e       |
                # +------+----------------+
                #           \- Extract -/
                return Extract(msb, lsb, gchild)
        elif lsb == 0:
            # We also have msb > gchild.width - 1
            # We can remove the Extract if we modify the Extension length
            # +---------------+-------+
            # | Extend        |   e   |
            # +---------------+-------+
            #           \-- Extract --/
            extendNode = ConstNodeAuto(node.width - gchild.width)
            return OpNode(child.op, [extendNode, gchild])
        elif lsb > gchild.width - 1 and extendNode.op == 'ZE':
            # +-----------------+-------+
            # | ZExt            |   e   |
            # +-----------------+-------+
            #   \-- Extract --/
            return Const(0, msb - lsb + 1)
        elif lsb >= gchild.width - 1 and extendNode.op == 'SE':
            assert(extendNode.op == 'SE')
            if gchild.width > 1:
                # +-----------------+-------+
                # | SExt            |   e   |
                # +-----------------+-------+
                #   \-- Extract --/
                gchildMsb = gchild.width - 1
                newExtractNode = Extract(gchildMsb, gchildMsb, gchild)
                return SignExt(msb - lsb, newExtractNode)
            else:
                return SignExt(msb - lsb, gchild)
        else:
            return node

    elif child.op == 'C':
        concatNode = child
        startBitIdx = lsb
        removedBitsOnRight = 0
        i = 0
        while concatNode.children[i].width <= startBitIdx:
            concatChild = concatNode.children[i]
            concatChildWidth = concatChild.width
            startBitIdx -= concatChildWidth
            removedBitsOnRight += concatChildWidth
            i += 1

        startChildIdx = i
        endBitIdx = msb - removedBitsOnRight

        i = startChildIdx
        currBitIdx = concatNode.children[i].width - 1
        while currBitIdx < endBitIdx:
            i += 1
            currBitIdx += concatNode.children[i].width
        endChildIdx = i

        if startChildIdx == endChildIdx:
            # Remove Concat
            if startBitIdx == 0 and endBitIdx == concatNode.children[startChildIdx].width - 1:
                # Also Remove Extract
                return concatNode.children[startChildIdx]
            else:
                return Extract(endBitIdx, startBitIdx, concatNode.children[startChildIdx])
        
        # Extract covers 2 children or more
        newConcatNode = Concat(*concatNode.children[startChildIdx:endChildIdx + 1][::-1])
        if startBitIdx == 0 and endBitIdx == currBitIdx:
            # Remove Extract
            return newConcatNode
        else:
            return Extract(endBitIdx, startBitIdx, newConcatNode)

    elif child.op == 'E':
        # Extract(m, l, Extract(v, u, e)) -> Extract(m + u, l + u, e)
        gMsbNode = child.children[0]
        gMsb = gMsbNode.cst
        gLsbNode = child.children[1]
        gLsb = gLsbNode.cst
        gchild = child.children[2]
        return Extract(msb + gLsb, lsb + gLsb, gchild)


    # Default case
    else:
        return node




def equivalence(node0, node1):
    node0simp = simplify(node0)
    node1simp = simplify(node1)
    return node0simp.h == node1simp.h




