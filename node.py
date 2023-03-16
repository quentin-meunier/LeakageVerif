#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier


from __future__ import print_function
from config import *

import sys
import hashlib



class ArrayExp(object):

    allArrays = {}

    def __init__(self, name, inWidth, outWidth):
        if not isinstance(name, str):
            print('*** Error: ArrayExp name must be a string')
            assert(False)
        if name in ArrayExp.allArrays:
            print('*** Error: ArrayExp name %s already used' % name)
            assert(False)
        self.name = name
        self.inWidth = inWidth
        self.outWidth = outWidth
        ArrayExp.allArrays[name] = self

    def __getitem__(self, child):
        if child.width != self.inWidth:
            print('*** Error: Expression %s has a width of %d which cannot be used to index array %s with a width of %d' % (child, child.width, self.name, self.inWidth))
            assert(False)
        nameNode = Str(self.name)
        return OpNode('A', [nameNode, child])


class Node(object):

    associativeOps = ['^', '+', '&', '|', '*', '**']
    bitwiseOps = ['^', '&', '|', '~']
    maskingOps = ['^', '+']
    preserveMaskingOps = ['~', 'A', '-']
        
    symb2node = {}
    cst2node = {}
    str2node = {}
   
    nodeNum = 0

    def __init__(self):
        self.children = []
        self.num = Node.nodeNum
        Node.nodeNum += 1
        
        # Cache to Extract node for each bit
        self.extractBit = [None] * self.width
        # Cache for the concatenation of all the extracted bits, with single bit variables
        self.concatExtEq = None
        self.simpEq = None # simplified equivalent node
        self.simpEqUsbv = None # simplified equivalent node using single-bit variables

        self.secretVarOcc = {}
        self.publicVarOcc = {}
        self.preservedMask = None
        self.currentlyMasking = {}
        self.maskingMaskOcc = {}
        self.otherMaskOcc = {}
        self.h = None # hash


    def printVarOcc(self):
        #print('Masks: {', end = '')
        #for m in self.maskVarOcc.keys():
        #    print('%s: %d; ' % (m.symb, self.maskVarOcc[m]), end = '')
        #print('}')
        print('Secrets: {', end = '')
        for m in self.secretVarOcc.keys():
            print('%s: %d; ' % (m.symb, self.secretVarOcc[m]), end = '')
        print('}')
        print('Public {', end = '')
        for m in self.publicVarOcc.keys():
            print('%s: %d; ' % (m.symb, self.publicVarOcc[m]), end = '')
        print('}')


    def printMaskOcc(self):
        if self.preservedMask != None:
            if self.preservedMask[1] == None:
                ch1 = 'None'
            elif self.preservedMask[1] == self:
                ch1 = 'self'
            else:
                ch1 = '%s' % self.preservedMask[1]
            #print('# Preserved Mask: (%s, %s)' % (self.preservedMask[0], ch1))
        else:
            print('# Preserved Mask: None')

        print('# Currently masking:')
        for m in self.currentlyMasking:
            print('#    Mask %s' % m)
            #print('#        CTR: %s' % self.currentlyMasking[m])
        print('# Masking mask occurrences:')
        for m in self.maskingMaskOcc:
            print('#    Mask %s' % m)
            for ctrBase in self.maskingMaskOcc[m]:
                #print('#        ctrBase %s' % ctrBase)
                for ctr in self.maskingMaskOcc[m][ctrBase]:
                    #print('#            ctr %s' % ctr)
                    print('#                count:  %d' % self.maskingMaskOcc[m][ctrBase][ctr][0])
                    print('#                height: %d' % self.maskingMaskOcc[m][ctrBase][ctr][1])
        print('# Other mask occurrences:')
        for m in self.otherMaskOcc:
            print('#    Mask %s' % m)
            for p in self.otherMaskOcc[m]:
                #print('#        Parent: %s' % p)
                print('#            count: %d' % self.otherMaskOcc[m][p])



    def setVarsOccurrences(self):
        if isinstance(self, ConstNode):
            return
        if isinstance(self, SymbNode):
            if self.symbType == 'M':
                self.preservedMask = (self, None) # (mask, parent)
                self.otherMaskOcc[self] = None
            elif self.symbType == 'P':
                self.publicVarOcc[self] = 1
            elif self.symbType == 'S':
                self.secretVarOcc[self] = 1
            return
        for child in self.children:
            for p in child.publicVarOcc:
                if p in self.publicVarOcc:
                    self.publicVarOcc[p] += child.publicVarOcc[p]
                else:
                    self.publicVarOcc[p] = child.publicVarOcc[p]
            for k in child.secretVarOcc:
                if k in self.secretVarOcc:
                    self.secretVarOcc[k] += child.secretVarOcc[k]
                else:
                    self.secretVarOcc[k] = child.secretVarOcc[k]


    def dump(self, filename):
        def fillReachableNodes(n, rn):
            if n not in rn:
                rn.add(n)
            for child in n.children:
                fillReachableNodes(child, rn)

        reachableNodes = set()
        fillReachableNodes(self, reachableNodes)
        Node.dumpNodes(filename, reachableNodes)


    @staticmethod
    def dumpNodes(filename, nodes):
        f = open(filename, 'w')
        content = 'digraph g {\n'
        for n in nodes:
            if isinstance(n, SymbNode):
                s = 'Symbol: %s [%s]' % (n.symb, n.symbType)
            elif isinstance(n, OpNode):
                if n.op == '|':
                    s = 'Op: \\| (num %d)' % n.num
                elif n.op == '<<':
                    s = 'Op: \\<\\<'
                elif n.op == 'LS':
                    s = 'Op: LShR'
                elif n.op == '>>':
                    s = 'Op: \\>\\>'
                else:
                    s = 'Op: %s (num %d)' % (n.op, n.num)
            elif isinstance(n, ConstNode):
                s = 'Const: %d' % n.cst
            else:
                s = ''
            content += '   N%d [shape=record, label=\"{%s}\"];\n' % (n.num, s)
            for a in n.children:
                content += '   edge[tailclip=true];\n'
                content += '   N%d -> N%d\n' % (n.num, a.num)
        content += '}'
        f.write(content)
        f.close()

    def __and__(self, other):
        e = self.makeBitwiseNode('&', [self, other])
        return e

    def __or__(self, other):
        e = self.makeBitwiseNode('|', [self, other])
        return e

    def __xor__(self, other):
        e = self.makeBitwiseNode('^', [self, other])
        return e

    def __invert__(self):
        n = self.makeBitwiseNode('~', [self])
        return n

    def __add__(self, other):
        n = self.makeBitwiseNode('+', [self, other])
        return n

    def makeBitwiseNode(self, op, children):
        assert(children != None and children)
        width = children[0].width
        for child in children:
            assert(child.width == width)
            assert(isinstance(child, Node))
        if propagateCstOnBuild():
            allChildrenCst = True
            for child in children:
                if not isinstance(child, ConstNode):
                    allChildrenCst = False
                    break
            if allChildrenCst:
                if op == '&':
                    res = ~0
                elif op == '*' or op == '**':
                    res = 1
                else:
                    res = 0
                for child in children:
                    if op == '^':
                        res = res ^ child.cst
                    elif op == '&':
                        res = res & child.cst
                    elif op == '|':
                        res = res | child.cst
                    elif op == '~':
                        res = (1 << width) - 1 - child.cst
                    elif op == '+':
                        res = (res + child.cst) % (1 << width)
                    elif op == '*':
                        res = gmulInt(res, child.cst)
                    elif op == '**':
                        res = imulInt(res, child.cst, width)
                    else:
                        assert(False)

                return Const(res, width)

        n = OpNode(op, children)
        return n

    def __sub__(self, other):
        assert(isinstance(other, Node))
        if propagateCstOnBuild():
            if isinstance(self, ConstNode) and isinstance(other, ConstNode):
                return Const((self.cst - other.cst) % (1 << self.width), self.width)
        n = self + (-other)
        return n

    def __neg__(self):
        if propagateCstOnBuild():
            if isinstance(self, ConstNode):
                return Const(-self.cst % (1 << self.width), self.width)
        n = OpNode('-', [self])
        return n

    def __lshift__(self, shval):
        if isinstance(shval, ConstNode):
            shval = shval.cst
        if not isinstance(shval, int):
            print('*** Error: Second operand of a Shift operation can only be a constant')
            assert(False)

        width = self.width
        if shval >= width:
            print('*** Warning: shift value (%d) >= bit width of expression (%d)' % (shval, width))

        if propagateCstOnBuild() and isinstance(self, ConstNode):
            n = Const((self.cst << shval) % (1 << width), width)
            return n

        sh = Const(shval, shval.bit_length())
        n = OpNode('<<', [self, sh])
        return n

    def __rshift__(self, shval):
        # Arith Shift Right
        if isinstance(shval, ConstNode):
            shval = shval.cst
        if not isinstance(shval, int):
            print('*** Error: Second operand of a Shift operation can only be a constant')
            assert(False)

        width = self.width
        if shval >= width:
            print('*** Warning: shift value (%d) >= bit width of expression (%d)' % (shval, width))

        if propagateCstOnBuild() and isinstance(self, ConstNode):
            cst = self.cst
            if cst >> (width - 1) == 1: # MSB == 1
                mod = 1 << width
                n = Const(~((~cst % mod) >> shval) % mod, width)
            else:
                n = Const(cst >> shval, width)
            return n

        sh = Const(shval, shval.bit_length())
        n = OpNode('>>', [self, sh])
        return n

    def __mul__(self, other):
        assert(isinstance(other, Node))
        if propagateCstOnBuild():
            if isinstance(self, ConstNode) and isinstance(other, ConstNode):
                return gmul(self, other)
        n = self.makeBitwiseNode('*', [self, other])
        return n

    def __pow__(self, other):
        assert(isinstance(other, Node))
        if propagateCstOnBuild():
            if isinstance(self, ConstNode) and isinstance(other, ConstNode):
                return imul(self, other)
        n = self.makeBitwiseNode('**', [self, other])
        return n




    def __str__(self):
        return self.expPrint(False, False)

    def verbatimPrint(self):
        return self.expPrint(False, True)



