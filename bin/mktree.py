#!/usr/bin/python
# -*- encoding: utf8 -*-

"""
Greedy search for a tree of 2-cycles
"""

from math import factorial
import sys

SYMBOLS = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def cyclerep(c):
	m = min(c)
	i = c.index(m)
	return c[i:] + c[:i]

def rmchar(char, s):
	i = s.index(char)
	return s[:i] + s[i+1:]

def neighbours((c, p), include_double_overlaps=False):
	for i in range(len(p)):
		d = p[:i] + p[i+1:]
		for j in range(len(p) - 1):
			if include_double_overlaps or i != j:
				yield (p[i], cyclerep(d[:j] + c + d[j:]))

def overlaps((c, p), (d, q)):
	if c == d: return p == q
	return cyclerep(rmchar(c, q)) == cyclerep(rmchar(d, p))

n = int(sys.argv[1])
l = (n-1) * factorial(n-3) - 1
s = SYMBOLS[:n]


def okay(d, c, cycles):
	nbs = neighbours(d, True)
	for e in cycles:
		if e != c and overlaps(d, e):
			return False
	return True

def search(cycles):
	print >>sys.stderr, "\r" + str(len(cycles)) + "    ",

	if len(cycles) == l:
		return cycles

	for c in cycles:
		for d in neighbours(c):
			if okay(d, c, cycles):
				r = search(cycles + [d])
				if r is not None:
					return r

	return None

print search([
	(s[-1], s[:i] + s[-2] + s[i:-2])
	for i in range(1, n-1)
])
