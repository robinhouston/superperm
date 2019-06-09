#!/usr/bin/python
# -*- encoding: utf8 -*-

"""
Construct universal cycles of permutations using the Eulerian path method.

B. Jackson, Universal cycles of k-subsets and k-permutations, Discrete Mathematics, 149 (1996) 123–129
"""

import itertools
import random
import sys

def shuffled(iterable):
	a = list(iterable)
	random.shuffle(a)
	return a

n = int(sys.argv[1])
k = int(sys.argv[2])

indices = range(n)
index_set = set(indices)
nodes = list(itertools.permutations(indices, k-1))
index_by_node = dict(( (n, i) for (i, n) in enumerate(nodes) ))
edges = [
	[
		index_by_node[node[1:] + (index,)]
		for index in shuffled(index_set.difference(node))
	]
	for node in nodes
]
num_edges = sum([ len(edges_from_node) for edges_from_node in edges ])

def find_cycle(index):
	global num_edges
	cycle = []
	while True:
		e = edges[index]
		if not e: return cycle
		index = e.pop()
		num_edges -= 1
		cycle.append(index)

cycle = [ 0 ]
while num_edges:
	for (i, index) in enumerate(cycle):
		e = edges[index]
		if e:
			cycle[i+1:i+1] = find_cycle(index)
			break

SYMBOLS = "123456789ABCDEFG"
loop = "".join([ SYMBOLS[nodes[i][-1]] for i in cycle[1:] ])
start = (loop + loop[:k-1]).index(SYMBOLS[:k])

print loop[start:] + loop[:start]
