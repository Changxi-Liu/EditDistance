#! /usr/bin/python3 
import json
query_str = ""
output_str = ""
cluster_num = 0
id_str = 0

string2ids = dict()
sum_num = 0 
with open("data/combined_clusters_with_references.txt","r") as f:
    lines = f.readlines()
    num = len(lines)
    i = 0
    while i < num :
        line = lines[i]
        cluster_data_num = int(line)
        j = 0
        ids = []
        for j in range( cluster_data_num ):
            idx = i + j + 2
            line = lines[idx]
            output_str += line
            ids.append(id_str)
            id_str += 1
        cluster_str = lines[i+1][:-1]
        if(cluster_str in string2ids):
            string2ids[ cluster_str ] += ids
            sum_num += 1
        else:
            query_str += cluster_str+"\n"
            ids = [(cluster_num)] + ids
            string2ids[ cluster_str ] = ids
            cluster_num += 1
            sum_num += 1
        i += cluster_data_num + 2
for elem in string2ids.keys():
    vec = string2ids[elem]
    for i in range(1,len(vec)):
        vec[i] = vec[i] + cluster_num
print( sum_num ) 
id2clusterid = dict()
cluster_id = 0
for elem in string2ids.keys():
    vec = string2ids[elem]
    for i in range(len(vec)):
        id2clusterid[ vec[i] ] = cluster_id
    cluster_id += 1

json_data = json.dumps( id2clusterid , sort_keys=True, indent=4)
with open("data/references_clusterid","w") as f:
    f.write(json_data)


json_data = json.dumps( string2ids , sort_keys=True, indent=4)
with open("data/references_cluster","w") as f:
    f.write(json_data)

with open("data/references","w") as f:
    f.write(str(cluster_num) + "\n"  + query_str + output_str )
