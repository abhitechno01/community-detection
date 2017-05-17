from igraph import *
import csv


def run_const_comm():
    global g, vertex_count
    g.simplify()
    #vertex_count_changed = g.vcount()

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
        for j in range(i+1,vertex_count):
            if cmp(mat_membership[i], mat_membership[j])==0:
                temp_match.append(j)
                duplicates.append(j)
        if len(temp_match)>1:
            result[counter] = temp_match
            counter += 1
    return result

def edge_clustering_co():
    global edge_list, edge_clustering_co_list
    for edge in edge_list:
        neighbors_v1 = set(g.neighbors(edge[0]))
        neighbors_v2 = set(g.neighbors(edge[1]))
        comm_neighbors_len = len(neighbors_v1.intersection(neighbors_v2))
        deg_v1, deg_v2 = g.degree(edge[0])-1, g.degree(edge[1])-1
        min_deg_v1v2 = min(deg_v1, deg_v2)
        edge_co_value = float(comm_neighbors_len)/min_deg_v1v2
        edge_clustering_co_list.append(edge_co_value)
        print "Edge :   ", str(edge[0]), '-', str(edge[1])
        print "Number of triangles  :   ", comm_neighbors_len
        print "Total number of poosible triangle    :   ", min_deg_v1v2
        print "Edge Clustering Co-effiecient    :   ", edge_co_value, "\n"
    return edge_clustering_co_list


def write_csv(normalized, file_to_save):
    global edge_list, vertex_count, edge_count, edge_betweenness_list, edge_clustering_co_list
    CONSTANT = 1
    if normalized:
        CONSTANT = float(2)/(vertex_count*(vertex_count-1))
    #file_to_save = raw_input("Input filename to save... ")
    writer = csv.writer(open(file_to_save+'_EB_ECC.csv', 'wb'))
    writer.writerow(['Edge', 'Edge Betweenness', 'Edge Clustering Coefficient'])
    for i in range(edge_count):
        writer.writerow([edge_list[i], CONSTANT*edge_betweenness_list[i], edge_clustering_co_list[i]])

def index_of_duplicates(listname, item):
    index_loc = []
    start_pos = -1
    item_count = listname.count(item)
    for i in range(item_count):
        index = listname.index(item, start_pos+1)
        index_loc.append(index)
        start_pos = index
    return index_loc

def splitting_factor_and_community_check(outer, inner):
    print 'Outer Deleted Edge:  ', outer
    print 'Inner Deleted Edge:  ', inner
    global writer, no_of_orig_comm
    comm_list_after_edge_del = run_const_comm()
    no_of_comm = len(comm_list_after_edge_del)
    print no_of_comm, no_of_orig_comm
    flag1= False
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
            splitting_factor = abs(no_of_orig_comm-no_of_comm)
            print 'Splitting Factor(abs(before breakage-after breakage)):   ', splitting_factor
            print 'Uneven Communities\n', 'Communities after edge deletion: '
            for i in range(no_of_comm):
                print comm_list_after_edge_del[i]
                writer.writerow([outer, inner, comm_list_after_edge_del[i], splitting_factor])
            print '\n'