class FinalNode(Node):
    def __init__(self, width):
        self.width = width
        Node.__init__(self)


class SymbNode(FinalNode):
    def __init__(self, symb, symbType, width):
        self.symb = symb
        self.symbType = symbType
        self.op = None
        self.hasWordOp = False
        self.wordAnalysisHasFailedOnSubExp = False
        FinalNode.__init__(self, width)
        self.setVarsOccurrences()
        self.simpEq = self
        self.h = hashlib.sha256(self.symb).hexdigest()

    def toString(self):
        return super().toString(self) + ' Symb<%d> %s [%s]' % (self.width, self.symb, self.symbType)

    def expPrint(self, parNeeded, verbatim):
        return '%s' % self.symb



class ConstNode(FinalNode):
    def __init__(self, cst, width):
        self.cst = cst
        self.op = None
        self.hasWordOp = False
        self.wordAnalysisHasFailedOnSubExp = False
        FinalNode.__init__(self, width)
        self.simpEq = self
        self.h = hashlib.sha256(str(self.cst)).hexdigest()

    def toString(self):
        return super().toString(self) + ' Const<%d> %d' % (self.width, self.cst)

    def expPrint(self, parNeeded, verbatim):
        if verbatim:
            return 'Const(%d, %d)' % (self.cst, self.width)
        else:
            return '0x%.2x' % self.cst


