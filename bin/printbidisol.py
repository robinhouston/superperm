#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

from itertools import permutations
import math
import optparse
import sys

SYMBOLS = "123456789ABCDEFG"

parser = optparse.OptionParser(usage="%prog [options] N xx.sol")
parser.add_option("", "--perms", action="store", help="File containing a list of permutations")

(options, args) = parser.parse_args()
if len(args) != 2: parser.error("Wrong number of arguments")

n = int(args[0])
sol_filename = args[1]

if options.perms:
    perms = [ line.strip() for line in open(options.perms, 'r') ]
else:
    perms = [ "".join([ SYMBOLS[i] for i in p ]) for p in permutations(range(n)) ]
n_perms = len(perms)

def read_sol(sol_filename):
    with open(sol_filename, 'r') as f:
        nodes = int(next(f).strip())
        if nodes != math.factorial(n) + 1:
            raise Exception("Unexpected number of nodes: " + str(nodes))

        for line in f:
            for ix in map(int, line.strip().split()):
                if ix > 0:
                    yield perms[ix - 1]

def squash(xs):
    return reduce(lambda x, y: x + y[overlap(x, y):], xs, "")

def overlap(x, y):
    n = min(len(x), len(y))
    for i in range(n, -1, -1):
        if x[len(x)-i:] == y[:i]:
            return i

for p in read_sol(sol_filename):
    print p
