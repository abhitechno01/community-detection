import networkx as nx
from igraph import *
import community


filename = 'p_n'  # raw_input("Input Edge-list filename... ")
g = Graph().Read_Edgelist(filename + '.txt', directed=False)
g.simplify()
print len(g.clusters())
gx = nx.read_edgelist('p_n.txt', nodetype=int)
gx.remove_edges_from(gx.selfloop_edges())
n = gx.order()

#G = nx.path_graph(10)
#comp = community.girvan_newman(G)
#result = tuple(sorted(c) for c in next(comp))
#print result

print n, nx.number_connected_components(gx), tuple(nx.connected_components(gx))#, nx.girvan_newman(gx)