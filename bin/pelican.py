import sys

peloton = eval(sys.stdin.read())
if isinstance(peloton[0], tuple):
	peloton = [ x[0] for x in peloton ]

def elements(peloton):
	p = peloton[0]
	yield p

	for q in peloton[1:]:
		while True:
			p2 = p[2:] + p[1] + p[0]
			if p2 == q:
				p = q
				print
				yield p
				break
			p = p[1:] + p[0]
			yield p

	for i in range(len(p) - 1):
		p = p[1:] + p[0]
		yield p

for p in elements(peloton):
	print "OneCycle(\"" + p + "6\"),"
