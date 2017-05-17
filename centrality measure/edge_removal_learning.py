from igraph import *
import networkx as nx
import xlwt
g = Graph().Read_Edgelist('p_n.txt', directed=False)
g.simplify()

#print g.get_adjacency()
#print g.get_adjlist()

gx = nx.read_edgelist('p_n.txt', nodetype=int)
n = gx.order()
vertex_list = [i for i in range(n)]

comm_id = g.community_edge_betweenness().as_clustering().membership
avg_degree = 0
avg_clustering_coefficient = 0
edge_list = gx.edges()
f1_list1 = []
f1_list2 = []
common_neighbours_count_list = list()
f2_list = []
f3_list1 = []
f3_list2 = []
deg_list = []
cid_list = []

f = open('p_n_const_community.txt', 'r')
c = []
for line in f:
    c.append(line.split())
l = len(c)
print c
cou, o, i, ii, iii = 0, 0, 0, 0, 0
for edge in gx.edges():
    print edge
    if((str(edge[0]) in c[0]) and (str(edge[1]) in c[0])):
        o += 1
        cid_list.append(0)
    elif((str(edge[0]) in c[1]) and (str(edge[1]) in c[1])):
        i += 1
        cid_list.append(1)
    elif((str(edge[0]) in c[2]) and (str(edge[1]) in c[2])):
        ii +=1
        cid_list.append(2)
    else:       #handles the edge that have end-point in different communities
        iii += 1
        cid_list.append(-1)

    cou += 1

print cou, o, i, ii, iii
print cid_list
print len(cid_list)
print g.ecount()
def avg_degree_clustering_coefficient():
    global avg_degree, avg_clustering_coefficient, deg_list
    deg_list = g.degree()
    total_degree = 0
    for i in deg_list:
        total_degree += i
    avg_degree = total_degree/n
    avg_clustering_coefficient = g.transitivity_avglocal_undirected()

def calculate_features():
    global f1_list1, f1_list2,f2_list, f3_list1, f3_list2, common_neighbours_count_list
    const_term = (n*(n-1)/2)*avg_clustering_coefficient
    edge_list = g.get_adjlist()
    for edge in gx.edges():
        neighbour1, neighbour2 = set(edge_list[edge[0]]), set(edge_list[edge[1]])
        common_neighbours = neighbour2.intersection(neighbour1)
        common_neighbours_count = len(common_neighbours)
        common_neighbours_count_list.append(common_neighbours_count)
        f1 = g.degree(edge[0])/avg_degree
        f1_list1.append(f1)
        f2 = g.degree(edge[1])/avg_degree
        f1_list2.append(f2)
        f3 = common_neighbours_count/const_term
        f2_list.append(f3)
        f3_temp1 = g.transitivity_local_undirected(vertices=edge[0])
        f3_temp2 = g.transitivity_local_undirected(vertices=edge[1])
        f3_list1.append(f3_temp1)
        f3_list2.append(f3_temp2)
    print gx.edges()
    print f1_list1
    print f1_list2
    print common_neighbours_count_list
    print f2_list
    print f3_list1
    print f3_list2


def write_excelsheet():
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Features')
    column_list = [
                    'Community ID',
                    'Edge',
                    'Degree(SID)',
                    'Degree(DID)',
                    'Common Nbrs Count',
                    'Common Nbrs Feature',
                    'Clstrng Co-efficient(SID)',
                    'Clstrng Co-efficient(DID)',
    ]
    for i in range(0,len(column_list)):
        ws.write(0, i, column_list[i])
    for i in range(0, g.ecount()):
        ws.write(i+1, 0, str(cid_list[i]))
        ws.write(i+1, 1, str(edge_list[i]))
        ws.write(i+1, 2, f1_list1[i])
        ws.write(i+1, 3, f1_list2[i])
        ws.write(i+1, 4, common_neighbours_count_list[i])
        ws.write(i+1, 5, f2_list[i])
        ws.write(i+1, 6, f3_list1[i])
        ws.write(i+1, 7, f3_list2[i])
    wb.save('features.xls')

avg_degree_clustering_coefficient()
calculate_features()
write_excelsheet()