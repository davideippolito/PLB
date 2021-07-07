#!/usr/bin/python3

import sys
import random

nof_nodes = int(sys.argv[1])
edge_perc = float(sys.argv[2])
nof_labels = int(sys.argv[3])
o_file = sys.argv[4]


if nof_labels > 25:
	print('max number of allowed labels is 25')
	nof_labels = 25

max_edges = nof_nodes * nof_nodes
min_edges = nof_nodes - 1
nof_edges = int(max_edges * edge_perc)

if nof_edges < min_edges:
	print('minimum number of edges',min_edges)
	nof_edges = min_edges

print('generating graph with',nof_nodes,'nodes, ',nof_edges,'/',max_edges,', and ',nof_labels,'labels')

labels = ['A' for i in range(nof_nodes)]
for i in range(nof_nodes):
	labels[i] = chr(ord('A') + random.randint(0, nof_labels - 1))


edges = set()
for i in range(nof_nodes):
	n = random.randint(0,nof_nodes - 1)
	while n == i:
		n = random.randint(0,nof_nodes - 1)
	edges.add((i,n))

for i in range(nof_edges - len(edges)):
	a = random.randint(0,nof_nodes - 1)
	b = random.randint(0,nof_nodes - 1)
	while (a,b) in edges:
		a = random.randint(0,nof_nodes - 1)
		b = random.randint(0,nof_nodes - 1)
	edges.add( (a,b) )

with open(o_file,'w') as of:
	of.write('#mygraph\n')
	of.write(str(nof_nodes) +'\n')
	for i in range(nof_nodes):
		of.write(labels[i]+'\n')
	of.write(str(nof_edges)+'\n')
	for e in sorted(edges):
		of.write(str(e[0])+' '+str(e[1])+'\n')
