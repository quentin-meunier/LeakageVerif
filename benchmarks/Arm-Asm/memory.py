#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LIP6DROMEL project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function
import sys

from leakage_verif import *


class Memory:

    def __init__(self, name, topcell, setMemory):
        self.name = name
        self.topcell = topcell
        self.mem = {}
        self.symbols = {}
        
        setMemory(self)


    @staticmethod
    def addrPlusOffset(a):
        if not isinstance(a.getRoot(), OpNode) or a.getRoot().op != '+' or len(a.getRoot().children) != 2:
            return None, None
        if isinstance(a.getRoot().children[0], ConstNode):
            offset = a - Const(a.getRoot().children[0].cst, a.getRoot().children[0].width)
            offset = simplify(offset)
            return a.getRoot().children[0].cst, offset
        elif not isinstance(a.getRoot().children[1], ConstNode):
            return None, None
        else:
            offset = a - Const(a.getRoot().children[1].cst, a.getRoot().children[1].width)
            offset = simplify(offset)
            return a.getRoot().children[0].cst, offset


    def ldr(self, base, offset):
        base = litteralInteger(base)
        assert(base != None)
        o = litteralInteger(offset)
        if o == None:
            try:
                arr = getMemArrayByAddr(base)
            except:
                print('*** Error: Array at address 0x%x not registered' % int(str(base)))
                assert(False)
            #if (1 << width(offset)) != arr.size:
            #    print('*** Warning: Access at address 0x%x: array size is %d while expression is on %d bits' % (base, arr.size, width(offset)))
            if arr.func == None:
                return arr.array[offset]
            else:
                return arr.func(self, offset)
        addr = (base + o) % (1 << 32)
        if self.topcell.debug:
            print('# Ldr address : 0x%x' % addr)
        if addr in self.mem and addr + 1 in self.mem and addr + 2 in self.mem and addr + 3 in self.mem:
            n = Concat(self.mem[addr + 3], self.mem[addr + 2], self.mem[addr + 1], self.mem[addr])
            n = simplify(n)
            return n
        else:
            print('*** Error: Address 0x%x is not in memory' % addr)
            assert(False)
            # FIXME: what to do when the accessed word has not been initialized or only partially?
            #mem[addr] = BitVec('Byte_%x' % addr), 8)
            #mem[addr + 1] = BitVec('Byte_%x' % addr + 1), 8)
            #mem[addr + 2] = BitVec('Byte_%x' % addr + 2), 8)
            #mem[addr + 3] = BitVec('Byte_%x' % addr + 3), 8)
            #return Concat(mem[addr + 3], mem[addr + 2], mem[addr + 1], mem[addr])
    
    
    def ldrb(self, base, offset):
        base = litteralInteger(base)
        assert(base != None)
        o = litteralInteger(offset)
        if o == None:
            try:
                arr = getMemArrayByAddr(base)
            except:
                print('*** Error: Array at address 0x%x not registered' % int(str(base)))
                assert(False)
            #if (1 << width(offset)) != arr.size:
            #    print('*** Warning: Access at address 0x%x: array size is %d while expression is on %d bits' % (base, arr.size, width(offset)))
            if arr.func == None:
                return arr.array[offset]
            else:
                return arr.func(self, offset)

        addr = (base + o) % (1 << 32)
        if self.topcell.debug:
            print('# Ldrb address : 0x%x' % addr)
        # for all registered arrays
        if addr in self.mem:
            return self.mem[addr]
        else:
            print('*** Error: Address 0x%x is not in memory' % addr)
            assert(False)
    
    
    def strw(self, base, offset, v):
        if v is None:
            print('*** Warning: trying to store None')
            assert(False)

        base = litteralInteger(base)
        assert(base != None)
        o = litteralInteger(offset)
        if o == None:
            try:
                arr = getMemArrayByAddr(base)
            except:
                print('*** Error: Array at address 0x%x not registered' % int(str(base)))
                assert(False)
            print('*** Warning: store at symbolic address %s -- ignored' % offset)
            return

        assert(width(v) == 32)
        addr = (base + o) % (1 << 32)
        if self.topcell.debug:
            print('# Store w: mem[0x%x] <- %s' % (addr, v))

        n0 = Extract(7, 0, v)
        n1 = Extract(15, 8, v)
        n2 = Extract(23, 16, v)
        n3 = Extract(31, 24, v)
        n0 = simplify(n0)
        n1 = simplify(n1)
        n2 = simplify(n2)
        n3 = simplify(n3)

        self.setVal(addr, n0)
        self.setVal(addr + 1, n1)
        self.setVal(addr + 2, n2)
        self.setVal(addr + 3, n3)
    

    def strb(self, base, offset, v):
        base = litteralInteger(base)
        assert(base != None)
        o = litteralInteger(offset)
        if o == None:
            try:
                arr = getMemArrayByAddr(base)
            except:
                print('*** Error: Array at address 0x%x not registered' % int(str(base)))
                assert(False)
            print('*** Warning: store at symbolic address %s -- ignored' % offset)
            return

        assert(width(v) >= 8)
        addr = (base + o) % (1 << 32)
        if self.topcell.debug:
            print('# Store b: mem[0x%x] <- %s' % (addr, v))
        if width(v) > 8:
            n = Extract(7, 0, v)
            self.setVal(addr, n)
        else:
            self.setVal(addr, v)

    def setVal(self, addr, val):
        self.mem[addr] = val

    def registerSymbol(self, symb, nature, width):
        assert(symb not in self.symbols)
        s = symbol(symb, nature, width)
        self.symbols[symb] = s
        return s

    def getSymbol(self, symbName):
        try:
            return self.symbols[symbName]
        except:
            return None



