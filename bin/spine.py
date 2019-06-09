#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Extract the spine of a superpermutation
"""

import sys

if len(sys.argv) > 1:
	s = sys.argv[1]
else:
	s = sys.stdin.read()

s = s.strip()

symbols = set(s)
n = len(symbols)
sorted_perm = sorted(symbols)

if len(set(s[:n])) != n:
	print >>sys.stderr, "The first %d symbols (%s) are not distinct" % (n, s[:n])
	sys.exit(1)

if s[:n] != "".join(sorted_perm):
	print >>sys.stderr, "The first %d symbols (%s) are not in order" % (n, s[:n])
	sys.exit(1)

wait_for = None
printing = True
for i in range(len(s) - n + 1):
	p = superperm[i : i + n]
	if sorted(p) == sorted_perm:
		if printing:
			print p
		gap = 0
	else:
		gap += 1
