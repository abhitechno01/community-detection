from igraph import *
import networkx as nx

g = Graph().Read_Edgelist('edgelist_edgebetweenness.txt', directed = False)
for e in g.es:
    print(e.tuple)
f = g.edge_betweenness()
print(type(f))
print(f)

g1 = nx.read_edgelist('edgelist_edgebetweenness.txt')
f1 = nx.edge_betweenness_centrality(g1, normalized=True)
print(type(f1))
print(f1)

g2 = nx.read_edgelist('tryedgelist.txt')
f2 = nx.edge_betweenness_centrality(g2, normalized=True)
print(type(f2))
print(f2)

