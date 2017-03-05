from igraph import *
import csv
g = Graph().Read_Edgelist('football_network.txt',directed=False)
g.simplify()
f = g.community_multilevel()
print(dir(f))
print(len(f))
print(f)

with open('fname.csv','wb') as file:
    csvWriter = csv.writer(file)
    for index in range(len(f)):
        for j in f[index]:
            csvWriter.writerow((index,j))
