# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LeakageVerif project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Inès Ben El Ouahma, Quentin L. Meunier

from leakage_verif import *
from instruction import *


def simp(x):
    return simplify(x)


def getRegisterInit():
    registerInit = {}
    for i in range(0,13):
        registerInit[i] = constant(0, 32)
    registerInit[13] = constant(0x7fff0000, 32)
    registerInit[14] = constant(0, 32)
    registerInit[15] = constant(0x00008030, 32)
    return registerInit


def setGeneratedMemory(mem):
    # symbols init
    m10 = mem.registerSymbol('m10', 'M', 8)
    b1 = mem.registerSymbol('b1', 'P', 8)
    k1 = mem.registerSymbol('k1', 'S', 8)
    k0 = mem.registerSymbol('k0', 'S', 8)
    m1 = mem.registerSymbol('m1', 'M', 8)
    m0 = mem.registerSymbol('m0', 'M', 8)
    a1 = mem.registerSymbol('a1', 'P', 8)
    m01 = mem.registerSymbol('m01', 'M', 8)
    c1 = mem.registerSymbol('c1', 'P', 8)
    c0 = mem.registerSymbol('c0', 'P', 8)

    # mem init
    mem.mem[0x18a08] = simp(Extract(7,0,constant(0x00000000,32)))
    mem.mem[0x18a09] = simp(Extract(15,8,constant(0x00000000,32)))
    mem.mem[0x18a0a] = simp(Extract(23,16,constant(0x00000000,32)))
    mem.mem[0x18a0b] = simp(Extract(31,24,constant(0x00000000,32)))
    mem.mem[0x18a0c] = simp(Extract(7,0,constant(0x00000000,32)))
    mem.mem[0x18a0d] = simp(Extract(15,8,constant(0x00000000,32)))
    mem.mem[0x18a0e] = simp(Extract(23,16,constant(0x00000000,32)))
    mem.mem[0x18a0f] = simp(Extract(31,24,constant(0x00000000,32)))
    mem.mem[0x18a10] = simp(Extract(7,0,constant(0x00000000,32)))
    mem.mem[0x18a11] = simp(Extract(15,8,constant(0x00000000,32)))
    mem.mem[0x8128] = simp(Extract(7,0,constant(0x00018a08,32)))
    mem.mem[0x8129] = simp(Extract(15,8,constant(0x00018a08,32)))
    mem.mem[0x812a] = simp(Extract(23,16,constant(0x00018a08,32)))
    mem.mem[0x812b] = simp(Extract(31,24,constant(0x00018a08,32)))

    mem.mem[0x812c] = simp(Extract(7,0,constant(0x00018a0e,32)))
    mem.mem[0x812d] = simp(Extract(15,8,constant(0x00018a0e,32)))
    mem.mem[0x812e] = simp(Extract(23,16,constant(0x00018a0e,32)))
    mem.mem[0x812f] = simp(Extract(31,24,constant(0x00018a0e,32)))

    mem.mem[0x8130] = simp(Extract(7,0,constant(0x00018a11,32)))
    mem.mem[0x8131] = simp(Extract(15,8,constant(0x00018a11,32)))
    mem.mem[0x8132] = simp(Extract(23,16,constant(0x00018a11,32)))
    mem.mem[0x8133] = simp(Extract(31,24,constant(0x00018a11,32)))

    mem.mem[0x8134] = simp(Extract(7,0,constant(0x00018a0f,32)))
    mem.mem[0x8135] = simp(Extract(15,8,constant(0x00018a0f,32)))
    mem.mem[0x8136] = simp(Extract(23,16,constant(0x00018a0f,32)))
    mem.mem[0x8137] = simp(Extract(31,24,constant(0x00018a0f,32)))

    mem.mem[0x8138] = simp(Extract(7,0,constant(0x00018a0a,32)))
    mem.mem[0x8139] = simp(Extract(15,8,constant(0x00018a0a,32)))
    mem.mem[0x813a] = simp(Extract(23,16,constant(0x00018a0a,32)))
    mem.mem[0x813b] = simp(Extract(31,24,constant(0x00018a0a,32)))

    mem.mem[0x813c] = simp(Extract(7,0,constant(0x00018a0b,32)))
    mem.mem[0x813d] = simp(Extract(15,8,constant(0x00018a0b,32)))
    mem.mem[0x813e] = simp(Extract(23,16,constant(0x00018a0b,32)))
    mem.mem[0x813f] = simp(Extract(31,24,constant(0x00018a0b,32)))

    mem.mem[0x8140] = simp(Extract(7,0,constant(0x00018a0c,32)))
    mem.mem[0x8141] = simp(Extract(15,8,constant(0x00018a0c,32)))
    mem.mem[0x8142] = simp(Extract(23,16,constant(0x00018a0c,32)))
    mem.mem[0x8143] = simp(Extract(31,24,constant(0x00018a0c,32)))

    mem.mem[0x8144] = simp(Extract(7,0,constant(0x00018a09,32)))
    mem.mem[0x8145] = simp(Extract(15,8,constant(0x00018a09,32)))
    mem.mem[0x8146] = simp(Extract(23,16,constant(0x00018a09,32)))
    mem.mem[0x8147] = simp(Extract(31,24,constant(0x00018a09,32)))

    mem.mem[0x8148] = simp(Extract(7,0,constant(0x00018a10,32)))
    mem.mem[0x8149] = simp(Extract(15,8,constant(0x00018a10,32)))
    mem.mem[0x814a] = simp(Extract(23,16,constant(0x00018a10,32)))
    mem.mem[0x814b] = simp(Extract(31,24,constant(0x00018a10,32)))

    mem.mem[0x814c] = simp(Extract(7,0,constant(0x00018a0d,32)))
    mem.mem[0x814d] = simp(Extract(15,8,constant(0x00018a0d,32)))
    mem.mem[0x814e] = simp(Extract(23,16,constant(0x00018a0d,32)))
    mem.mem[0x814f] = simp(Extract(31,24,constant(0x00018a0d,32)))

    # symbols init
    testLitteral = False
    if testLitteral:
        mem.mem[0x18a08] = constant(0xb9, 8)
        mem.mem[0x18a0f] = constant(0x66, 8)
        mem.mem[0x18a0c] = constant(0x37, 8)
        mem.mem[0x18a0e] = constant(0xa1, 8)
        mem.mem[0x18a11] = constant(0x0f, 8)
    else:
        mem.mem[0x18a08] = m0
        mem.mem[0x18a0f] = m1
        mem.mem[0x18a0c] = m01
        mem.mem[0x18a0e] = k0
        mem.mem[0x18a11] = k1
    mem.mem[0x18a09] = m10
    mem.mem[0x18a0a] = b1
    mem.mem[0x18a0b] = a1
    mem.mem[0x18a0d] = c1
    mem.mem[0x18a10] = c0