class StrNode(FinalNode):
    def __init__(self, s):
        self.strn = s
        self.op = None
        self.hasWordOp = False
        self.wordAnalysisHasFailedOnSubExp = False
        FinalNode.__init__(self, 0)
        self.simpEq = self
        self.h = hashlib.sha256(s).hexdigest()

    def toString(self):
        return super().toString(self) + ' String<%d> %s' % (self.width, self.strn)

    def expPrint(self, parNeeded, verbatim):
        if verbatim:
            return '%s' % self.strn
        else:
            return '%s' % self.strn



class OpNode(Node):
    def __init__(self, op, children):
        assert(children != None and children)
        self.op = op
        self.hasWordOp = (op == '*' or op == '**')
        if not self.hasWordOp:
            for c in children:
                if c.hasWordOp:
                    self.hasWordOp = True
                    break
        self.wordAnalysisHasFailedOnSubExp = False
        for c in children:
            if c.wordAnalysisHasFailedOnSubExp:
                self.wordAnalysisHasFailedOnSubExp = True
                break

        if op == '+' or op == '--' or op == '-' or op == '&' or op == '|' or op == '^' or op == '~' or op == '<<' or op == '>>' or op == 'LS' or op == '*' or op == '**':
            self.width = children[0].width
        elif op == 'ZE' or op == 'SE':
            self.width = children[0].cst + children[1].width
        elif op == 'C':
            width = 0
            for child in children:
                width += child.width
            self.width = width
        elif op == 'E':
            self.width = children[0].cst - children[1].cst + 1
        elif op == 'A':
            self.width = ArrayExp.allArrays[children[0].strn].outWidth
        else:
            print("op = %s" % op)
            assert(False)


        Node.__init__(self)

        for child in children:
            assert(isinstance(child, Node))
            self.children.append(child)

        self.setVarsOccurrences()

        # Examples to have in mind
        #
        #          +          ^         +       +      +     +
        #         /|\        /|\       / \     / \    / \   / \
        #        / | \      e n ~      \ /     \ /    \ /   ~ ~
        #      m1  ^  m0        |       ~       m      ~    | |
        #         / \           ^       |              |    m m
        #        m0  k         / \      ^              m
        #                     k   ~    / \
        #                         |   k   m
        #                         m


        # Occurrences in currentlyMasking are also present in maskingMaskOcc
        # Mask in preservedMask is also present in otherMaskOcc

        # "Masking" mask occurrences
        for child in children:
            for m in child.maskingMaskOcc:
                if m not in self.maskingMaskOcc:
                    self.maskingMaskOcc[m] = {}
                for ctrBase in child.maskingMaskOcc[m]:
                    if ctrBase not in self.maskingMaskOcc[m]:
                        self.maskingMaskOcc[m][ctrBase] = {}
                    for ctr in child.maskingMaskOcc[m][ctrBase]:
                        if ctr not in self.maskingMaskOcc[m][ctrBase]:
                            entry = child.maskingMaskOcc[m][ctrBase][ctr]
                            # entry[0] : count (number of occurrences)
                            # entry[1] : height of ctr starting from ctrBase (0 for ctrBase)
                            self.maskingMaskOcc[m][ctrBase][ctr] = [entry[0], entry[1]]
                        else:
                            self.maskingMaskOcc[m][ctrBase][ctr][0] += child.maskingMaskOcc[m][ctrBase][ctr][0]

 
        # For other mask occurrences, we do the union of all the children
        for child in children:
            for m in child.otherMaskOcc:
                if m not in self.otherMaskOcc:
                    self.otherMaskOcc[m] = {}
                if child.otherMaskOcc[m] == None:
                    if self in self.otherMaskOcc[m]:
                        self.otherMaskOcc[m][self] += 1
                    else:
                        self.otherMaskOcc[m][self] = 1
                else:
                    for p in child.otherMaskOcc[m]:
                        if p in self.otherMaskOcc[m]:
                            self.otherMaskOcc[m][p] += child.otherMaskOcc[m][p]
                        else:
                            self.otherMaskOcc[m][p] = child.otherMaskOcc[m][p]



        # currentlyMasking: Masks masking current node, value is ctrBase
        # preservedMask: bijection of a mask, can mask if a maskingNode is encountered. tuple if not None: (mask, parent)
        if op in Node.maskingOps:
            # Conditions for a mask to become a "currently masking" mask in a maskingOp node:
            # - it must be a "currently masking" mask or a preserved mask of one of the children
            # - it must not have other occurrences in any other child (masking or other occ)
            for i in range(len(children)):
                child = children[i]
                # FIXME: can it be done in one pass? (without the 2nd for loop on children)
                for m in child.currentlyMasking:
                    maskIsMasking = True
                    for j in range(len(children)):
                        if i == j:
                            continue
                        other = children[j]
                        if m in other.maskingMaskOcc or m in other.otherMaskOcc:
                            maskIsMasking = False
                            break
                    if maskIsMasking:
                        self.currentlyMasking[m] = child.currentlyMasking[m]
                        # Adding mask to masking mask occ
                        height = child.maskingMaskOcc[m][child.currentlyMasking[m]][child][1]
                        self.maskingMaskOcc[m][child.currentlyMasking[m]][self] = [1, height + 1]

                if child.preservedMask != None:
                    m = child.preservedMask[0]
                    parent = child.preservedMask[1]
                    maskIsMasking = True
                    for j in range(len(children)):
                        if i == j:
                            continue
                        other = children[j]
                        if m in other.maskingMaskOcc or m in other.otherMaskOcc:
                            maskIsMasking = False
                            break
                    if maskIsMasking:
                        self.currentlyMasking[m] = self

                        # Removing mask occurrence from otherOccurrences
                        if parent == None:
                            parent = self
                        self.otherMaskOcc[m][parent] -= 1
                        if self.otherMaskOcc[m][parent] == 0:
                            del self.otherMaskOcc[m][parent]
                            if len(self.otherMaskOcc[m]) == 0:
                                del self.otherMaskOcc[m]

                        # Adding mask to masking mask occurrences
                        if m not in self.maskingMaskOcc:
                            self.maskingMaskOcc[m] = {}
                        self.maskingMaskOcc[m][self] = {}
                        self.maskingMaskOcc[m][self][self] = [1, 0]

        elif op in Node.preserveMaskingOps:
            if op == 'A':
                child = children[1]
            else:
                #assert(op == '~' or op == '-')
                child = children[0]

            if child.preservedMask != None:
                if child.preservedMask[1] != None:
                    self.preservedMask = child.preservedMask
                else:
                    self.preservedMask = (child.preservedMask[0], self)

            self.currentlyMasking = child.currentlyMasking
            # Creating new masking occurrences for masks masking current node
            for m in self.currentlyMasking:
                ctrBase = self.currentlyMasking[m]
                height = child.maskingMaskOcc[m][ctrBase][child][1]
                self.maskingMaskOcc[m][ctrBase][self] = [1, height + 1]
        
        # if node is neither a masking node nor a preserving node, currently masking masks and preserved masks are empty
            

        if op in Node.associativeOps:
            self.children.sort(key = lambda x:x.h)
        self.h = hashlib.sha256(op + ''.join(map(lambda x:x.h, self.children))).hexdigest()



    def expPrint(self, parNeeded, verbatim):
        assert(isinstance(self, OpNode))
        if self.op == '~':
            res = '~' + self.children[0].expPrint(True, verbatim)
            return res
        elif self.op == '-':
            res = '-' + self.children[0].expPrint(True, verbatim)
            return res
        elif self.op == 'ZE':
            res = 'ZeroExt(' + str(self.children[0].cst) + ', ' + self.children[1].expPrint(False, verbatim) + ')'
            return res
        elif self.op == 'SE':
            res = 'SignExt(' + str(self.children[0].cst) + ', ' + self.children[1].expPrint(False, verbatim) + ')'
            return res
        elif self.op == 'C':
            res = 'Concat(' + ', '.join(map(lambda x:x.expPrint(False, verbatim), self.children[::-1])) + ')'
            return res
        elif self.op == 'E':
            #if isinstance(self.children[2], SymbNode) and self.children[0].cst == self.children[1].cst:
            #    res = self.children[2].expPrint(False, verbatim) + '#' + str(self.children[0].cst)
            #else:
            res = 'Extract(' + str(self.children[0].cst) + ', ' + str(self.children[1].cst) + ', ' + self.children[2].expPrint(False, verbatim) + ')'
            return res
        elif self.op == 'A':
            res = self.children[0].strn + '[' + self.children[1].expPrint(False, verbatim) + ']'
            return res
        elif self.op == 'LS':
            res = 'LShR(' + self.children[0].expPrint(False, verbatim) + ', ' + str(self.children[1].cst) + ')'
            return res
        elif (self.op == '>>' or self.op == '<<'):
            res = self.children[0].expPrint(True, verbatim) + ' ' + self.op + ' ' + str(self.children[1].cst)
            if parNeeded:
                res = '(' + res + ')'
            return res

        res = ''
        for idx in range(len(self.children)):
            res += self.children[idx].expPrint(True, verbatim)
            if idx != len(self.children) - 1:
                res += ' %s ' % self.op
        if parNeeded:
            res = '(' + res + ')'
        return res

    def __str__(self):
        return self.expPrint(False, False)



