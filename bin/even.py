#!/usr/bin/python
# -*- encoding: utf-8 -*-

from itertools import permutations
import sys

SYMBOLS = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

sympos = dict(( (s,i) for (i, s) in enumerate(SYMBOLS) ))

def cycles(perm):
    ii = set(range(len(perm)))
    cycles = []
    while ii:
        i = j = ii.pop()
        cycle = SYMBOLS[i]
        while True:
            j = sympos[perm[j]]
            if j == i: break
            cycle += SYMBOLS[j]
            ii.remove(j)
        cycles.append(cycle)
    return cycles

def parity(perm):
    return sum([
        1 - len(cycle)%2
        for cycle in cycles(perm)
    ]) % 2

n = int(sys.argv[1])
for p in permutations(SYMBOLS[:n]):
    p = "".join(p)
    if parity(p) == 0:
        print p
