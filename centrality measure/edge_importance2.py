from igraph import *
import csv


def run_const_comm(g):
    vertex_count = g.vcount()
    g.simplify()
    def fill(y, comm):
        for x in range(vertex_count):
            mat_membership[x][y] = comm[x]

    number_of_cda = 5
    mat_membership = [[-1 for x in range(number_of_cda)] for y in range(vertex_count)]
    fill(0, g.community_multilevel().membership)
    fill(1, g.community_label_propagation().membership)
    fill(2, g.community_infomap().membership)
    fill(3, g.community_walktrap().as_clustering().membership)
    fill(4, g.community_fastgreedy().as_clustering().membership)
    #fill(5, g.community_edge_betweenness().as_clustering().membership)

    duplicates = []
    result = dict()
    counter = 0
    for i in range(vertex_count):
        temp_match = [i]
        if i in duplicates:
            continue
        for j in range(i + 1, vertex_count):
            if cmp(mat_membership[i], mat_membership[j]) == 0:
                temp_match.append(j)
                duplicates.append(j)
        if len(temp_match) > 1:
            result[counter] = temp_match
            counter += 1
    return result


def edge_clustering_co(g):
    edge_list = g.get_edgelist()
    ecc_list = []
    for edge in edge_list:
        neighbors_v1 = set(g.neighbors(edge[0]))
        neighbors_v2 = set(g.neighbors(edge[1]))
        comm_neighbors_len = len(neighbors_v1.intersection(neighbors_v2))
        deg_v1, deg_v2 = g.degree(edge[0]) - 1, g.degree(edge[1]) - 1
        min_deg_v1v2 = min(deg_v1, deg_v2)
        edge_co_value = float(comm_neighbors_len) / min_deg_v1v2
        ecc_list.append(edge_co_value)
        print "Edge :   ", str(edge[0]), '-', str(edge[1])
        print "Number of triangles  :   ", comm_neighbors_len
        print "Total number of poosible triangle    :   ", min_deg_v1v2
        print "Edge Clustering Co-effiecient    :   ", edge_co_value, "\n"
    return ecc_list


def write_csv(normalized, file_to_save):
    global edge_list, vertex_count, edge_count, eb_list, ecc_list
    CONSTANT = 1
    if normalized:
        CONSTANT = float(2) / (vertex_count * (vertex_count - 1))
    # file_to_save = raw_input("Input filename to save... ")
    writer = csv.writer(open(file_to_save + '_EB_ECC.csv', 'wb'))
    writer.writerow(['Edge', 'Edge Betweenness', 'Edge Clustering Coefficient'])
    for i in range(edge_count):
        writer.writerow([edge_list[i], CONSTANT * eb_list[i], ecc_list[i]])


def index_of_duplicates(listname, item):
    index_loc = []
    start_pos = -1
    item_count = listname.count(item)
    for i in range(item_count):
        index = listname.index(item, start_pos + 1)
        index_loc.append(index)
        start_pos = index
    return index_loc


def imp_edge(g, check_edge_list):
    '''
    Returns Edge ID of important edge.
    Important edge is one with high eb and low ecc value
    '''

    list((set(eb_list).difference(set(check_edge_list))))
    edge_list = g.get_edgelist()
    eb_list = g.edge_betweenness()
    ecc_list = edge_clustering_co(g)
    max_eb = max(list(set(eb_list).difference(set(check_edge_list))))
    min_ecc = min(list(set(ecc_list).difference(set(check_edge_list))))
    common_edge_list = index_of_duplicates(eb_list, max_eb) and index_of_duplicates(ecc_list, min_ecc)
    if len(common_edge_list) > 0:
        return common_edge_list[0]
    else:
        if ecc_list[index_of_duplicates(eb_list, max_eb)[0]] == 1:
            check_edge_list.append(index_of_duplicates(eb_list, max_eb)[0])
            max_eb = max(list(set(eb_list).difference(set(check_edge_list))))
            min_ecc = min(list(set(ecc_list).difference(set(check_edge_list))))
            common_edge_list = index_of_duplicates(eb_list, max_eb) and index_of_duplicates(ecc_list, min_ecc)
            return common_edge_list[0]

        else:
            edge_with_max_eb_index = eb_list.index(max_eb)
            edge_with_min_ecc_index = ecc_list.index(min_ecc)
            ebmax_edge_ecc = ecc_list[edge_with_max_eb_index]
            delta_ecc = ebmax_edge_ecc - min_ecc
            if delta_ecc <= 0.2:
                return edge_with_max_eb_index
            else:
                return edge_with_min_ecc_index


