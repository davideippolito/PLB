#!/usr/bin/python3

import sys
import re
import math
import random
import copy

print(sys.argv)

i_net = sys.argv[1]
i_directed = sys.argv[2]
i_nof_subgraphs = int(sys.argv[3])
i_nof_nodes = int(sys.argv[4])
i_perc_edges = float(sys.argv[5])
i_o_prefix = sys.argv[6]

if i_directed == 'false':
    i_directed = False
else:
    i_directed = True

if i_perc_edges > 1.0:
    i_perc_edges = 1.0

if i_directed:
    if i_perc_edges <= 0.0:
        i_perc_edges = (i_nof_nodes - 1) / (i_nof_nodes * i_nof_nodes)
    i_nof_edges = math.ceil(i_perc_edges * (i_nof_nodes * i_nof_nodes))
    if i_nof_edges < (i_nof_nodes - 1):
        i_nof_edges = (i_nof_nodes - 1)
else:
    if i_perc_edges <= 0.0:
        i_perc_edges = (i_nof_nodes - 1) / ((i_nof_nodes * (i_nof_nodes - 1)) / 2)
    i_nof_edges = math.ceil(i_perc_edges * ((i_nof_nodes * (i_nof_nodes - 1)) / 2))
    if i_nof_edges < (i_nof_nodes - 1):
        i_nof_edges = (i_nof_nodes - 1)

print('input network', i_net)
print('is directed', i_directed)
print('number of subgraphs', i_nof_subgraphs)
print('number of subgraph nodes',i_nof_nodes)
print('percentage of subgraph edges', i_perc_edges)
print('required edges', i_nof_edges)
print('output prefix', i_o_prefix)



class graph_t:
    def __init__(self, name, nof_nodes):
        self.name = name
        self.node_labels = [None for i in range(nof_nodes)]
        self.edges = [ [False for i in range(nof_nodes)] for i in range(nof_nodes) ]
        self.edge_labels = [ [None for i in range(nof_nodes)] for i in range(nof_nodes) ]
    def set_node_label(self, node_i, label):
        self.node_labels[node_i] = label
    def get_node_label(self, node_i):
        return self.node_labels[node_i]
    def set_edge(self, source_i, target_i, label):
        self.edges[source_i][target_i] = True
        self.edge_labels[source_i][target_i] = label
    def get_edge(self, source_i, target_i):
        return self.edges[source_i][target_i], self.edge_labels[source_i][target_i]
    def get_edge_label(self, source_i, target_i):
        return self.edge_labels[source_i][target_i]
    def is_edge(self, source_i, target_i):
        return self.edges[source_i][target_i]
    def get_neighs(self, node_i):
        return [i for i in range(self.nof_nodes()) if self.edges[node_i][i] or self.edges[i][node_i]]
    def get_out_neighs(self, node_i):
        return [i for i in range(self.nof_nodes()) if self.edges[node_i][i]]
    def get_in_neighs(self, node_i):
        return [i for i in range(self.nof_nodes()) if self.edges[i][node_i]]
    def nof_nodes(self):
        return len(self.node_labels)
    def nof_edges(self):
        c = 0
        for v in self.edges:
            for i in v:
                if i:
                    c += 1
        return c
    def get_component_nodes(self, min_nodes):
        to_return = set()
        c_distr = dict()
        visited = set()
        nof_nodes = self.nof_nodes()
        while len(visited) != nof_nodes:
            c_comp = list()
            ci = 0
            for i in range(nof_nodes):
                if i not in visited:
                    c_comp.append(i)
                    #print('i',i)
                    break
            while ci < len(c_comp):
                for n in self.get_neighs(c_comp[ci]):
                    if n not in c_comp:
                        c_comp.append(n)
                ci += 1
            #print('|c_comp|',len(c_comp))
            c_distr[ len(c_comp) ] = c_distr.get(len(c_comp),0) + 1
            visited = visited | set(c_comp)
            if len(c_comp) >= min_nodes:
                to_return = to_return | set(c_comp)
            #print('|visited|', len(visited))
        #print('component length distribution')
        #for k,v in sorted(c_distr.items()):
        #    print(k,v)
        return to_return

def read_graph(ifile, is_directed):
    iff = open(ifile, 'r')
    name = iff.readline().strip()
    nof_nodes = int(iff.readline())
    g  = graph_t(name, nof_nodes)
    for i in range(nof_nodes):
        label = iff.readline().strip()
        g.set_node_label(i, label)
    nof_edges = int(iff.readline())
    p = re.compile('\s+')
    for i in range(nof_edges):
        cc = p.split(iff.readline().strip())
        label = None
        if len(cc) > 2:
            label = cc[2]
        g.set_edge(int(cc[0]), int(cc[1]), label)
        if not is_directed:
            g.set_edge(int(cc[1]), int(cc[0]), label)   
    return g

