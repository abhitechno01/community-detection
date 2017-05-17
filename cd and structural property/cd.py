from igraph import *
import csv
filename = 'simple_network from ppt'
#g = Graph().Read_GML(filename+'.gml')
g = Graph().Read_Edgelist(filename+'.txt', directed=False)
g.simplify()

cda = {
        g.community_multilevel():'_multilevel_louvian_',
        g.community_label_propagation():'_labelpropagation_',
        g.community_infomap():'_infomap_',
        g.community_walktrap().as_clustering():'_walktrap_',
        g.community_fastgreedy().as_clustering():'_fastgreedy',
        g.community_edge_betweenness().as_clustering():'_edge_betweenness_newmangirvan_'

}

for i in cda:
    print i
    fname = filename+cda[i]+'.csv'
    with open(fname,'wb') as file:
        csvWriter = csv.writer(file)
        for index in range(len(i)):
            for j in i[index]:
                csvWriter.writerow((j, index))