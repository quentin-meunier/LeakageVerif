#!/usr/bin/python

from __future__ import print_function

from config import *
from utils import *
from node import *
from simplify import *



def getReplacedGraph(node, selMask, childToReplace):
    def getReplacedGraphRec(node, selMask, childToReplace, m):
        if not isinstance(node, OpNode):
            return node
        children = []
        for child in node.children:
            if child in m:
                children.append(m[child])
                continue
            if child is selMask:
                children.append(childToReplace)
                continue
            if child is childToReplace:
                children.append(selMask)
                continue
            #if selMask in child.maskVarOcc:
            if selMask in child.maskingMaskOcc or selMask in child.otherMaskOcc:
                newChild = getReplacedGraphRec(child, selMask, childToReplace, m)
                children.append(newChild)
            else:
                children.append(child)
        n = OpNode(node.op, children)
        m[node] = n
        return n

    return getReplacedGraphRec(node, selMask, childToReplace, {})


def tps(n):
    #print('# Call func tps on exp %s' % n)
    node = n
    res = tpsRun(node)
    return res


def tpsRun(nodeIn):

    node = simplify(nodeIn)

    masksTaken = set()
    cpt = 0
    while True:
        #print('# Starting iteration %d' % cpt)
        #print('# e = %s' % node)
        #node.dump('dot/graph_%d.dot' % cpt)
        cpt += 1

        if len(node.secretVarOcc) == 0:
            #print('# No more secret')
            return True
       
        if len(node.currentlyMasking) != 0:
            return True
 
        # Choice of CTR:
        # - Choose mask m which minimizes the number of nodes with occurrence of m (CTR Bases + other Occ)
        # - For this m, choose CTR Base with the highest count
        # - For this CTR Base, choose the CTR with the max height for the same count
        maskingMaskOcc = node.maskingMaskOcc
        otherMaskOcc = node.otherMaskOcc
        minOcc = 1000000 # FIXME...
        selMask = None
        for m in maskingMaskOcc:
            if m in masksTaken:
                continue

            if m in maskingMaskOcc:
                nbMaskingOp = len(maskingMaskOcc[m])
            else:
                continue

            if m in otherMaskOcc:
                nbOtherOp = len(otherMaskOcc[m])
            else:
                nbOtherOp = 0

            nbOcc = nbMaskingOp + nbOtherOp
            if nbOcc < minOcc:
                minOcc = nbOcc
                selMask = m

        if selMask == None:
            #print('# No mask can be taken')
            return False

        #print('# Choosing mask %s (number of parent nodes: %d)' % (selMask, minOcc))

        maxCount = 0
        selCtrBase = None
        occs = maskingMaskOcc[selMask]
        for ctrBase in occs:
            if occs[ctrBase][ctrBase][0] > maxCount:
                maxCount = occs[ctrBase][ctrBase][0]
                selCtrBase = ctrBase

        #print('# Choosing following ctr base with %d occurrences: %s' % (maxCount, selCtrBase))

        maxHeight = -1
        selCtr = None
        for ctr in occs[selCtrBase]:
            height = occs[selCtrBase][ctr][1]
            if occs[selCtrBase][ctr][0] == maxCount and height > maxHeight:
                maxHeight = height
                selCtr = ctr
        
        #print('# Choosing following ctr with a height of %d: %s' % (maxHeight, selCtr))

        # FIXME: do a deterministic choice? (for each of the three choices, add a comparison on node hash)

        masksTaken.add(selMask)
        node = getReplacedGraph(node, selMask, selCtr)

        #print('# Replacing %s with %s' % (selCtr, selMask))
        #print('# and other occurrences of %s with %s' % (selMask, selCtr))

        #node.dump('dot/graph_%d_end.dot' % (cpt - 1))

        # Simplify
        node = simplify(node)


