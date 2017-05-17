from igraph import *

'''
fill(0, g.community_multilevel().membership)
fill(1, g.community_label_propagation().membership)
fill(2, g.community_infomap().membership)
fill(3, g.community_walktrap().as_clustering().membership)
fill(4, g.community_fastgreedy().as_clustering().membership)
fill(5, g.community_edge_betweenness().as_clustering().membership)
'''

g = Graph().Read_Edgelist('simple_network ScaleFreeCDA.txt', directed=False)
g.simplify()
print 'community_multilevel(), Louvian:  '
a  = g.community_multilevel()
print str(a), '\n'
print 'community_label_propagation():   '
print g.community_label_propagation(), '\n'
print 'community_infomap(): '
print g.community_infomap(), '\n'
print 'community_walktrap():    '
print g.community_walktrap().as_clustering(), '\n'
print 'community_fastgreedy():  '
print g.community_fastgreedy().as_clustering(), '\n'
print 'community_edge_betweenness(), girvan-newman: '
print g.community_edge_betweenness().as_clustering(), '\n'

