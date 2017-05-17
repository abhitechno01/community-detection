from igraph import *
import xlwt

'''
filename = raw_input('Input filename containing adjacency list:  ')
g = Graph().Read_Edgelist(filename, directed = False)
'''

g = Graph().Read_Edgelist('football_network.txt', directed = False)
g.simplify()

vertex_count = g.vcount()
edge_count = g.ecount()
edge_list = g.get_edgelist()

f = open('.txt', 'r')
original_comm1 = []
for line in f:
    original_comm1.append(line.split())

original_comm = []
for line in original_comm1:
    a = []
    for i in line:
        a.append(int(i))
    original_comm.append(a)

no_of_orig_comm = len(original_comm)

def run_const_comm():
    global g
    g.simplify()
    vertex_count_changed = g.vcount()

    def fill(y, comm):
        for x in range(vertex_count_changed):
            mat_membership[x][y] = comm[x]

    number_of_cda = 5
    mat_membership = [[-1 for x in range(number_of_cda)] for y in range(vertex_count_changed)]
    fill(0, g.community_multilevel().membership)
    fill(1, g.community_label_propagation().membership)
    fill(2, g.community_infomap().membership)
    fill(3, g.community_walktrap().as_clustering().membership)
    fill(4, g.community_fastgreedy().as_clustering().membership)
    #fill(5, g.community_edge_betweenness().as_clustering().membership)

    duplicates = []
    result = dict()
    counter = 0
    for i in range(vertex_count_changed):
        temp_match = [i]
        if i in duplicates:
            continue
        for j in range(i+1,vertex_count):
            if cmp(mat_membership[i], mat_membership[j])==0:
                temp_match.append(j)
                duplicates.append(j)
        if len(temp_match)>1:
            result[counter] = temp_match
            counter += 1

    '''
    number_of_comm = len(result)
    print number_of_comm
    print('Constant Communities :')
    for i in range(number_of_comm):
        print result[i]
    #'''

    return result

def save_measures(filen):
    global g
    g.simplify()
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

    a=g.degree(mode="in" )
    avg_degree=average_list(a)
    avg_nodes_degree=normalize(a,avg_degree)
    b=g.evcent(directed="False")
    c=g.betweenness(directed="False")
    d=g.closeness()
    e=g.pagerank(directed="False")
    f=g.transitivity_local_undirected()
    avg_cluster=average_list(f)

    cluster_nodes_average=normalize(f,avg_cluster)

    '''
    print(a)#degree
    print(b)#eigen vector
    print(c)#betweenness
    print(d)#closeness
    print(e)#pagerank
    print(f)#clustering coefficient local
    '''
    wb=xlwt.Workbook()
    ws=wb.add_sheet("Graph Details")
    ws.write(0,0,"Vertices")
    ws.write(0,1,"Degree")
    ws.write(0,2,"Avg Degree")#normalized degree based on average degree of nodes
    ws.write(0,3,"Eigen Vector")
    ws.write(0,4,"Betweeness")
    ws.write(0,5,"Closeness")
    ws.write(0,6,"Page Rank")
    ws.write(0,7,"Clustering Coefficient")
    ws.write(0,8,"Average Clustering Coefficient")#normalized clustering coefficient based on average local clustering coefficient

    for i in list(range(1,vertex_count+1)):
        ws.write(i, 0, i-1)
        ws.write(i, 1, a[i-1])
        ws.write(i,2,avg_nodes_degree[i-1])
        ws.write(i, 3, b[i-1])
        ws.write(i, 4, c[i-1])
        ws.write(i, 5, d[i-1])
        ws.write(i, 6, e[i-1])
        ws.write(i, 7, f[i-1])
        ws.write(i,8,cluster_nodes_average[i-1])

    filename = filen+'.xls'
    wb.save(filename)

checked_edges = set()

for i in range(edge_count):
    print 'Counter', i
    edge_betweenness_list = g.edge_betweenness()
    print edge_betweenness_list
    edge_betweenness_list_sorted = sorted(edge_betweenness_list)
    edge_to_remove = edge_list[edge_betweenness_list.index(edge_betweenness_list_sorted[i])]
    '''
    index_max_element = edge_betweenness_list.index(max(edge_betweenness_list))
    edge_to_remove = edge_list[index_max_element]
    print edge_list
    checked_edges.add(edge_to_remove)
    if edge_to_remove in checked_edges:
        len_checked_edges = len(checked_edges)
        find_index = edge_betweenness_list_sorted[len_checked_edges]
        edge_to_remove = edge_list[edge_betweenness_list.index(find_index)]
        checked_edges.add(edge_to_remove)
    '''

    flag = False
    for communities in original_comm:
        if edge_to_remove[0] in communities and edge_to_remove[1] in communities:
            g.delete_edges([edge_to_remove])
            flag = True
            print 'Deleted Edge    ', str(edge_to_remove)
    if flag:
        comm_list_after_edge_del = run_const_comm()
        no_of_comm = len(comm_list_after_edge_del)
        print no_of_comm, no_of_orig_comm
        flag1= False
        if no_of_comm == no_of_orig_comm:
            #'''
            for i in range(no_of_comm):
                sublist1_len = len(original_comm[i])
                sublist2_len = len(comm_list_after_edge_del[i])
                if sublist1_len == sublist2_len:
                    sort_sublist2 = sorted(comm_list_after_edge_del[i])
                    for j in range(sublist1_len):
                        if original_comm[i][j] != sort_sublist2[j]:
                            flag1 = True
                            print 'Length comparison: Uneven   '

            #'''

            '''
            for i in range(no_of_orig_comm):
                if cmp(original_comm[i], sorted(comm_list_after_edge_del[i])) != 0:
                    flag1 = True
                    print 'length comparison    '
            '''


        if (no_of_comm != no_of_orig_comm) or flag1:
            print 'Uneven Communities\n', 'Communities after edge deletion: '
            for i in range(no_of_comm):
                print comm_list_after_edge_del[i]
            save_measures(str(edge_to_remove))
        g.add_edges([edge_to_remove])