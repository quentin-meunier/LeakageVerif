# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LIP6DROMEL project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier


from __future__ import print_function

from leakage_verif import *

test_litteral = False

def sim(e):
    return simplify(e)

nbExps = 0
nbLeak = 0

def checkExpLeakage(e):
    global nbExps
    global nbLeak
    nbExps += 1

    res, wordRes, tpsTime = checkTpsVal(e)
    if not res:
        nbLeak += 1
        print('# Leakage in value for exp num %d' % (nbExps))
        sys.exit(0)



sbox = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]


rcon = [ 1, 2, 4, 8, 16, 32, 64, 128, 27, 54 ]


def display_vector(v):
    for i in range(16):
        print('%.2x' % int(str(v[i])), end = '')
    print('')


def sub_bytes(x):
    for i in range(4):
        for j in range(4):
            e = sim(sbox[x[i][j]])
            checkExpLeakage(e)
            x[i][j] = e


def shift_rows(x):
    tmp = x[1][0]
    x[1][0] = x[1][1]
    x[1][1] = x[1][2]
    x[1][2] = x[1][3]
    x[1][3] = tmp

    tmp = x[2][0]
    x[2][0] = x[2][2]
    x[2][2] = tmp
    tmp = x[2][1]
    x[2][1] = x[2][3]
    x[2][3] = tmp

    tmp = x[3][0]
    x[3][0] = x[3][3]
    x[3][3] = x[3][2]
    x[3][2] = x[3][1]
    x[3][1] = tmp


def mix_columns(x):
    def xtime(y):
        e = y >> 7
        e = sim(e)
        checkExpLeakage(e)
        e = e & constant(0x1b, 8)
        e = sim(e)
        checkExpLeakage(e)
        f = y << 1
        f = sim(f)
        checkExpLeakage(f)
        e = f ^ e
        e = sim(e)
        checkExpLeakage(e)
        return e

    for i in range(4):
        t        = x[0][i]
        # tmp    = x[0][i] ^ x[1][i] ^ x[2][i] ^ x[3][i]
        e = x[0][i] ^ x[1][i]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ x[2][i]
        e = sim(e)
        checkExpLeakage(e)
        e = e ^ x[3][i]
        e = sim(e)
        checkExpLeakage(e)
        tmp = e

        tm       = x[0][i] ^ x[1][i]
        tm       = sim(tm)
        checkExpLeakage(tm)
        tm       = xtime(tm)

        # x[0][i] ^= tm ^ tmp
        e        = tm ^ tmp
        e        = sim(e)
        checkExpLeakage(e)
        e        = x[0][i] ^ e
        e        = sim(e)
        checkExpLeakage(e)
        x[0][i]  = e

        tm       = x[1][i] ^ x[2][i]
        tm       = sim(tm)
        checkExpLeakage(tm)
        
        tm       = xtime(tm)

        # x[1][i] ^= tm ^ tmp
        e        = tm ^ tmp
        e        = sim(e)
        checkExpLeakage(e)
        e        = x[1][i] ^ e
        e        = sim(e)
        checkExpLeakage(e)
        x[1][i]  = e

        tm       = x[2][i] ^ x[3][i]
        tm       = sim(tm)
        checkExpLeakage(tm)
 
        tm       = xtime(tm)

        # x[2][i] ^= tm ^ tmp
        e        = tm ^ tmp
        e        = sim(e)
        checkExpLeakage(e)
        e        = x[2][i] ^ e
        e        = sim(e)
        checkExpLeakage(e)
        x[2][i]  = e

        tm       = x[3][i] ^ t
        tm       = sim(tm)
        checkExpLeakage(tm)

        tm       = xtime(tm)

        # x[3][i] ^= tm ^ tmp
        e        = tm ^ tmp
        e        = sim(e)
        checkExpLeakage(e)
        e        = x[3][i] ^ e
        e        = sim(e)
        checkExpLeakage(e)
        x[3][i]  = e



