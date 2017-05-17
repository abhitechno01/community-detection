from igraph import *
import csv
filename = 'simple_network ScaleFreeCDA'
g = Graph().Read_Edgelist(filename+'.txt', directed=False)
#g = Graph().Read_GML(filename+'.gml')
g.simplify()
vertex_count = g.vcount()
#gx = nx.read_edgelist(filename++'.txt', nodetype=int)
#n = gx.order()
#vertex_list = [i for i in range(n)]

def average_list(m):
    s=0
    for i in range(len(m)):
       s=s+m[i]
    return s/len(m)

def normalize(m,n):
    j=[]
    for i in range(len(m)):
      j.append(m[i]/n)
    return j

a=g.degree()
avg_degree=average_list(a)
avg_nodes_degree=normalize(a,avg_degree)
b=g.evcent(directed="False")
c=g.betweenness(directed="False")
d=g.closeness()
e=g.pagerank(directed="False")
f=g.transitivity_local_undirected()
avg_cluster=average_list(f)

cluster_nodes_average=normalize(f,avg_cluster)

print(a)#degree
print(b)#eigen vector
print(c)#betweenness
print(d)#closeness
print(e)#pagerank
print(f)#clustering coeffecient local
file_to_save = filename#raw_input('Filename to save in as... ')
writer = csv.writer(open(file_to_save + '_structural_property.csv', 'wb'))
writer.writerow(['Node', 'Vertex Degree', 'Eigen Vector Centrality',
                 'Vertex Betweenness', 'Closeness Centrality', 'Pagerank', 'Local Clustering Co-efficient'
                 ])
for i in range(vertex_count):
    writer.writerow([i, a[i], b[i], c[i], d[i], e[i], f[i]])
