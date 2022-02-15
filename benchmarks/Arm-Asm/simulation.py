#!/usr/bin/python

from __future__ import print_function

# Choose between secmult and AES
from secmult import *
#from aes import *
from topcell import *


instList = getGeneratedInsts()

topcell = Topcell(instList, getStartAddress(), getStopAddress(), getRegisterInit(), setGeneratedMemory)

cycle = 0
while True:
    print('### Cycle %3d ###' % cycle)
    cycle += 1

    stop = topcell.advanceCycle()
    if stop:
        break
    topcell.computeOutput()
    topcell.analyse()

topcell.displayResults()

