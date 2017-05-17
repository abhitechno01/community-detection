from igraph import *
g = Graph().Read_Edgelist('p_n.txt', directed=False)
g.simplify()
vertex_count = g.vcount()
edge_list = g.get_edgelist()
#print edge_list, type(edge_list), type(edge_list[5])

def fill(y, comm):
    for x in range(vertex_count):
        mat_membership[x][y] = comm[x]

number_of_cda = 6
mat_membership = [[-1 for x in range(number_of_cda)] for y in range(vertex_count)]
fill(0, g.community_multilevel().membership)
fill(1, g.community_label_propagation().membership)
fill(2, g.community_infomap().membership)
fill(3, g.community_walktrap().as_clustering().membership)
fill(4, g.community_fastgreedy().as_clustering().membership)
fill(5, g.community_edge_betweenness().as_clustering().membership)

#for i in range(vertex_count):
#    print mat_membership[i]

duplicates = []
result = dict()
for i in range(vertex_count):
    temp_match = [i]
    if i in duplicates:
        continue
    for j in range(i+1,vertex_count):
        if cmp(mat_membership[i], mat_membership[j])==0:
            temp_match.append(j)
            duplicates.append(j)
    if len(temp_match)>1:
        result[i] = temp_match

number_of_comm = len(result)
print('Constant Communities :')
for i in range(number_of_comm):
    print result[i]