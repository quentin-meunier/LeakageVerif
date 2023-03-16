# -*- coding: utf-8 -*-
 
# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function

from config import *
from node import *


registeredArraysByAddr = {}
registeredArraysByName = {}
registeredArrays = set()


class MemArray:
    def __init__(self, name, inWidth, outWidth, addr, size, func):
        self.name = name
        self.addr = addr
        self.size = size
        self.func = func
        self.elemSize = outWidth / 8
        self.array = ArrayExp(name, inWidth, outWidth)


def registerArray(name, inWidth, outWidth, addr, size, func):

    if addr != None:
        if addr in registeredArraysByAddr:
            print('*** Error: Array with base address 0x%x already registered' % addr)
            assert(False)

    if name in registeredArraysByName:
        print('*** Error: Array with name %s already registered' % name)
        assert(False)

    arr = MemArray(name, inWidth, outWidth, addr, size, func)

    if addr != None:
        #print('registering array %s at address %x' % (name, addr))
        registeredArraysByAddr[addr] = arr
    registeredArraysByName[name] = arr
    registeredArrays.add(arr)


def getMemArrayByAddr(addr):
    return registeredArraysByAddr[addr]

def getMemArrayByName(name):
    return registeredArraysByName[name]

def getArrayByAddr(addr):
    return registeredArraysByAddr[addr].array

def getArrayByName(name):
    return registeredArraysByName[name].array

def getArraySizeByAddr(addr):
    return registeredArraysByAddr[addr].size

def getArraySizeByName(name):
    return registeredArraysByName[name].size

def getArrayFuncByAddr(addr):
    return registeredArraysByAddr[addr].func

def getArrayFuncByName(name):
    return registeredArraysByName[name].func

def getArrayInWidth(memArray):
    return memArray.array.inWidth

def getArrayOutWidth(memArray):
    return memArray.array.outWidth



def getArrayAndOffset(addr):
    arr = None
    newChildren = []
        
    if isinstance(addr, OpNode) and addr.op == '+':
        for child in addr.children:
            if isinstance(child, ConstNode):
                arr = getMemArrayByAddr(child.cst)
            else:
                newChildren.append(child)
    if arr != None:
        if len(newChildren) == 1:
            offset = newChildren[0]
        else:
            offset = OpNode('+', newChildren)
        if arr.elemSize != 1:
            offset = simp(LShR(offset, arr.elemSize.bit_length() - 1))

        if width(offset) < getArrayInWidth(arr):
            offset = ZeroExt(getArrayInWidth(arr) - width(offset), offset)
        elif width(offset) > getArrayInWidth(arr):
            # FIXME: verify that all removed bits are 0?
            offset = Extract(getArrayInWidth(arr) - 1, 0, offset)
        return arr, offset

    # FIXME: in case symbolic array of 32-bit integers is at adress 0x1000,
    # and offset is (k ^ m) + 4, array will be searched at address 0x1004 and it will fail
    # this case will be implemented if encountered
    print('*** Error: symbolic address for symbolic array access does not contain array base address (address is %s)' % addr)
    sys.exit(1)


def getArrayAndOffsetConcrete(addr):
    # FIXME: deal with fully symbolic arrays (return array access from constant index): return arr, offset
    # and semi-symbolic arrays (return constant value from constant index): return None, None
    assert(isinstance(addr, int))
    return None, None

    for arr in registeredArrays:
        if addr >= arr.addr and addr < arr.addr + arr.size:
            offset = (addr - arr.addr) / arr.elemSize
            return arr, Const(offset, getArrayInWidth(arr))
    return None, None



def checkResults(res, ref, pei = False, usbv = False):
    from node import Node
    from simplify import simplifyCore, equivalence
    assert(isinstance(res, Node))
    assert(isinstance(ref, Node))

    nbBits = ref.width
    
    if nbBits != res.width:
        print('KO (nbBits on res: %d -- expected %d)' % (res.width, nbBits))

    res_s = simplifyCore(res, pei, usbv)
    ref_s = simplifyCore(ref, pei, usbv)

    print('res : %s [%d]' % (res_s, res_s.width))
    print('ref : %s [%d]' % (ref_s, ref_s.width))

    if nbBits != res.width or nbBits != ref.width:
        print('KO (nbBits after simplify: res: %d - ref: %d - expected: %d)' % (res.width, ref.width, nbBits))
    
    if equivalence(res_s, ref_s):
        print('OK')
    else:
        print('KO')
    

def checkTpsResult(exp, expected):
    from check_leakage import checkTpsVal
    res, t0, t1 = checkTpsVal(exp)
    if res == expected:
        print('OK')
    else:
        print('KO')


def constant(val, width):
    return Const(val, width)


def symbol(name, nature, width):
    return Symb(name, nature, width)


def litteralInteger(e):
    from simplify import simplify
    if isinstance(e, int):
        return e
    elif isinstance(e, ConstNode):
        return e.cst
    else:
        s = simplify(e)
        if isinstance(s, ConstNode):
            return s.cst
        else:
            return None
        
def width(e):
    return e.width


