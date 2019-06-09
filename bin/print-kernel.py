#!/usr/bin/python
# -*- encoding: utf8 -*-

import sys

SYMBOLS = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

n = int(sys.argv[1]) - 1
kernel = sys.argv[2]

def parse_kernel_spec(spec):
	k = 0
	r = []
	while k < len(spec):
		i = int(spec[k])
		j = 2
		if k + 1 < len(spec) and spec[k + 1] == ' ':
			j = 3
			k += 2
		else:
			k += 1
		r.append((i, j))
	return r

class RepeatFound(Exception):
	def __init__(self, kernel):
		self.kernel = kernel

def make_kernel(n, parsed_spec):
	print "Score:", sum([ x[0] - (x[1] - 2) * (n-1) for x in parsed_spec ]) - (n-1) * len(parsed_spec)
	p = SYMBOLS[:n]
	kernel = [p]
	seen = set(kernel)
	for (pos, (i, j)) in enumerate(parsed_spec):
		for ii in range(i - 1):
			p = p[1:] + p[0]
			kernel.append(p)
			if p in seen: raise RepeatFound(kernel)
			seen.add(p)

		if pos < len(parsed_spec) - 1:
			p = p[j:] + "".join(reversed(p[:j]))
			kernel.append(p)
			if p in seen: raise RepeatFound(kernel)
			seen.add(p)

	return kernel

try:
	print make_kernel(n, parse_kernel_spec(kernel))
except RepeatFound, e:
	print >>sys.stderr, "Repeat found!", e.kernel
