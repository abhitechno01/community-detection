from igraph import *
import csv
import xlwt

filename = raw_input("Input filename... ")
g = Graph().Read_Edgelist(filename+'.txt', directed = False)
g.simplify()

vertex_count = g.vcount()
edge_count = g.ecount()
edge_list = g.get_edgelist()
edge_betweenness_list = g.edge_betweenness()
edge_clustering_co_list = []

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

'''
def write_excelsheet():
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Edge_Clustering')
    column_list = [
                    #'Edge',
                    'Edge Betweenness',
                    'Edge Clustering Coefficient'

                    ]
    for i in range(0,len(column_list)):
        ws.write(0, i, column_list[i])
    for i in range(0, g.ecount()):
        #ws.write(i+1, 0, int(edge_list[i]))
        ws.write(i+1, 0, int(edge_betweenness_list[i]))
        ws.write(i+1, 1, int(edge_clustering_co_list[i]))
    wb.save('edge_clustering_footballnw.xls')
'''

def write_csv(normalized):
    global edge_list, vertex_count, edge_count, edge_betweenness_list, edge_clustering_co_list
    CONSTANT = 1
    if normalized:
        CONSTANT = float(2)/(vertex_count*(vertex_count-1))
    file_to_save = raw_input("Input filename to save... ")
    writer = csv.writer(open(file_to_save+'_Edge_Betweenness_ECC.csv', 'wb'))
    writer.writerow(['Edge', 'Edge Betweenness', 'Edge Clustering Coefficient'])
    for i in range(edge_count):
        writer.writerow([edge_list[i], CONSTANT*edge_betweenness_list[i], edge_clustering_co_list[i]])


edge_clustering_co()
write_csv(normalized=True)
#write_excelsheet()

