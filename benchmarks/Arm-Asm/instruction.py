#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function



class Instruction:

    usesBusAList = ['asr', 'asrs', 'cmp', 'eor', 'eors', 'eor.w', 'ors', 'and', 'add', 'adds', 'rd1', 'wr1', 'sub', 'subs', 'subs.w', 'not', 'sbfx', 'ubfx', 'uxtb']
    usesBusBList = ['asr', 'asrs', 'cmp', 'eor', 'eors', 'eor.w', 'ors', 'and', 'add', 'adds', 'rd1', 'wr1', 'wr2', 'mov', 'mov.w', 'movs', 'sub', 'subs.w', 'subs', 'sbfx', 'ubfx', 'lsr', 'lsrs', 'lsl', 'lsls']

    writesRegBankList = ['asr', 'asrs', 'eor', 'eors', 'eor.w', 'ors', 'and', 'add', 'adds', 'rd2', 'mov', 'mov.w', 'movs', 'sub', 'subs.w', 'subs.s', 'subs', 'sbfx', 'ubfx', 'uxtb', 'lsr', 'lsrs', 'lsl', 'lsls']

    loadList = ['ldr', 'ldrb', 'rd1', 'rd2']
    storeList = ['str', 'strb', 'str_pre', 'wr1', 'wr2']

    def __init__(self, addr, op, rd, ra, rb, rc, imm, sh, shOp, width, size, wbPre, wbPost):
        self.addr = addr
        self.op = op
        self.rd = rd
        self.ra = ra
        self.rb = rb
        self.rc = rc
        self.imm = imm
        self.sh = sh # shift amount
        self.shOp = shOp
        self.size = size # 1, 2, or 4 (for Mem Accesses)
        self.width = width # for sbfx and ubfx : number of bits extracted
        self.wbPre = wbPre
        self.wbPost = wbPost

    def __str__(self):
        s = ''
        s += '[0x%x] ' % self.addr
        s += self.op
        if self.rd != None:
            s += ' rd = r%d;' % self.rd
        if self.ra != None:
            s += ' ra = r%d;' % self.ra
        if self.rb != None:
            s += ' rb = r%d;' % self.rb
        if self.rc != None:
            s += ' rc = r%d;' % self.rc
        if self.imm != None:
            s += ' imm = 0x%x;' % self.imm
        if self.shOp != None:
            s += ' shOp = %s;' % self.shOp
        if self.sh != None:
            s += ' sh = %d;' % self.sh
        if self.width != None:
            s+= '  width = %d;' % self.width
        if self.wbPre:
            s += ' !'
        if self.wbPost:
            s += ' post'
        return s

    def isLoad(self):
        return self.op in self.loadList or self.op.startswith('ldr')

    def isStore(self):
        return self.op in self.storeList or self.op.startswith('str')
    
    def isMemInst(self):
        return self.isLoad() or self.isStore()

    def hasImm(self):
        return self.imm != None

    def isStoreRegOffset(self):
        return self.isStore() and self.rc != None

    def isLoadRegOffset(self):
        return self.isLoad() and self.rb != None

    def uses_BusA(self):
        return self.op in Instruction.usesBusAList or self.op.startswith('ldr') or self.op.startswith('str')    

    def uses_BusB(self):
        return self.op in Instruction.usesBusBList or self.op.startswith('ldr') or self.op.startswith('str')

    @staticmethod
    def usesBusA():
        return Instruction.usesBusAList

    @staticmethod
    def usesBusB():
        return Instruction.usesBusBList

    @staticmethod
    def writesRegBank():
        return Instruction.writesRegBankList

    @staticmethod
    def makeLdrInst(addr, rd, ra, imm, wbPre, wbPost):
        inst = Instruction(addr, 'ldr', rd, ra, None, imm, None, None, 4, wbPre, wbPost)
        return inst

    @staticmethod
    def makeLdrbInst(addr, rd, ra, imm, wbPre, wbPost):
        inst = Instruction(addr, 'ldrb', rd, ra, None, imm, None, None, 1, wbPre, wbPost)
        return inst

    @staticmethod
    def makeStrbInst(addr, rv, ra, imm, wbPre, wbPost):
        inst = Instruction(addr, 'strb', None, ra, rv, imm, None, None, 1, wbPre, wbPost)
        return inst

    @staticmethod
    def makeStrbRegInst(addr, rd, ra, rb, wbPre, wbPost):
        inst = Instruction(addr, 'strb', rd, ra, rb, None, None, None, 1, wbPre, wbPost) 
        return inst

    @staticmethod
    def makeEorsInst(addr, rd, ra, rb):
        inst = Instruction(addr, 'eors', rd, ra, rb, None, None, None, None, None, None)
        return inst

    @staticmethod
    def makeEorwInst(addr, rd, ra, rb, sh):
        inst = Instruction(addr, 'eor.w', rd, ra, rb, None, sh, None, None, None, None)
        return inst

    @staticmethod
    def makeAndInst(addr, rd, ra, imm):
        inst = Instruction(addr, 'and', rd, ra, None, imm, None, None, None, None, None)
        return inst

    @staticmethod
    def makeSubswInst(addr, rd, ra, imm):
        inst = Instruction(addr, 'subs.w', rd, ra, None, imm, None, None, None, None, None)
        return inst

    @staticmethod
    def makeMovInst(addr, rd, rb):
        inst = Instruction(addr, 'mov', rd, None, rb, None, None, None, None, None, None)
        return inst

    @staticmethod
    def makeMovwInst(addr, rd, imm):
        inst = Instruction(addr, 'mov.w', rd, None, None, imm, None, None, None, None, None)
        return inst

    @staticmethod
    def makeSbfxInst(addr, rd, ra, imm, width):
        inst = Instruction(addr, 'sbfx', rd, ra, None, imm, None, width, None, None, None)
        return inst

    @staticmethod
    def makeUbfxInst(addr, rd, ra, imm, width):
        inst = Instruction(addr, 'ubfx', rd, ra, None, imm, None, width, None, None, None)
        return inst

    @staticmethod
    def makeBlInst(addr):
        inst = Instruction(addr, 'bl', None, None, None, None, None, None, None, None, None)
        return inst

    @staticmethod
    def makeBxInst(addr, rs):
        inst = Instruction(addr, 'bx', None, rs, None, None, None, None, None, None, None)
        return inst










