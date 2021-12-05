#! /usr/bin/python3 
import numpy as np
import sys
import json
from tqdm import tqdm
from multiprocessing import Pool
from utils import arg_sort,l2_dist

import Levenshtein
from multiprocessing import cpu_count
path = ( sys.argv[1] )
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

def get_cluster( emb ):
    xq_shape = xq.shape
    min_value = Levenshtein.distance(emb, cluster_lines[0]) 
    min_idx = 0
    for i in range(1,xq_shape[0]): 
        new_data = Levenshtein.distance(emb, cluster_lines[i]) 
        if( new_data < min_value ):
            min_value = new_data
            min_idx = i
#    print( min_value,min_idx )
    return min_idx

def calculate( ids , embs,n_thread,progress = True ):
    right_numer = 0
    num = len( ids)
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
    clusters = all_pair( embs,n_thread )

    for qi in range( num ):
        cluster_id = clusters[qi]
        id1 = ids[qi]
        cluster_str = cluster_lines[cluster_id][:-1]
        if id1 in correct_dict[ cluster_str ]:
            right_numer += 1
    #    else:
    #        print( id1 , cluster_lines[id1] )

    #        print( cluster_lines[ cluster_id] )
    #        for elem in correct_dict.keys():
    #            if id1 in correct_dict[elem]:
    #                print( cluster_lines[ correct_dict[elem][0] ] )
    #                break
    #        exit(1)
        #    print( id1,correct_dict[str(cluster_id)])
    print( "Accuracy : ", right_numer * 1. / num  )
#calculate( train_ids, xt ,cpu_count()//2)
xb_string = [""] * 10000
i = 0
for elem in base_ids[0:10000]:
    xb_string[ i ] = cluster_lines[elem]
    i = i+1
calculate( base_ids[0:10000], xb_string[0:10000] ,cpu_count()//2) 
#calculate( query_ids, xq, cpu_count()//2 ) 
#data = l2_dist( xq, xt[0:1] )
#print(data )
