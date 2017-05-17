import networkx as nx
import csv
filename = raw_input('Input filename... ')
gx = nx.read_edgelist(filename+'.txt',nodetype=int)
n = gx.order()
writer = csv.writer(open(filename+"_edge_betweenness_and_ECC.csv", "wb"))
edgeBetweenness = nx.edge_betweenness_centrality(gx, normalized=True, weight=None)
for eh in gx.edges():
	for i in range(len(edgeBetweenness)):
		if(eh == (edgeBetweenness.keys())[i]):
			#print eh[0],eh[1],": "
			actual_triangles = len(set(gx.neighbors(eh[0])) & set(gx.neighbors(eh[1])))
			print"No. of actual triangles: ",actual_triangles
				
			no_possible_triangles = min(gx.degree(eh[0]) - 1, gx.degree(eh[1]) - 1)
			print"No. of possible triangles: ",no_possible_triangles
				
			ecc = float(actual_triangles)/no_possible_triangles
			print"Edge Clustering Coefficient of",eh[0],eh[1],": ",ecc
			print"\n"
			writer.writerow([eh, (edgeBetweenness.values())[i], ecc])
			