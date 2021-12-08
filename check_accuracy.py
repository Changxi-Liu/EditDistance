#! /usr/bin/python3 
import numpy as np
import sys
import json
from tqdm import tqdm
from multiprocessing import Pool
from utils import arg_sort,l2_dist
import os
import Levenshtein
from multiprocessing import cpu_count
import argparse
def get_args():
    parser = argparse.ArgumentParser(description="HyperParameters for String Embedding")
    parser.add_argument("--norm", type=int , default=2, help="norm type")
    parser.add_argument(
        "--shuffle-seed", type=int, default=808, help="seed for shuffle"
    )

    parser.add_argument("--path", type=str, default=None, help="path")
    args = parser.parse_args()

    return args
args = get_args()
path = args.path
norm_type = args.norm
if norm_type == -1:
    norm_type = np.inf
print(norm_type)
#exit(1)
def get_embed( path ):
    base_ids = np.load( path + "base_idx.npy")
    query_ids = np.load( path + "query_idx.npy" )
    train_ids = np.load( path + "train_idx.npy" )
    xt = np.load( path+"embedding_xt.npy")
    xq = np.load( path+"embedding_xq.npy")
    xb = np.load( path+"embedding_xb.npy")
    return base_ids,query_ids,train_ids,xt,xq,xb
base_ids,query_ids,train_ids,xt,xq,xb = get_embed( path )

with open("data/references","r") as f:
    lines = f.readlines()
    cluster_num = int(lines[0])
    cluster_lines = lines[1:]

with open("data/references_cluster","r") as f:
    str1 = f.read()
    correct_dict = json.loads(str1)
    
print(type(correct_dict))

K = [1,2,4,8,16,32,64,128]
max_K = max(K)
def get_cluster( emb ):
    xq_shape = xq.shape
    length = xq_shape[0]
    norms = [0] * length
    for i in range( xq_shape[0]):
        
        new_data = np.linalg.norm( emb-xq[i],norm_type )
        norms[i] = new_data
    sort_norm_idx = np.argsort( norms )
    return sort_norm_idx[ : max_K ] 
#    print( min_value,min_idx )
#    return res
def get_levenshtein_cluster( para ):
    idx, sort_norm_idx = para
    edits = [0] * max_K
    j = 0
    for i in sort_norm_idx : 
        new_data = Levenshtein.distance( cluster_lines[idx], cluster_lines[i])
        edits[ j ] = new_data
        j+=1

    cluster_ids = [ -1 ] * len(K)
    j = 0
    for k in K:
        min_idx = np.argmin( edits[:k] )
        cluster_ids[ j ] = sort_norm_idx[min_idx]
        j += 1
    return cluster_ids


def calculate( ids , embs,n_thread,flag="train", progress = True ):
    right_numer = 0
    num = len( ids)
    print( num )
    print( embs.shape )
    bar = tqdm if progress else lambda iterable, total, desc: iterable
    def all_pair(embs_para,  n_thread):
        with Pool(n_thread) as pool:
            edit = list(
                bar(
                    pool.imap(get_cluster,embs_para ),
                    total= num ,
                    desc="# clustering ",
                ))
            return np.array(edit)
    cluster_file = flag + "_cluster.npy"
    if not os.path.isfile( path+"/" + cluster_file):
        clusters = all_pair( embs,n_thread )
        np.save( path + "/" + cluster_file , clusters )
    else:
        clusters = np.load( path + "/" + cluster_file )
    def all_edit_pair( ids_para ,n_thread):
        with Pool(n_thread) as pool:
            edit = list(
                bar(
                    pool.imap(get_levenshtein_cluster, zip(ids_para,clusters )),
                    total= num ,
                    desc="# clustering ",
                ))
            return np.array(edit)
    real_clusters = all_edit_pair( ids, n_thread )
    for ki in range( len(K)):
        right_numer = 0
        for qi in range( num ):
            cluster_ids = real_clusters[qi][ki]
            
            id1 = ids[qi]
            cluster_str = cluster_lines[cluster_ids][:-1]
            if id1 in correct_dict[ cluster_str ]:
                right_numer += 1
        print( "K = ",K[ki] ," Accuracy : ", right_numer * 1. / num  )
calculate( train_ids, xt ,cpu_count(),"train"+str(norm_type)) 
#calculate( base_ids[0:10000], xb[0:10000] ,cpu_count()//2) 
calculate( base_ids , xb  ,cpu_count(),"base"+str(norm_type)) 
#calculate( query_ids, xq, cpu_count()//2 ) 
#data = l2_dist( xq, xt[0:1] )
#print(data )