def Symb(symb, symbType, width):
    if '#' in symb:
        print('*** Error: symbol name (%s) cannot contain the \'#\' character' % (symb))
        sys.exit(1)
    if symb in Node.symb2node:
        print('*** Error: symbol %s has already been defined' % symb)
        assert(False)
        sys.exit(1)
    return SymbInternal(symb, symbType, width)



def SymbInternal(symb, symbType, width):
    if symb in Node.symb2node:
        return Node.symb2node[symb]
    else:
        n = SymbNode(symb, symbType, width)
        Node.symb2node[symb] = n
        return n


def Const(cst, width):
    def makeConstNode(cst, nbBits):
        if nbBits in Node.cst2node.keys():
            if cst in Node.cst2node[nbBits].keys():
                return Node.cst2node[nbBits][cst]
            else:
                n = ConstNode(cst, nbBits)
                Node.cst2node[nbBits][cst] = n
                return n
        else:
            Node.cst2node[nbBits] = {}
            n = ConstNode(cst, nbBits)
            Node.cst2node[nbBits][cst] = n
            return n

    if cst >= 0:
        if cst.bit_length() > width:
            print('*** Error: constant %d cannot be coded on %d bits' % (cst, width))
            assert(False)
        node = makeConstNode(cst, width)
        return node
    else:
        if cst < -(1 << (width - 1)):
            print('*** Error: constant %d cannot be coded on %d bits' % (cst, width))
            assert(False)
        # Storing positive value
        cst = cst % (1 << width)
        node = makeConstNode(cst, width)
        return node


