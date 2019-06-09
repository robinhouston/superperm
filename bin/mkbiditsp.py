#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import math
from itertools import permutations
import optparse

parser = optparse.OptionParser(usage="%prog [options] N")
parser.add_option("-b", "--bound", type="int", help="only include edges up to this weight")
parser.add_option("-n", "--no-cyclic", action="store_true", help="no edges between non-adjacent cyclic permutations")
parser.add_option("-s", "--simple", action="store_true", help="only include edges from a.b -> b.a^r")
parser.add_option("", "--perms", action="store", help="File containing a list of permutations")

(options, args) = parser.parse_args()
if len(args) != 1: parser.error("Wrong number of arguments")
N = int(args[0])

if options.bound:
    max_weight = options.bound
else:
    max_weight = N
INF = 99999

SYMBOLS = "123456789ABCDEFG"

if options.perms:
    perms = [ line.strip() for line in open(options.perms, 'r') ]
else:
    perms = list(permutations(range(N)))

n_perms = len(perms)
ordered = tuple(range(N))

def distance(p, q):
    if p == q: return INF
    
    weight = INF
    if options.simple:
        for n in range(max_weight+1):
            if p[n:] + tuple(reversed(p[:n])) == q:
                weight = n
                break
    else:
        for n in range(max_weight+1):
            if p[n:] == q[:N-n]:
                weight = n
                break
    
    if weight > 1 and options.no_cyclic:
        sp = "".join([ SYMBOLS[i] for i in p ])
        sq = "".join([ SYMBOLS[i] for i in q ])
        if sp in sq+sq: return INF
    
    return weight

def bidi(p, q):
    return min(distance(p, q), distance(q, p))

print "NAME : superperm %d" % (N,)
print "TYPE : TSP"
print "DIMENSION : %d" % (n_perms + 1,)
print "EDGE_WEIGHT_TYPE : EXPLICIT"
print "EDGE_WEIGHT_FORMAT : UPPER_ROW"
print "NODE_COORD_TYPE : NO_COORDS"
print "DISPLAY_DATA_TYPE : NO_DISPLAY"

print "EDGE_WEIGHT_SECTION :"

print " ".join([ "0" for p in perms ])
for (i, p) in enumerate(perms):
    print " ".join([ str(bidi(p, q)) for q in perms[i+1 :] ])