def mix_column(r):
    a = {}
    b = {}
    for c in range(4):
        a[c] = r[c]
        a[c] = sim(a[c])
        checkExpLeakage(a[c])

        h = r[c] >> 7 # 8 bits
        h = sim(h)
        checkExpLeakage(h)
        b[c] = r[c] << 1
        b[c] = sim(b[c])
        checkExpLeakage(b[c])
        # b[c] ^= constant(0x1b, 8) & h
        e = constant(0x1B, 8) & h
        e = sim(e)
        checkExpLeakage(e)
        b[c] = b[c] ^ e
        b[c] = sim(b[c])
        checkExpLeakage(b[c])

    # r[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1]
    e = b[0] ^ a[3]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[2]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ b[1]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[1]
    e = sim(e)
    checkExpLeakage(e)
    r[0] = e

    # r[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2]
    e = b[1] ^ a[0]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[3]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ b[2]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[2]
    e = sim(e)
    checkExpLeakage(e)
    r[1] = e

    # r[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3]
    e = b[2] ^ a[1]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[0]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ b[3]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[3]
    e = sim(e)
    checkExpLeakage(e)
    r[2] = e

    # r[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0]
    e = b[3] ^ a[2]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[1]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ b[0]
    e = sim(e)
    checkExpLeakage(e)
    e = e ^ a[0]
    e = sim(e)
    checkExpLeakage(e)
    r[3] = e



def add_round_key(x, round_key, rnd):
    for i in range(4):
        for j in range(4):
            #x[j][i] ^= round_key[(rnd << 4) + (i << 2) + j]
            e = round_key[(rnd << 4) + (i << 2) + j]
            e = sim(e)
            checkExpLeakage(e)
            e = x[j][i] ^ e
            e = sim(e)
            checkExpLeakage(e)
            x[j][i] = e


def add_round_key_no_verif(x, round_key, rnd):
    for i in range(4):
        for j in range(4):
            #x[j][i] ^= round_key[(rnd << 4) + (i << 2) + j]
            e = round_key[(rnd << 4) + (i << 2) + j]
            e = sim(e)
            e = x[j][i] ^ e
            e = sim(e)
            x[j][i] = e