def Str(s):
    if s in Node.str2node.keys():
        return Node.str2node[s]
    else:
        n = StrNode(s)
        Node.str2node[s] = n
        return n


def LShR(child, shval):
    assert(isinstance(child, Node))
    
    if isinstance(shval, ConstNode):
        shval = shval.cst
    if not isinstance(shval, int):
        print('*** Error: Second operand of a Shift operation can only be a constant')
        assert(False)

    width = child.width
    if shval >= width:
        print('*** Warning: shift value (%d) >= bit width of expression (%d)' % (shval, width))

    if propagateCstOnBuild() and isinstance(child, ConstNode):
        n = Const(child.cst >> shval, width)
        return n

    sh = Const(shval, shval.bit_length())

    n = OpNode('LS', [child, sh])
    return n


def RotateRight(child, shval):
    assert(isinstance(child, Node))
    
    if isinstance(shval, ConstNode):
        shval = shval.cst
    if not isinstance(shval, int):
        print('*** Error: Second operand of a Shift operation can only be a constant')
        assert(False)

    width = child.width
    if shval >= width:
        print('*** Warning: shift value (%d) >= bit width of expression (%d)' % (shval, width))

    return Concat(Extract(shval - 1, 0, child), Extract(width - 1, shval, child))


def Concat(*children):
    assert(children != None and children)
    for child in children:
        assert(isinstance(child, Node))

    if len(children) == 1:
        return children[0]

    if propagateCstOnBuild():
        allChildrenCst = True
        for child in children:
            if not isinstance(child, ConstNode):
                allChildrenCst = False
                break
        if allChildrenCst:
            cstRes = 0
            currNbBits = 0
            for child in reversed(children):
                cstRes += child.cst << currNbBits
                currNbBits += child.width
            newConstExp = Const(cstRes, currNbBits)
            return newConstExp

    # Inverting list so that child 0 of node has weight 0
    n = OpNode('C', children[::-1])
    return n