def splitting_factor_and_community_check(g, outer, inner):
    print 'Outer Deleted Edge:  ', outer
    print 'Inner Deleted Edge:  ', inner
    global writer, no_of_orig_comm
    comm_list_after_edge_del = run_const_comm(g)
    no_of_comm = len(comm_list_after_edge_del)
    print no_of_comm, no_of_orig_comm
    flag1 = False
    if no_of_comm == no_of_orig_comm:
        for i in range(no_of_comm):
            sublist1_len = len(original_comm[i])
            sublist2_len = len(comm_list_after_edge_del[i])
            if sublist1_len == sublist2_len:
                sort_sublist2 = sorted(comm_list_after_edge_del[i])
                for j in range(sublist1_len):
                    if original_comm[i][j] != sort_sublist2[j]:
                        flag1 = True
                        print 'Length comparison: Uneven   '
    if (no_of_comm != no_of_orig_comm) or flag1:
        splitting_factor = abs(no_of_orig_comm - no_of_comm)
        print 'Splitting Factor(abs(before breakage-after breakage)):   ', splitting_factor
        print 'Uneven Communities\n', 'Communities after edge deletion: '
        for i in range(no_of_comm):
            print comm_list_after_edge_del[i]
            writer.writerow([outer, inner, comm_list_after_edge_del[i], splitting_factor])
        print '\n'


if __name__ == '__main__':
    filename = 'p_n'  # raw_input("Input Edge-list filename... ")
    g = Graph().Read_Edgelist(filename + '.txt', directed=False)
    g.simplify()

    vertex_count_outer = g.vcount()
    edge_count_outer = g.ecount()
    edge_list_outer = g.get_edgelist()
    eb_list_outer = g.edge_betweenness()
    ecc_list_outer = []
    check_edge_list_outer = []

    filename_constant_comm = 'p_n_const_community'  # raw_input("Input constant community file...    ")
    f = open(filename_constant_comm + '.txt', 'r')
    original_comm1 = []
    for line in f:
        original_comm1.append(line.split())
    f.close()
    original_comm = []
    for line in original_comm1:
        a = []
        for i in line:
            a.append(int(i))
        original_comm.append(a)
    no_of_orig_comm = len(original_comm)
    ecc_list_outer = edge_clustering_co()

    # write_csv(True) #fix scalablity if number of files increases
    print ecc_list_outer
    file_to_save = 'toyNetwork'  #raw_input('Input filename to save... ')
    writer = csv.writer(open(file_to_save + '_SF_COMMUNITIES.csv', 'wb'))
    writer.writerow(['Outer-Edge', 'Inner-Edge', 'Splitting Factor', 'Communities After Breakage'])

    while (max(list(set(ecc_list_outer).difference(set(check_edge_list_outer)))) != 1):
        print 'outer loop'
        edge_list_outer = g.get_edgelist()
        edge_to_del_outer = imp_edge(g, check_edge_list_outer)
        edge_name_outer = edge_list[edge_to_del_outer]
        g.delete_edges([edge_to_del_outer])
        print 'Edge Deleted:    ',str(edge_name_outer)
        check_edge_list_outer.append(edge_name_outer)
        splitting_factor_and_community_check(g, outer=str(edge_name_outer), inner=0)
        ecc_list_inner = edge_clustering_co(g)
        print ecc_list_inner
        check_edge_list_inner = list()
        while (max(list(set(ecc_list_inner).difference(set(check_edge_list_inner)))) != 1):
            print 'inner loop'
            edge_list_inner = g.get_edgelist()
            edge_to_del_inner = imp_edge(g, check_edge_list_inner)
            edge_name_inner = edge_list_inner[edge_to_del_inner]
            g.delete_edges([edge_to_del_inner])
            print 'Edge Deleted:    ',str(edge_name_inner)
            check_edge_list_inner.append(edge_name_outer)
            splitting_factor_and_community_check(g, outer=str(edge_name_outer), inner=str(edge_name_inner))
            ecc_list_inner = edge_clustering_co(g)
            print ecc_list_inner