# Masked Key generation
def masked_init_masked_aes_keys(key, round_key, m, mp, mpt):
    for i in range(4):
        for j in range(4):
            # round_key[i * 4 + j] = key[i * 4 + j] ^ mpt[j] ^ m
            e = key[i * 4 + j] ^ mpt[j]
            e = sim(e)
            checkExpLeakage(e)
            e = e ^ m
            e = sim(e)
            checkExpLeakage(e)
            round_key[i * 4 + j] = e

    for i in range(4, 40):
        # Generating the keys for rounds 1 to 9
        # 1 word per iteration
        # All keys are masked with M and (M1', M2', M3', M4')
        temp = {}
        for j in range(4):
            temp[j] = round_key[(i - 1) * 4 + j]

        if i % 4 == 0:
            #k = temp[0] ^ mpt[0]
            #temp[0] = temp[1] ^ mpt[1]
            #temp[1] = temp[2] ^ mpt[2]
            #temp[2] = temp[3] ^ mpt[3]
            #temp[3] = k
            k = temp[0] ^ mpt[0]
            k = sim(k)
            checkExpLeakage(k)
            temp[0] = temp[1] ^ mpt[1]
            temp[0] = sim(temp[0])
            checkExpLeakage(temp[0])
            temp[1] = temp[2] ^ mpt[2]
            temp[1] = sim(temp[1])
            checkExpLeakage(temp[1])
            temp[2] = temp[3] ^ mpt[3]
            temp[2] = sim(temp[2])
            checkExpLeakage(temp[2])
            temp[3] = k

            # Masked with M
            for j in range(4):
                temp[j] = SBoxPrime(temp[j], m, mp)
                temp[j] = sim(temp[j])
                checkExpLeakage(temp[j])
            # Masked with M'
            temp[0] = temp[0] ^ constant(rcon[(i / 4) - 1], 8)
            temp[0] = sim(temp[0])
            checkExpLeakage(temp[0])

            # xoring with previous words adds masks M and (M1', M2', M3', M4')
            # We remask with M' to remove it
            for j in range(4):
                # round_key[i * 4 + j] = (round_key[(i - 4) * 4 + j] ^ temp[j]) ^ mp
                e = round_key[(i - 4) * 4 + j] ^ temp[j]
                e = sim(e)
                checkExpLeakage(e)
                e = e ^ mp
                e = sim(e)
                checkExpLeakage(e)
                round_key[i * 4 + j] = e
            # Masked with M and (M1', M2', M3', M4')
        else:
            # As both previous word and the same word in previous key are masked with
            # M and (M1', M2', M3', M4'), we remove M from the word in previous key
            # and (M1', M2', M3', M4') from the previous word before xoring
            for j in range(4):
                # round_key[i * 4 + j] = (round_key[(i - 4) * 4 + j] ^ m) ^ (temp[j] ^ mpt[j])
                e = round_key[(i - 4) * 4 + j] ^ m
                e = sim(e)
                checkExpLeakage(e)
                f = temp[j] ^ mpt[j]
                f = sim(f)
                checkExpLeakage(f)
                g = e ^ f
                g = sim(g)
                checkExpLeakage(g)
                round_key[i * 4 + j] = g
            # Masked with M and (M1', M2', M3', M4')

    for i in range(40, 44):
        # For the last key, we mask it with M'
        temp = {}
        for j in range(4):
            temp[j] = round_key[(i - 1) * 4 + j]
        
        if i % 4 == 0:
            #k = temp[0] ^ mpt[0]
            #temp[0] = temp[1] ^ mpt[1]
            #temp[1] = temp[2] ^ mpt[2]
            #temp[2] = temp[3] ^ mpt[3]
            #temp[3] = k
            k = temp[0] ^ mpt[0]
            k = sim(k)
            checkExpLeakage(k)
            temp[0] = temp[1] ^ mpt[1]
            temp[0] = sim(temp[0])
            checkExpLeakage(temp[0])
            temp[1] = temp[2] ^ mpt[2]
            temp[1] = sim(temp[1])
            checkExpLeakage(temp[1])
            temp[2] = temp[3] ^ mpt[3]
            temp[2] = sim(temp[2])
            checkExpLeakage(temp[2])
            temp[3] = k

            # Masked with M
            for j in range(4):
                temp[j] = SBoxPrime(temp[j], m, mp)
                temp[j] = sim(temp[j])
                checkExpLeakage(temp[j])

            # Masked with M'
            temp[0] = temp[0] ^ constant(rcon[(i / 4) - 1], 8)
            temp[0] = sim(temp[0])
            checkExpLeakage(temp[0])

            # xoring with previous words adds masks M and (M1', M2', M3', M4')
            # We remove them to only let M'
            for j in range(4):
                # round_key[i * 4 + j] = (round_key[(i - 4) * 4 + j] ^ temp[j]) ^ m ^ mpt[j]
                e = round_key[(i - 4) * 4 + j] ^ temp[j]
                e = sim(e)
                checkExpLeakage(e)
                e = e ^ m
                e = sim(e)
                checkExpLeakage(e)
                e = e ^ mpt[j]
                e = sim(e)
                checkExpLeakage(e)
                round_key[i * 4 + j] = e
            #Masked with M'
        else:
            # The previous word is masked with M' and the same word in previous key is masked with
            # M and (M1', M2', M3', M4'), we remove M and (M1', M2', M3', M4')
            for j in range(4):
                # round_key[i * 4 + j] = (round_key[(i - 4) * 4 + j] ^ temp[j]) ^ m ^ mpt[j]
                e = round_key[(i - 4) * 4 + j] ^ temp[j]
                e = sim(e)
                checkExpLeakage(e)
                e = e ^ m
                e = sim(e)
                checkExpLeakage(e)
                e = e ^ mpt[j]
                e = sim(e)
                checkExpLeakage(e)
                round_key[i * 4 + j] = e
            # Masked with M'



# Mask all bytes from line i with mpt[i]
def mask_plain_text(x, mpt):
    for i in range(4):
        x[i][0] = x[i][0] ^ mpt[i]
        x[i][1] = x[i][1] ^ mpt[i]
        x[i][2] = x[i][2] ^ mpt[i]
        x[i][3] = x[i][3] ^ mpt[i]


def masked_sub_bytes(x, m, mp):
    for i in range(4):
        for j in range(4):
            # x[i][j] = SBoxPrime(x[i][j], m, mp)
            e = SBoxPrime(x[i][j], m, mp)
            e = sim(e)
            checkExpLeakage(e)
            x[i][j] = e
 

# Changes masks:
# - from M' to M1 on the first row
# - from M' to M2 on the second row
# - from M' to M3 on the third row
# - from M' to M4 on the forth row
def change_masks(x, mp, mt):
    for i in range(4):
        for j in range(4):
            # x[i][j] = (x[i][j] ^ mt[i]) ^ mp # order is important: masking with new mask before demasking old mask
            e = x[i][j] ^ mt[i]
            e = sim(e)
            checkExpLeakage(e)
            e = e ^ mp
            e = sim(e)
            checkExpLeakage(e)
            x[i][j] = e



def SBox(e):
    if isinstance(e, ConstNode):
        return Const(sbox[e.cst], 8)
    sb = getArrayByName('sbox')
    return sb[e]
    


def SBoxPrime(e, m, mp):
    return SBox(e ^ m) ^ mp



