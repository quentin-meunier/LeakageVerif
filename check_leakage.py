#!/usr/bin/python

# Copyright (C) 2021, Sorbonne Universite, LIP6
# This file is part of the LIP6DROMEL project, under the GPL v3.0 license
# See https://www.gnu.org/licenses/gpl-3.0.en.html for license information
# SPDX-License-Identifier: GPL-3.0-only
# Author(s): Quentin L. Meunier

from __future__ import print_function
import timeit

from node import *
from simplify import *
from tps import *
from utils import *



def checkTpsVal(e):
    tpsTimerStart = timeit.default_timer()

    if e.hasWordOp:
        resTps = False
        usedBitExp = False
        if not e.wordAnalysisHasFailedOnSubExp:
            resTps = tps(e)
            if not resTps:
                e.wordAnalysisHasFailedOnSubExp = True

        if not resTps and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
        else:
            usedBitExp = False
            resTps = tps(e)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return resTps, usedBitExp, tpsTime


def checkTpsTrans(e0, e1):
    tpsTimerStart = timeit.default_timer()
    e = Concat(e0, e1)

    if e.hasWordOp:
        resTps = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            resTps = tps(e)
            # FIXME: if only transition and no value, how to make the flag become true? check each exp independently? Make an external set for storing this information instead of storing it in nodes? Or only for transitions?
            #if not resTps:
            #    e0.wordAnalysisHasFailedOnSubExp = True
            #    e1.wordAnalysisHasFailedOnSubExp = True

        if not resTps and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
        else:
            usedBitExp = False
            resTps = tps(e)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return resTps, usedBitExp, tpsTime


def checkTpsTransBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0

        assert(e0.width == e1.width)

        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = Concat(simplifyCore(Extract(b, b, e0), True, True), simplifyCore(Extract(b, b, e1), True, True))

            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart

            if not resTps:
                break

        return resTps, tpsTime
    else:
        return False, 0


def checkTpsTransXor(e0, e1):
    assert(e0.width == e1.width)
    tpsTimerStart = timeit.default_timer()
    e = simplify(e0 ^ e1)

    if e.hasWordOp:
        resTps = False
        usedBitExp = False
        if not (e0.wordAnalysisHasFailedOnSubExp or e1.wordAnalysisHasFailedOnSubExp):
            resTps = tps(e)
            # FIXME: if only transition and no value, how to make the flag become true? check each exp independently?
            #if not resTps:
            #    e0.wordAnalysisHasFailedOnSubExp = True
            #    e1.wordAnalysisHasFailedOnSubExp = True

        if not resTps and bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
    else:
        if bitExpEnable():
            be = getBitDecomposition(e)
            usedBitExp = True
            resTps = tps(be)
        else:
            usedBitExp = False
            resTps = tps(e)

    tpsTimerEnd = timeit.default_timer()
    tpsTime = tpsTimerEnd - tpsTimerStart
    return resTps, usedBitExp, tpsTime


def checkTpsTransXorBit(e0, e1):
    if bitExpEnable():
        tpsTime = 0

        assert(e0.width == e1.width)

        for b in range(e0.width - 1, -1, -1):
            tpsTimerStart = timeit.default_timer()
            be = simplifyCore(Extract(b, b, e0) ^ Extract(b, b, e1), True, True)

            resTps = tps(be)
            tpsTimerEnd = timeit.default_timer()
            tpsTime += tpsTimerEnd - tpsTimerStart

            if not resTps:
                break

        return resTps, tpsTime
    else:
        return False, 0


