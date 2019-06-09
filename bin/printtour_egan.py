#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

from itertools import permutations
import sys

SYMBOLS = "123456789ABCDEFG"

n = int(sys.argv[1])
tour_filename = sys.argv[2]

perms = list(permutations(range(n)))
n_perms = len(perms)

def read_tour(tour_filename):
    with open(tour_filename, 'r') as f:
        tour_section = False
        for line in f:
            if line.startswith("TOUR_SECTION"):
                tour_section = True
            elif tour_section:
                ix = int(line)
                if ix == -1: break
                yield "".join([ SYMBOLS[i] for i in perms[ix - 1] ])

def squash(xs):
    return reduce(lambda x, y: x + y[overlap(x, y):], xs, "")

def overlap(x, y):
    n = min(len(x), len(y))
    for i in range(n, -1, -1):
        if x[len(x)-i:] == y[:i]:
            return i

def elim(perms):
    first = next(perms)
    second = next(perms)
    if first == reversed(second):
        yield second
        next(perms)
    else:
        yield first

    for p in perms:
        yield p
        next(perms)

# for p in elim(read_tour(tour_filename)):
#     print p

print squash(elim(read_tour(tour_filename)))