def write_graph(ofile, g):
    off = open(ofile, 'w')
    off.write(g.name.strip() + '\n')
    off.write(str(g.nof_nodes()) + '\n')
    for i in range(g.nof_nodes()):
        off.write(g.get_node_label(i).strip() + '\n')
    off.write(str(g.nof_edges()) + '\n')
    for i in range(g.nof_nodes()):
        for j in range(g.nof_nodes()):
            a,l = g.get_edge(i,j)
            if a:
                if l:
                    off.write(str(i) +' '+ str(j) +' '+ str(l) +'\n')
                else:
                    off.write(str(i) +' '+ str(j) + '\n')

def extract_subgraph(inet, available_nodes, name, nof_nodes, nof_edges, is_directed):
    """
    It works on directed graphs, and extract directed subgraphs
    """
    #s_nodes = [ random.randint(0, inet.nof_nodes() - 1) ]
    s_nodes = [   available_nodes[  random.randint(0, len(available_nodes) - 1)   ]   ]
    s_neighs = inet.get_neighs(s_nodes[0])
    
    # extract adjacent nodes
    #print(s_nodes, s_neighs)
    for i in range(nof_nodes - 1):
        #print(i, nof_nodes)
        if len(s_neighs) == 0:
            return None, None
        a = random.choice(s_neighs)
        s_nodes.append(a)
        s_neighs.remove(a)
        for n in inet.get_neighs(a):
            if (n not in s_nodes) and (n not in s_neighs):
                s_neighs.append(n)
        #print(s_nodes, s_neighs)
        
    #print(s_nodes)
    s_edges = set()
    # create a connected subgraph
    for i in range(len(s_nodes) - 1):
        p = random.choice(list(set(inet.get_neighs(s_nodes[i])) & (set(s_nodes) - {s_nodes[i]} )))
        if is_directed:
            if inet.is_edge(s_nodes[i],p):
                s_edges.add( (s_nodes[i],p) )
            else:
                s_edges.add( (p,s_nodes[i]) )
        else:
            s_edges.add( (s_nodes[i],p) )
            s_edges.add( (p,s_nodes[i]) )
    #print(s_edges)
    
    # extract other edges
    s_neighs = list()
    s_nodes = sorted(s_nodes)
    for i in range(len(s_nodes) - 1):
        for j in range(i + 1, len(s_nodes) - 1):
            if inet.is_edge(s_nodes[i], s_nodes[j]) and (s_nodes[i],s_nodes[j]) not in s_edges:
                s_neighs.append( (s_nodes[i],s_nodes[j]) )
            if inet.is_edge(s_nodes[j],s_nodes[i]) and (s_nodes[j],s_nodes[i]) not in s_edges:
                s_neighs.append( (s_nodes[j],s_nodes[i]) )
    #print(s_neighs)
    
    #print('edges to choose', nof_edges - len(s_edges), nof_edges, len(s_edges))
    to = nof_edges - len(s_edges)
    if to < 0:
        to = 0
    #for i in range( nof_edges - len(s_edges)  ):
    for i in range( to ):
        if len(s_neighs) == 0:
            break
        e = random.choice(s_neighs)
        s_edges.add(e)
        s_neighs.remove(e)
        
        if not is_directed:
            s_edges.add( (e[1],e[0]) )
            s_neighs.remove( (e[1],e[0]) )
        
    # create the new graph
    random.shuffle(s_nodes)
    #print('chosen nodes', s_nodes)
    nmap = { s_nodes[i] : i for i in range(len(s_nodes))  }
    #print('nmap', nmap)
    
    subnet = graph_t(name, len(s_nodes))
    for i in range(len(s_nodes)):
        subnet.set_node_label(i,  inet.get_node_label(s_nodes[i]))
    for e in s_edges:
        #print('mapping edge', e)
        subnet.set_edge(  nmap[e[0]], nmap[e[1]], inet.get_edge_label(s_nodes[i], s_nodes[j]) )
    #print(len(s_edges))
    return subnet, s_nodes






inet = read_graph(i_net, i_directed)

av_nodes = list(inet.get_component_nodes(i_nof_nodes))
if len(av_nodes) < i_nof_nodes:
    print('there is not a connect component big enought', len(av_nodes))
    quit()

e_distr = dict()

for i in range(i_nof_subgraphs):
    
    min_edges = i_nof_nodes - 1
    c_edges = random.randint(min_edges, i_nof_edges)
    
    #sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, i_nof_edges, i_directed)
    sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, c_edges, i_directed)
    while sg == None:
        sg, nmap = extract_subgraph(inet, av_nodes, inet.name +'_sub_'+ str(i), i_nof_nodes, c_edges, i_directed)  
    e_distr[sg.nof_edges()] = e_distr.get(sg.nof_edges(), 0) + 1
    # print(sg.name)
    # print(sg.nof_nodes(), sg.nof_edges())
    # print(nmap)
    write_graph(i_o_prefix + '_sub_'+str(i)+'.gfd', sg)
    
for k,v in sorted(e_distr.items()):
    print(k,v)