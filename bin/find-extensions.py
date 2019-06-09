#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import math
import sys

SYMBOLS = "123456789ABCDEFG"

def rotate(w, x):
	"""
	Rotate the word w so it starts with the symbol x.
	"""
	i = w.index(x)
	return w[i:] + w[:i]

def cyclerep(w):
	"""
	The canonical representative of the cyclic equivalence class of w,
	assuming w has no repeated symbols.
	"""
	return rotate(w, min(w))

def distance(a, b):
	for i in range(len(b), 0, -1):
		if a[-i:] == b[:i]:
			return len(b) - i
	return len(b)

def find_extensions(n):
	num_one_cycles = math.factorial(n-1)
	min_interesting_score = 0
	max_path_len = 10

	def search(p, score=0, before_jump=None, one_cycles=set(), path=[]):
		if score + num_one_cycles - len(one_cycles) < min_interesting_score:
			return

		# print "search", p, score, path
		if len(path) > max_path_len: return

		c = cyclerep(p)
		if c in one_cycles:
			return

		one_cycles.add(c)

		if before_jump and path:
			loop_score = score - (n-1) * (distance(before_jump, SYMBOLS[:n]) - 1) - 1
			if loop_score >= min_interesting_score:
				print str(loop_score) + ": " + "".join([
					str(i+1) + (" " if j > 2 else "")
					for (i, j) in path
				])

		for i in range(n-1, -1, -1):
			q = p[i:] + p[:i]
			for j in (2,3):
				r = q[j:] + q[:j][::-1]

				path.append((i, j))
				search(r, score + i - (n-2) - (j-2) * (n-1), q)
				path.pop()

		one_cycles.remove(c)

	search(SYMBOLS[:n])

n = int(sys.argv[1])
find_extensions(n-1)