def masked_aes(key, pt, ct, m, mp, mt):

    mpt = {} # M' table : (M1', M2', M3', M4')

    # Init mpt
    mpt[0] = mt[0]
    mpt[1] = mt[1]
    mpt[2] = mt[2]
    mpt[3] = mt[3]
    mix_column(mpt)

    x = {}
    for i in range(4):
        x[i] = {}
        for j in range(4):
            x[i][j] = pt[i * 4 + j]

    # Masking plain text with (M1', M2', M3', M4')
    # - with M1' on the first row
    # - with M2' on the second row
    # - with M3' on the third row
    # - with M4' on the forth row
    mask_plain_text(x, mpt)

   
    ### START analysis ###

    round_key = {}
    print('# Start Key Schedule')
    masked_init_masked_aes_keys(key, round_key, m, mp, mpt)
    print('# End of Key Schedule, starting AES')

    # Rounds
    for rnd in range(9):
        print('# Round %d' % rnd)
        print('# ARK')
        # Add round key: changes mask from (M1', M2', M3', M4') to M
        add_round_key(x, round_key, rnd)

        print('# SB')
        # SBox': changes mask M to M'
        masked_sub_bytes(x, m, mp)


        print('# ShiftRows')
        # Shift rows: does not change mask
        shift_rows(x)


        print('# ChangeMasks')
        # Changes masks from M' to (M1, M2, M3, M4)
        change_masks(x, mp, mt)


        print('# MixColumns')
        # Mix columns: changes masks from  (M1, M2, M3, M4) to (M1', M2', M3', M4')
        r = {}
        for col in range(4):
            r[0] = x[0][col]
            r[1] = x[1][col]
            r[2] = x[2][col]
            r[3] = x[3][col]
            mix_column(r)
            x[0][col] = r[0]
            x[1][col] = r[1]
            x[2][col] = r[2]
            x[3][col] = r[3]


        if not test_litteral:
            print('# End of Round %d' % rnd)
            print('# Nb. expressions analysed: %d' % nbExps)
            print('# Nb. expressions leaking: %d' % nbLeak)


    # Final Round (no Mix Columns)
    # Add round key: changes mask from (M1', M2', M3', M4') to M
    print('# Final Round (9)')
    print('# ARK')
    add_round_key(x, round_key, 9)
    # SBox': changes mask M to M'
    print('# SB')
    masked_sub_bytes(x, m, mp)
    print('# ShiftRows')
    shift_rows(x)

    ### End analysis ###

    # Add round key: removes mask M'
    print('# ARK')
    add_round_key_no_verif(x, round_key, 10) # must leak because the masks are removed...

    # Writing output ciphered text
    for i in range(16):
        # ct[i] = x[i % 4][i / 4]
        e = x[i % 4][i / 4]
        #checkExpLeakage(e) # leaks because masks have been removed
        ct[i] = e
    print('# End of AES')
    print('# Total Nb. of expression analysed: %d' % nbExps)
    print('# Total Nb. of expression leaking: %d' % nbLeak)



if __name__ == '__main__':

    if test_litteral:
        pt = {}
        for i in range(16):
            pt[i] = constant(0x00, 8)

        key = {}
        key[0] = constant(0x80, 8)
        for i in range(1, 16):
            key[i] = constant(0x00, 8)

        m = constant(0x83, 8)
        mp = constant(0x7E, 8)
        mt = {} # M table : (M1, M2, M3, M4)
        mt[0] = constant(0xFA, 8)
        mt[1] = constant(0x49, 8)
        mt[2] = constant(0xA0, 8)
        mt[3] = constant(0x3c, 8)

        print("Plain text:    ", end = '')
        display_vector(pt)

        print("Key:           ", end = '')
        display_vector(key)
        
        ct = {}
        masked_aes(key, pt, ct, m, mp, mt)

        print('Cyphered text (Masked AES): ', end = '')
        display_vector(ct)

    else:
        registerArray('sbox', 8, 8, None, 256, None)

        pt = {}
        for i in range(16):
            pt[i] = symbol('pt%.2d' % i, 'P', 8)

        key = {}
        for i in range(0, 16):
            key[i] = symbol('k%.2d' % i, 'S', 8)

        m = symbol('m', 'M', 8) # M
        mp = symbol('mp', 'M', 8) # M'
        mt = {} # M table : (M1, M2, M3, M4)
        for i in range(4):
            mt[i] = symbol('m%d' % i, 'M', 8)

        ct = {}
        
        masked_aes(key, pt, ct, m, mp, mt)