def Extract(msb, lsb, child):
    assert(isinstance(child, Node))
    
    if isinstance(msb, ConstNode):
        msb = msb.cst
    if isinstance(lsb, ConstNode):
        lsb = lsb.cst

    if not isinstance(msb, int) or not isinstance(lsb, int):
        print('*** Error: msb and lsb parameters of makeExtractNode must be integer constants')
        assert(False)

    if msb < lsb:
        print('*** Error: msb must be greater than or equal to lsb')
        assert(False)

    width = child.width
    if msb < 0 or msb >= width or lsb < 0 or lsb >= width:
        print('*** Error: msb and lsb parameters must be comprised between 0 and %d' % (width - 1))
        assert(False)

    if propagateCstOnBuild() and isinstance(child, ConstNode):
        # Directly create a const node
        cst = child.cst
        assert(cst >= 0)
        cstString = format(cst, '0%db' % width)[::-1]
        newCstString = cstString[lsb:msb + 1]
        newCst = int(newCstString[::-1], 2)
        n = Const(newCst, msb - lsb + 1)
        return n

    # Since there is no more reference duplication in roots,
    # the process for removing useless nodes in simpler
    if msb == lsb and child.extractBit[lsb] != None:
        return child.extractBit[lsb]

    msbNode = Const(msb, msb.bit_length())
    lsbNode = Const(lsb, lsb.bit_length())
    n = OpNode('E', [msbNode, lsbNode, child])
    if msb == lsb:
        child.extractBit[lsb] = n

    return n



