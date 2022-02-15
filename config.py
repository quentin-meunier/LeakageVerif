#!/usr/bin/python

from __future__ import print_function
import sys


propagateCst = True
bitExp = True


def propagateCstOnBuild():
    return propagateCst

def bitExpEnable():
    return bitExp


def setPropagateCstOnBuild(val):
    assert(isinstance(val, bool))
    global propagateCst
    propagateCst = val

def setBitExpEnable(val):
    assert(isinstance(val, bool))
    global bitExp
    bitExp = val