if __name__ == '__main__':
    filename = 'p_n'#raw_input("Input Edge-list filename... ")
    g = Graph().Read_Edgelist(filename+'.txt', directed = False)
    g.simplify()

    vertex_count = g.vcount()
    edge_count = g.ecount()
    edge_list = g.get_edgelist()
    edge_betweenness_list = g.edge_betweenness()
    edge_clustering_co_list = []

    filename_constant_comm = 'p_n_const_community'#raw_input("Input constant community file...    ")
    f = open(filename_constant_comm+'.txt', 'r')
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

    edge_clustering_co_list = edge_clustering_co()
    #write_csv(True) #fix scalablity if number of files increases
    print edge_clustering_co_list
    threshold_ecc_outer = max(edge_clustering_co_list)

    print threshold_ecc_outer
    file_to_save = 'toyNetwork'#raw_input('Input filename to save... ')
    writer = csv.writer(open(file_to_save+'_SF_COMMUNITIES.csv', 'wb'))
    writer.writerow(['Outer-Edge', 'Inner-Edge', 'Splitting Factor', 'Communities After Breakage'])

    while(threshold_ecc_outer > 0.7):
        print 'in while clause of threshold_ecc_couter'
        outer_loop_del_edge_list = []
        max_eb = max(edge_betweenness_list)
        count_of_max_eb = edge_betweenness_list.count(max_eb)
        min_ecc = min(edge_clustering_co_list)
        count_of_min_eb = edge_clustering_co_list.count(min_ecc)
        if count_of_max_eb > 1:
            print 'in if clause of count_of_max_eb 1'
            if count_of_min_ecc > 1:
                print 'in if clause of count_of_min_eb 1'
                duplicate_eb_index = index_of_duplicates(edge_betweenness_list, max_eb)
                duplicate_ecc_index = index_of_duplicates(edge_clustering_co_list, min_ecc)
                common_index_list = sorted(list(set(duplicate_eb_index).intersection(set(duplicate_ecc_index))))
                common_index_len = len(common_index_list)
                for i in common_index_list:
                    print 'in for loop of common_index_list'
                    if i not in outer_loop_del_edge_list:

                        print 'in if clause of outer_loop_edge_list1'
                        outer_loop_del_edge_list.append(i)
                        edge_to_delete_outer = edge_list[i]
                        g.delete_edges([edge_to_delete_outer])
                        splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=0)
                        edge_list = g.get_edgelist()
                        edge_betweenness_list = g.edge_betweenness()
                        edge_clustering_co_list = edge_clustering_co()
                        threshold_ecc_inner = max(edge_clustering_co_list)
                        while(threshold_ecc_inner > 0.7):

                            print 'in while clause of threshold_ecc_inner'
                            max_eb = max(edge_betweenness_list)
                            count_of_max_eb = edge_betweenness_list.count(max_eb)
                            min_ecc = min(edge_clustering_co_list)
                            count_of_min_ecc = edge_clustering_co_list.count(min_ecc)
                            if count_of_max_eb > 1:
                                print 'in if clause of count_of_max_eb 2'
                                if count_of_min_ecc > 1:
                                    print 'in if clause of count_of_min_ecc 2'
                                    duplicate_eb_index = index_of_duplicates(edge_betweenness_list, max_eb)
                                    duplicate_ecc_index = index_of_duplicates(edge_clustering_co_list, min_ecc)
                                    common_index_list = sorted(list(set(duplicate_eb_index).intersection(set(duplicate_ecc_index))))
                                    common_index_len = len(common_index_list)
                                    for i in common_index_list:
                                        print 'in for loop threshold_ecc_inner'
                                        if i not in outer_loop_del_edge_list:
                                            print 'in if clause of outer_loop_del_edge_list2'
                                            outer_loop_del_edge_list.append(i)
                                            edge_to_delete_inner = edge_list[i]
                                            g.delete_edges([edge_to_delete_inner])
                                            splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=edge_to_delete_inner)
                                            edge_clustering_co_list = edge_clustering_co()
                                            threshold_ecc_inner = max(edge_clustering_co_list)
                    break

            else:
                print 'in else clause'
                duplicate_eb_index = index_of_duplicates(edge_betweenness_list, max_eb)
                i = set(duplicate_eb_index).intersection(edge_clustering_co_list.index(min_ecc))
                edge_to_delete_outer = edge_list[i]
                if edge_to_delete_outer not in outer_loop_del_edge_list:
                    print 'in if clause of else'
                    g.delete_edges([edge_to_delete_outer])
                    splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=0)
                    edge_list = g.get_edgelist()
                    edge_betweenness_list = g.edge_betweenness()
                    edge_clustering_co_list = edge_clustering_co()
                    threshold_ecc_inner = max(edge_clustering_co_list)
                    while(threshold_ecc_inner > 0.7):
                        print 'in while clause of threshold_ecc_inner'
                        max_eb = max(edge_betweenness_list)
                        count_of_max_eb = edge_betweenness_list.count(max_eb)
                        min_ecc = min(edge_clustering_co_list)
                        count_of_min_ecc = edge_clustering_co_list.count(min_ecc)
                        if count_of_max_eb > 1:
                            print 'in else clause threshold_ecc_inner count_of_max_eb'
                            if count_of_min_ecc > 1:
                                print 'in else clause threshold_ecc_inner count_of_min_ecc'
                                duplicate_eb_index = index_of_duplicates(edge_betweenness_list, max_eb)
                                duplicate_ecc_index = index_of_duplicates(edge_clustering_co_list, min_ecc)
                                common_index_list = sorted(list(set(duplicate_eb_index).intersection(set(duplicate_ecc_index))))
                                common_index_len = len(common_index_list)
                                for i in common_index_list:
                                    if i not in outer_loop_del_edge_list:
                                        outer_loop_del_edge_list.append(i)
                                        edge_to_delete_inner = edge_list[i]
                                        g.delete_edges([edge_to_delete_inner])
                                        splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=edge_to_delete_inner)
                                        edge_clustering_co_list = edge_clustering_co()
                                        threshold_ecc_inner = max(edge_clustering_co_list)

        else:
            ind = edge_betweenness_list.index(max_eb) == edge_clustering_co_list.index(min_ecc)
            print 'in else clause of unique eb and ecc but different edges'
            if ind:
                print 'in if clause of unique eb and ecc'
                index = edge_betweenness_list.index(max_eb)
                edge_to_delete_outer = edge_list[index]
                if edge_to_delete_outer not in outer_loop_del_edge_list:
                    g.delete_edges([edge_to_delete_outer])
                    splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=0)
                    edge_list = g.get_edgelist()
                    edge_betweenness_list = g.edge_betweenness()
                    edge_clustering_co_list = edge_clustering_co()
                    threshold_ecc_inner = max(edge_clustering_co_list)
                    while(threshold_ecc_inner > 0.7):
                        print 'in while clause of inner threshold'
                        max_eb = max(edge_betweenness_list)
                        count_of_max_eb = edge_betweenness_list.count(max_eb)
                        min_ecc = min(edge_clustering_co_list)
                        count_of_min_ecc = edge_clustering_co_list.count(min_ecc)
                        if count_of_max_eb > 1:
                            if count_of_min_ecc > 1:
                                duplicate_eb_index = index_of_duplicates(edge_betweenness_list, max_eb)
                                duplicate_ecc_index = index_of_duplicates(edge_clustering_co_list, min_ecc)
                                common_index_list = sorted(list(set(duplicate_eb_index).intersection(set(duplicate_ecc_index))))
                                common_index_len = len(common_index_list)
                                for i in common_index_list:
                                    if i not in outer_loop_del_edge_list:
                                        outer_loop_del_edge_list.append(i)
                                        edge_to_delete_inner = edge_list[i]
                                        g.delete_edges([edge_to_delete_inner])
                                        splitting_factor_and_community_check(outer=str(edge_to_delete_outer), inner=edge_to_delete_inner)
                                        edge_clustering_co_list = edge_clustering_co()
                                        threshold_ecc_inner = max(edge_clustering_co_list)
