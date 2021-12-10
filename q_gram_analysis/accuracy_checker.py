#! /usr/bin/python3 
import numpy as np
import sys
import json
from tqdm import tqdm
from multiprocessing import Pool
# from utils import arg_sort,l2_dist
import os
import Levenshtein
from multiprocessing import cpu_count

error_folder = "error9"

def get_strand( path ):
    temp = []
    f = open(path,'r')
    temp = f.readlines()
    f.close()
    return temp

binary_sig = get_strand('synth_data/'+ error_folder + '/bin_synth_noisy_strand.txt')
cluster_bin_sig = get_strand('synth_data/'+ error_folder + '/bin_synth_ref_strand.txt')

noisy_strand = get_strand('synth_data/'+ error_folder + '/synth_NoisyStrands_analysis.txt')
cluster_strand = get_strand('synth_data/'+ error_folder + '/synth_cluster_strands_analysis.txt')

with open('synth_data/'+ error_folder + '/synth_references_cluster_analysis',"r") as f:
    str1 = f.read()
    correct_dict = json.loads(str1)

def hamming_distance(x, y):
    z = int(x,2) ^ int(y,2)
    return bin(z).count("1")

K = [1,2,4,8,16,32,64,128]
max_K = max(K)
def get_cluster(signature):
    dist = [0] * len(cluster_bin_sig)
    for j in range(len(cluster_bin_sig)):
        dist[j] = hamming_distance(signature, cluster_bin_sig[j])
    sort_norm_idx = np.argsort(dist)
    return sort_norm_idx[:max_K]

def get_levenshtein_cluster( para ):
    strand, sort_norm_idx = para
    edits = [0] * max_K
    j = 0
    for i in sort_norm_idx : 
        new_data = Levenshtein.distance(strand, cluster_strand[i]) #actual dna strand compare with actual cluster strands
        edits[ j ] = new_data
        j+=1

    cluster_ids = [ -1 ] * len(K) #for different K values
    # print(len(cluster_ids))
    # print(len(sort_norm_idx))
    j = 0
    for k in K:
        min_idx = np.argmin( edits[:k] )
        cluster_ids[ j ] = sort_norm_idx[min_idx]
        j += 1
    return cluster_ids

def calculate(n_thread,progress = True ):
    right_numer = 0
    total_strands = len(binary_sig)

    bar = tqdm if progress else lambda iterable, total, desc: iterable
    def all_pair(embs_para,  n_thread):
        with Pool(n_thread) as pool:
            edit = list(
                bar(
                    pool.imap(get_cluster,embs_para ),
                    total= total_strands ,
                    desc="# clustering ",
                ))
            return np.array(edit)
    

    clusters = all_pair(binary_sig,n_thread )
    #print(len(clusters))

    def all_edit_pair( ids_para ,n_thread):
        with Pool(n_thread) as pool:
            edit = list(
                bar(
                    pool.imap(get_levenshtein_cluster, zip(ids_para,clusters )),
                    total= total_strands ,
                    desc="# clustering ",
                ))
            return np.array(edit)
    
    real_clusters = all_edit_pair( noisy_strand, n_thread )
    # print(real_clusters)
    
    for ki in range( len(K)):
        right_numer = 0
        for qi in range( total_strands ):
            cluster_ids = real_clusters[qi][ki]
            
            # id1 = ids[qi]
            # cluster_str = cluster_strand[cluster_ids][:-1]
            if qi in correct_dict[str(cluster_ids)]:
                right_numer += 1
                
        print( "K = ",K[ki] ," Accuracy : ", right_numer * 1. / total_strands  )

calculate(cpu_count()//2) 






