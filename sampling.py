#! /usr/bin/python3 
import numpy as np
import json
import sys
import math
import argparse

def get_embed( path ):
    base_ids = np.load( path + "base_idx.npy")
    query_ids = np.load( path + "query_idx.npy" )
    train_ids = np.load( path + "train_idx.npy" )
    xt = np.load( path+"embedding_xt.npy")
    xq = np.load( path+"embedding_xq.npy")
    xb = np.load( path+"embedding_xb.npy")
    x = np.concatenate( (xq,xt,xb))
    ids = np.concatenate( (query_ids,train_ids,base_ids))
    res = [None] * data_number
    for idx in ids:
        res[ idx ] = x[idx]
    return res

def real_same_cluster( id1,id2 ):
    cluster_id1 = correct_dict[id1 ]
    cluster_id2 = correct_dict[id2 ]
    return cluster_id1 == cluster_id2
def predict_same_cluster(id1,id2):
    thresold = 0.3
    new_data = math.sqrt(np.linalg.norm( emb_vectors[id1] - emb_vectors[id2] ))
    return new_data <= thresold
def get_args():
    parser = argparse.ArgumentParser(description="HyperParameters for String Embedding")
    parser.add_argument("--predict-threshold", action="store_true", default=False, help="if help to predit threshold")
    parser.add_argument(
        "--shuffle-seed", type=int, default=808, help="seed for shuffle"
    )

    parser.add_argument("--path", type=str, default=None, help="path")
    args = parser.parse_args()

    return args
if __name__ == "__main__":
    args = get_args()

    np.random.seed( args.shuffle_seed)
    with open("data/references","r") as f:
        lines = f.readlines()
        cluster_num = int(lines[0])
        cluster_lines = lines[1:]
    data_number = len(cluster_lines)
    str_lines = cluster_lines
    with open("data/references_clusterid","r") as f:
        str1 = f.read()
        correct_dict_tmp = json.loads(str1)
        correct_dict = [0] * data_number
        for elem in correct_dict_tmp.keys():
            correct_dict[ int(elem) ] = correct_dict_tmp[elem]
    if args.path != None:
        path = args.path 
    else:
        print( "You should define path" )
        exit(1)
    emb_vectors = get_embed( path )
    sampling_num = 100000
    sampling_index = np.random.randint( data_number , size=(sampling_num,2))
    data = []
    correct_num = 0
    data2 = []
    if args.predict_threshold:
        for elem in sampling_index:
            id1 , id2 = elem
            new_data = math.sqrt( np.linalg.norm( emb_vectors[id1] - emb_vectors[id2] ) )
            if( real_same_cluster(id1,id2) ):
                data.append(new_data)
            else:
                data2.append(new_data)
        print(data)
        np_data = np.array(data)
        print( np.mean(np_data) )
        print( np.var(np_data) )

        np_data = np.array(data2)
        print( np.mean(np_data) )
        print( np.var(np_data) )

    else:
        correct_num = 0
        for elem in sampling_index:
            id1 , id2 = elem
            true_flag = real_same_cluster(id1,id2) 
            predict_flag = predict_same_cluster(id1,id2)
            if true_flag == predict_flag:
                correct_num += 1
        print( "Accuracy: {} %".format( correct_num * 100. / sampling_num  ))

