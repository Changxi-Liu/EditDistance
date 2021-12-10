import json
query_str = ""
output_str = ""
cluster_num = 0
id_str = 0
sum_cluster_size = 0
underlying_str = ""
noisy_str = ""
clusters = []
clusters_ids = dict()
cluster_strands = []

string2ids = dict()

with open("./synth_data/error3/SynthDataClusters.txt","r") as f: #combined_clusters_with_references
    lines = f.readlines()
    num = len(lines)
    print(num)
    i = 0
    strand_index = 0
    while i < num :
        line = lines[i]
        cluster_data_num = int(line)
        j = 0
        ids = []
        temp_str = ""#lines[i+1]
        temp_ids = []
        for j in range( cluster_data_num):
            idx = i + j + 2
            # if(len(lines[idx])<=108*2):
            temp_str += lines[idx]
            temp_ids.append(strand_index)
            strand_index += 1
        cluster_str = lines[i+1][:-1]
        if(cluster_data_num > 0):
            if(cluster_str in string2ids):
                # print( cluster_str )
                temp_cluster_num = string2ids[cluster_str]
                clusters[temp_cluster_num] += temp_str
                clusters_ids[temp_cluster_num] += temp_ids
            else:
                # underlying_str += "CLUSTER " + str(cluster_num) + "\n"
                # underlying_str += temp_str
                # noisy_str += temp_str

                string2ids[ cluster_str ] = cluster_num
                cluster_strands.append("")
                cluster_strands[cluster_num] = cluster_str + "\n"
                clusters.append("")
                clusters[cluster_num] += temp_str
                clusters_ids[cluster_num] = temp_ids
                cluster_num += 1
                sum_cluster_size += cluster_data_num
        i += cluster_data_num + 2

print(sum_cluster_size/(cluster_num))
# for elem in string2ids.keys():
#     vec = string2ids[elem]
#     for i in range(1,len(vec)):
#         vec[i] = vec[i] + cluster_num
    
json_data = json.dumps(clusters_ids , sort_keys=True, indent=4)
with open("./synth_data/error3/synth_references_cluster_analysis","w") as f:
    f.write(json_data)

# with open("./proj_data/references","w") as f:
#     f.write(str(cluster_num) + "\n"  + query_str + output_str )
with open("./synth_data/error3/synth_cluster_strands_analysis.txt", "w") as f:
    for i in range(len(cluster_strands)):
        f.write(cluster_strands[i])

with open("./synth_data/error3/synth_NoisyStrands_analysis.txt", "w") as f:
    for i in range(len(clusters)):
        f.write(clusters[i])

# with open("./proj_data/UnderlyingClusters_analysis.txt", "w") as f:
#     for i in range(len(clusters)):
#         f.write("CLUSTER "+ str(i) + "\n")
#         f.write(clusters[i])

print("done")