def getStartAddress():
    return 0x8265

def getStopAddress():
    return 0x8269


def getRandAddress():
    return None


def getGeneratedInsts():
    insts = []
    # 802d push.w, sp { r3 r4 r5 r6 r7 r8 r9 lr }
    i = Instruction(0x1, 'str_pre', None, 14, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 9, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 8, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 7, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 6, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 5, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 4, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    i = Instruction(0x1, 'str_pre', None, 3, 13, None, -4, None, None, None, 4, True, False)
    insts.append(i)

    # 8031 ldr r0, pc, #0x000000f4
    i = Instruction(0x8031, 'ldr', 0, 15, None, None, 244, None, None, None, 4, False, False)
    insts.append(i)

    # 8033 ldr r3, pc, #0x000000f8
    i = Instruction(0x8033, 'ldr', 3, 15, None, None, 248, None, None, None, 4, False, False)
    insts.append(i)

    # 8035 ldr r1, pc, #0x000000f8
    i = Instruction(0x8035, 'ldr', 1, 15, None, None, 248, None, None, None, 4, False, False)
    insts.append(i)

    # 8037 ldr r5, pc, #0x000000fc
    i = Instruction(0x8037, 'ldr', 5, 15, None, None, 252, None, None, None, 4, False, False)
    insts.append(i)

    # 8039 ldrb r4, r1
    i = Instruction(0x8039, 'ldrb', 4, 1, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 803b ldrb r2, r0
    i = Instruction(0x803b, 'ldrb', 2, 0, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 803d ldrb r7, r3
    i = Instruction(0x803d, 'ldrb', 7, 3, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 803f ldrb r3, r5
    i = Instruction(0x803f, 'ldrb', 3, 5, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8041 ldr r1, pc, #0x000000f4
    i = Instruction(0x8041, 'ldr', 1, 15, None, None, 244, None, None, None, 4, False, False)
    insts.append(i)

    # 8043 ldr r6, pc, #0x000000f8
    i = Instruction(0x8043, 'ldr', 6, 15, None, None, 248, None, None, None, 4, False, False)
    insts.append(i)

    # 8045 eors r3, r3, r4
    i = Instruction(0x8045, 'eors', 3, 3, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8047 eors r2, r2, r7
    i = Instruction(0x8047, 'eors', 2, 2, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8049 strb, r3, r1
    i = Instruction(0x8049, 'strb', None, 3, 1, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 804b strb, r2, r6
    i = Instruction(0x804b, 'strb', None, 2, 6, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 804d bl, #0x00008265
    i = Instruction(0x804d, 'bl', None, None, None, None, 33381, None, None, None, None, None, None)
    insts.append(i)

    # 8265 bx, lr
    i = Instruction(0x8265, 'bx', None, 14, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8051 ldrb r0, r0
    i = Instruction(0x8051, 'ldrb', 0, 0, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8053 ldrb r1, r1
    i = Instruction(0x8053, 'ldrb', 1, 1, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8055 mov r3, r0
    i = Instruction(0x8055, 'mov', 3, 0, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8057 mov r4, r1
    i = Instruction(0x8057, 'mov', 4, 1, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8059 mov.w r8, #0x00000008
    i = Instruction(0x8059, 'mov', 8, None, None, None, 8, None, None, None, None, None, None)
    insts.append(i)

    # 805d mov.w lr
    i = Instruction(0x805d, 'mov', 14, None, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8061 sbfx r2, r3, #0x00000007, #1
    i = Instruction(0x8061, 'sbfx', 2, 3, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 8065 sbfx r7, r4, #1
    i = Instruction(0x8065, 'sbfx', 7, 4, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8069 and r2, r2, #0x0000001b
    i = Instruction(0x8069, 'and', 2, 2, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 806d eor.w r2, r2, r3 LSL 1
    i = Instruction(0x806d, 'eor', 2, 2, 3, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8071 subs.w r8, r8, #0x00000001
    i = Instruction(0x8071, 'subs', 8, 8, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8075 and.w r3, r3, r7
    i = Instruction(0x8075, 'and', 3, 3, 7, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8079 eor.w lr, lr, r3
    i = Instruction(0x8079, 'eor', 14, 14, 3, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 807d lsr.w r4, r4, #0x00000001
    i = Instruction(0x807d, 'lsr', 4, 4, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8081 uxtb r3, r2
    i = Instruction(0x8081, 'uxtb', 3, 2, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8083 bne, #0x00008061
    i = Instruction(0x8083, 'b', None, None, None, None, 32865, None, None, None, None, None, None)
    insts.append(i)

    # 8085 ldrb r4, r6
    i = Instruction(0x8085, 'ldrb', 4, 6, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8087 ldrb r5, r5
    i = Instruction(0x8087, 'ldrb', 5, 5, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8089 mov r2, r4
    i = Instruction(0x8089, 'mov', 2, 4, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 808b mov r9, r5
    i = Instruction(0x808b, 'mov', 9, 5, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 808d mov.w ip, #0x00000008
    i = Instruction(0x808d, 'mov', 12, None, None, None, 8, None, None, None, None, None, None)
    insts.append(i)

    # 8091 ldr r3, pc, #0x000000ac
    i = Instruction(0x8091, 'ldr', 3, 15, None, None, 172, None, None, None, 4, False, False)
    insts.append(i)

    # 8093 ldrb r7, r3
    i = Instruction(0x8093, 'ldrb', 7, 3, None, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8095 eor.w r6, r7, lr
    i = Instruction(0x8095, 'eor', 6, 7, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8099 uxtb r6, r6
    i = Instruction(0x8099, 'uxtb', 6, 6, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 809b sbfx r3, r2, #0x00000007, #1
    i = Instruction(0x809b, 'sbfx', 3, 2, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 809f sbfx lr, r9, #1
    i = Instruction(0x809f, 'sbfx', 14, 9, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80a3 and r3, r3, #0x0000001b
    i = Instruction(0x80a3, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80a7 eor.w r3, r3, r2 LSL 1
    i = Instruction(0x80a7, 'eor', 3, 3, 2, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80ab subs.w ip, ip, #0x00000001
    i = Instruction(0x80ab, 'subs', 12, 12, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80af and.w r2, r2, lr
    i = Instruction(0x80af, 'and', 2, 2, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b3 eor.w r8, r8, r2
    i = Instruction(0x80b3, 'eor', 8, 8, 2, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80b7 lsr.w r9, r9, #0x00000001
    i = Instruction(0x80b7, 'lsr', 9, 9, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80bb uxtb r2, r3
    i = Instruction(0x80bb, 'uxtb', 2, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80bd bne, #0x0000809b
    i = Instruction(0x80bd, 'b', None, None, None, None, 32923, None, None, None, None, None, None)
    insts.append(i)

    # 80bf mov lr, ip
    i = Instruction(0x80bf, 'mov', 14, 12, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80c1 movs r2, #0x00000008
    i = Instruction(0x80c1, 'movs', 2, None, None, None, 8, None, None, None, None, None, None)
    insts.append(i)

    # 80c3 eor.w r6, r6, r8
    i = Instruction(0x80c3, 'eor', 6, 6, 8, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80c7 ldr r3, pc, #0x0000007c
    i = Instruction(0x80c7, 'ldr', 3, 15, None, None, 124, None, None, None, 4, False, False)
    insts.append(i)

    # 80c9 uxtb r6, r6
    i = Instruction(0x80c9, 'uxtb', 6, 6, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80cb strb, r6, r3
    i = Instruction(0x80cb, 'strb', None, 6, 3, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80cd sbfx r3, r0, #0x00000007, #1
    i = Instruction(0x80cd, 'sbfx', 3, 0, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80d1 sbfx ip, r5, #1
    i = Instruction(0x80d1, 'sbfx', 12, 5, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 80d5 and r3, r3, #0x0000001b
    i = Instruction(0x80d5, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 80d9 eor.w r3, r3, r0 LSL 1
    i = Instruction(0x80d9, 'eor', 3, 3, 0, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 80dd subs r2, r2, #0x00000001
    i = Instruction(0x80dd, 'subs', 2, 2, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80df and.w r0, r0, ip
    i = Instruction(0x80df, 'and', 0, 0, 12, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e3 eor.w lr, lr, r0
    i = Instruction(0x80e3, 'eor', 14, 14, 0, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80e7 lsr.w r5, r5, #0x00000001
    i = Instruction(0x80e7, 'lsr', 5, 5, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 80eb uxtb r0, r3
    i = Instruction(0x80eb, 'uxtb', 0, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 80ed bne, #0x000080cd
    i = Instruction(0x80ed, 'b', None, None, None, None, 32973, None, None, None, None, None, None)
    insts.append(i)

    # 80ef movs r0, #0x00000008
    i = Instruction(0x80ef, 'movs', 0, None, None, None, 8, None, None, None, None, None, None)
    insts.append(i)

    # 80f1 ldr r3, pc, #0x00000054
    i = Instruction(0x80f1, 'ldr', 3, 15, None, None, 84, None, None, None, 4, False, False)
    insts.append(i)

    # 80f3 eor.w r7, r7, lr
    i = Instruction(0x80f3, 'eor', 7, 7, 14, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 80f7 strb, r7, r3
    i = Instruction(0x80f7, 'strb', None, 7, 3, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 80f9 sbfx r3, r4, #0x00000007, #1
    i = Instruction(0x80f9, 'sbfx', 3, 4, None, None, 7, None, None, 1, None, None, None)
    insts.append(i)

    # 80fd sbfx r5, r1, #1
    i = Instruction(0x80fd, 'sbfx', 5, 1, None, None, 0, None, None, 1, None, None, None)
    insts.append(i)

    # 8101 and r3, r3, #0x0000001b
    i = Instruction(0x8101, 'and', 3, 3, None, None, 27, None, None, None, None, None, None)
    insts.append(i)

    # 8105 eor.w r3, r3, r4 LSL 1
    i = Instruction(0x8105, 'eor', 3, 3, 4, None, None, 1, 'lsl', None, None, None, None)
    insts.append(i)

    # 8109 subs r0, r0, #0x00000001
    i = Instruction(0x8109, 'subs', 0, 0, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 810b and.w r4, r4, r5
    i = Instruction(0x810b, 'and', 4, 4, 5, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 810f eor.w r2, r2, r4
    i = Instruction(0x810f, 'eor', 2, 2, 4, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 8113 lsr.w r1, r1, #0x00000001
    i = Instruction(0x8113, 'lsr', 1, 1, None, None, 1, None, None, None, None, None, None)
    insts.append(i)

    # 8117 uxtb r4, r3
    i = Instruction(0x8117, 'uxtb', 4, 3, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8119 bne, #0x000080f9
    i = Instruction(0x8119, 'b', None, None, None, None, 33017, None, None, None, None, None, None)
    insts.append(i)

    # 811b ldr r3, pc, #0x00000030
    i = Instruction(0x811b, 'ldr', 3, 15, None, None, 48, None, None, None, 4, False, False)
    insts.append(i)

    # 811d eors r2, r2, r6
    i = Instruction(0x811d, 'eors', 2, 2, 6, None, None, None, None, None, None, None, None)
    insts.append(i)

    # 811f strb, r2, r3
    i = Instruction(0x811f, 'strb', None, 2, 3, None, 0, None, None, None, 1, False, False)
    insts.append(i)

    # 8121 bl, #0x00008269
    i = Instruction(0x8121, 'bl', None, None, None, None, 33385, None, None, None, None, None, None)
    insts.append(i)

    # 8269 bx, lr
    i = Instruction(0x8269, 'bx', None, 14, None, None, 0, None, None, None, None, None, None)
    insts.append(i)

    # 8125 pop.w sp { r3 r4 r5 r6 r7 r8 r9 pc }

    return insts
