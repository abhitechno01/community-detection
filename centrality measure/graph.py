from igraph import *
import networkx as nx
import xlwt


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



g=Graph.Read_Edgelist("p_n.txt")
#summary(g)
a=g.degree(mode="in" )
avg_degree=average_list(a)

gx = nx.read_edgelist('p_n.txt', nodetype=int)
edge_list = gx.edges()
#for edge in gx.edges():
#    print edge, type(edge)
#print len(gx.edges)
print type(edge_list[2])
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
#print(g)
wb=xlwt.Workbook()
ws=wb.add_sheet("Graph Details")
ws.write(0,0,"Vertices")
ws.write(0,1,"Degree")
ws.write(0,2,"Avg Degree")#normalized degree based on average degree of nodes
ws.write(0,3,"Eigen Vector")
ws.write(0,4,"Betweeness")
ws.write(0,5,"Closeness")
ws.write(0,6,"Page Rank")
ws.write(0,7,"Clustering Coeffecient")
ws.write(0,8,"Average Clustering Coeffecient")#normalized clustering coeffecient based on average local clustering coeffecient

for i in list(range(1,15)):
    ws.write(i, 0, i-1)
    ws.write(i, 1, a[i-1])
    ws.write(i,2,avg_nodes_degree[i-1])
    ws.write(i, 3, b[i-1])
    ws.write(i, 4, c[i-1])
    ws.write(i, 5, d[i-1])
    ws.write(i, 6, e[i-1])
    ws.write(i, 7, f[i-1])
    ws.write(i,8,cluster_nodes_average[i-1])

wb.save("try.xls")
