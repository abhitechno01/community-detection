import networkx as nx
from matplotlib import pyplot as plt

graph = nx.Graph()
graph2 = nx.Graph()
GREEN = "#77DD77"
plt.figure(figsize=(22,22))

with open('p_n.txt', encoding='utf-8') as a_file:
	for line in a_file:
		vertex = line.split()
		graph.add_edge(int(vertex[0]),int(vertex[1]))

my_dict_degree = nx.betweenness_centrality(graph)
for key in sorted(list(my_dict_degree.keys())):
        print("{:<5}{:<6.4}".format(key,my_dict_degree[key]))

with open('edgelist_centrality_test.txt', encoding='utf-8') as b_file:
	for line in b_file:
		vertex = line.split()
		graph2.add_edge(vertex[0],vertex[1])
        
my_dict_bdegree = nx.degree_centrality(graph2)
for key in sorted(list(my_dict_bdegree.keys())):
        print("{:<10}{:<6.4}".format(key,my_dict_bdegree[key]))
        
nx.draw(graph,node_color=GREEN,with_labels=True)
