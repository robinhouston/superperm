#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import math
from itertools import permutations
import optparse

parser = optparse.OptionParser(usage="%prog [options] N")

(options, args) = parser.parse_args()
if len(args) != 1: parser.error("Wrong number of arguments")
N = int(args[0])

max_weight = N
INF = 99999

SYMBOLS = "123456789ABCDEFG"

perms = list(permutations(range(N)))
n_perms = len(perms)
ordered = tuple(range(N))

def distance(p, q):
    q_ = tuple(reversed(q))
    if p == q_: return 0

    weight = INF
    for n in range(max_weight+1):
        if p[n:] == q_[:N-n]:
            weight = n
            break
    
    return weight + N*N

print "NAME : superperm %d" % (N,)
print "TYPE : ATSP"
print "DIMENSION : %d" % (n_perms,)
print "EDGE_WEIGHT_TYPE : EXPLICIT"
print "EDGE_WEIGHT_FORMAT : FULL_MATRIX"
print "NODE_COORD_TYPE : NO_COORDS"
print "DISPLAY_DATA_TYPE : NO_DISPLAY"

print "EDGE_WEIGHT_SECTION :"

for p in perms:
    print " ".join([ str(distance(p, q)) for q in perms ])
