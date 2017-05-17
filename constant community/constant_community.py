import csv
from operator import itemgetter

def sort_content(csvread):
        l = []
        for line in csvread:
            a = [int(line[0]), int(line[1])]
            l.append(a)
        return(sorted(l, key= itemgetter(1)))

file_name = [
    'footballnw_edge_betweenness_newmangirvan_final.csv',
    'footballnw_fastgreedyfinal.csv',
    'footballnw_infomap_final.csv',
    'footballnw_labelpropagation_final.csv',
    'footballnw_multilevel_louvian_final.csv',
    'footballnw_walktrap_final.csv'
    ]

with open(file_name[0], 'rb') as f, \
    open(file_name[1], 'rb') as f1, \
    open(file_name[2], 'rb') as f2, \
    open(file_name[3], 'rb') as f3, \
    open(file_name[4], 'rb') as f4, \
    open(file_name[5], 'rb') as f5, \
    open('constant_community.csv', 'wb+') as f6:
    csv_Writer = csv.writer(f6)
    csv_Writer.writerow(('Node', 'Newman-Girvan', 'Fast-Greedy', 'Infomap', 'Label-propagation', 'Louvian', 'Walktrap'))
    csv_Reader, csv_Reader1, csv_Reader2, csv_Reader3, csv_Reader4, csv_Reader5 \
        = csv.reader(f), csv.reader(f1), csv.reader(f2), csv.reader(f3), csv.reader(f4), csv.reader(f5)

    l = sort_content(csv_Reader)
    l1 = sort_content(csv_Reader1)
    l2 = sort_content(csv_Reader2)
    l3 = sort_content(csv_Reader3)
    l4 = sort_content(csv_Reader4)
    l5 = sort_content(csv_Reader5)

    constant_comm = []
    for i in range(115):
        csv_Writer.writerow((i,l[i][0],l1[i][0],l2[i][0],l3[i][0],l4[i][0],l5[i][0]))
        constant_comm.append([l[i][0],l1[i][0],l2[i][0],l3[i][0],l4[i][0],l5[i][0]])
    duplicates = []
    result = dict()
    for i in range(114):
        temp_match = [i]
        if i in duplicates:
            continue
        for j in range(i+1,115):
            if constant_comm[i]==constant_comm[j]:
                temp_match.append(j)
                duplicates.append(j)
        if len(temp_match)>1:
            result[i] = temp_match
    print(result)
    with open('const_comm.csv','wb') as f:
        csv_Writer = csv.writer(f)
        for i in result:
                csv_Writer.writerow((result[i]))
