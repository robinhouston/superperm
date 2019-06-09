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

def ones_and_twos(n):
	num_one_cycles = math.factorial(n-1)
	min_interesting_score = 5 # (n-1) * 2
	# max_path_len = 25

	def search(p, score=0, one_cycles=set(), path=[]):
		if score + num_one_cycles - len(one_cycles) < min_interesting_score:
			return

		# if len(path) > max_path_len: return

		if score > search.best_score:
			search.best_score = score
			print >>sys.stderr, "New best score:", search.best_score
		if score >= min_interesting_score: # and score % (n-1) == 0:
			print str(score) + ": " + "".join([
				str(i+1) + (" " if j > 2 else "")
				for (i, j) in path
			])

		c = cyclerep(p)
		if c in one_cycles: return
		one_cycles.add(c)

		for i in range(n-1, -1, -1):
			q = p[i:] + p[:i]
			for j in (2,):
				r = q[j:] + q[:j][::-1]

				path.append((i, j))
				search(r, score + i - (n-2) - (j-2) * (n-1))
				path.pop()

		one_cycles.remove(c)

	search.best_score = 0
	search(SYMBOLS[:n])

n = int(sys.argv[1])
ones_and_twos(n)