def ZeroExt(numZeros, child):
    assert(isinstance(child, Node))

    if isinstance(numZeros, ConstNode):
        numZeros = numZeros.cst

    if not isinstance(numZeros, int):
        print('*** Error: numZeros must be an integer constant')
        assert(False)

    if numZeros <= 0:
        print('*** Error: numZeros must be greater than 0')
        assert(False)

    if propagateCstOnBuild() and isinstance(child, ConstNode):
        cst = child.cst
        assert(cst >= 0)
        n = Const(cst, child.width + numZeros)
        return n

    numZerosNode = Const(numZeros, numZeros.bit_length())
    n = OpNode('ZE', [numZerosNode, child])
    return n


def SignExt(numSignBits, child):
    assert(isinstance(child, Node))

    if isinstance(numSignBits, ConstNode):
        numSignBits = numSignBits.cst

    if not isinstance(numSignBits, int):
        print('*** Error: numSignBits must be an integer constant')
        assert(False)

    if numSignBits <= 0:
        print('*** Error: numSignBits must be greater than 0')
        assert(False)

    if propagateCstOnBuild() and isinstance(child, ConstNode):
        width = child.width
        cst = child.cst
        assert(cst >= 0)
        if cst >> (width - 1) == 1: # MSB == 1
            cst = (1 << (width + numSignBits)) + (cst - (1 << width))
        n = Const(cst, width + numSignBits)
        return n

    numSignBitsNode = Const(numSignBits, numSignBits.bit_length())
    n = OpNode('SE', [numSignBitsNode, child])
    return n


def gmul(n0, n1):
    assert(n0.width == 8 and n1.width == 8)
    return Const(gmulInt(n0.cst, n1.cst), 8)


def gmulInt(a, b):
    assert(a >= 0 and a < 256)
    assert(b >= 0 and b < 256)
    p = 0
    for i in range(8):
        p = (((b & 1) * 0xff) & a) ^ p
        a = (a << 1) ^ ((((a & 0x80) >> 7) * 0xff) & 0x11b)
        b >>= 1
    assert(p < 256)
    return p;


def imul(n0, n1):
    assert(n0.width == n1.width)
    return Const(imulInt(n0.cst, n1.cst, n0.width), n0.width)


def imulInt(a, b, w):
    return (a * b) % (1 << w)






