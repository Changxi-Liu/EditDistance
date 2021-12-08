# [Convolutional Embedding for Edit Distance (SIGIR 20)](https://arxiv.org/abs/2001.11692)

This is the CS6219 module project merged from https://github.com/xinyandai/string-embed.git.
We have modified convolutional neural network structure and execution procedure to predict the clustering status of each DNA strands. 
There are also preprocess.py for preprocessing DNA data and check_accuracy.py to check the accuracy of embedded vector.

### before run
Please install PyTorch refer to [PyTorch](https://pytorch.org/get-started/locally/) 
and install Levenshtein and transformers via 
```
pip install python-Levenshtein
pip install transformers
```


### start training
- move dna data into data/ directory
- ./preprocess.py
- train CNN-ED model
```    
python main.py --dataset word --nt 10000 --nq 1000 --epochs 20 --save-split --save-embed --embed-dim 16
```
- derive the accuracy 
```
./check_accuracy.py --path ${model_path} --norm 2
```
##### optional arguments:
      -h, --help            show this help message and exit
      --dataset             dataset name which is under folder ./data/
      --nt                  # of training samples
      --nr                  # of generated training samples
      --nq                  # of query items
      --nb                  # of base items
      --k                   # sampling threshold
      --epochs              # of epochs
      --shuffle-seed        seed for shuffle
      --batch-size          batch size for sgd
      --test-batch-size     batch size for test
      --channel CHANNEL     # of channels
      --embed-dim           output dimension
      --save-model          save cnn model
      --save-split          save split data folder
      --save-embed          save embedding
      --random-train        generate random training samples and replace
      --random-append-train generate random training samples and append
      --embed-dir           embedding save location
      --recall              print recall
      --embed EMBED         embedding method
      --maxl MAXL           max length of strings
      --no-cuda             disables GPU training



# reference
If you use this code, please cite the following [paper](https://dl.acm.org/doi/abs/10.1145/3397271.3401045)
```
@inproceedings{cnned,
  author    = {Xinyan Dai and
               Xiao Yan and
               Kaiwen Zhou and
               Yuxuan Wang and
               Han Yang and
               James Cheng},
  title     = {Convolutional Embedding for Edit Distance},
  booktitle = {Proceedings of the 43rd International {ACM} {SIGIR} conference on
               research and development in Information Retrieval, {SIGIR} 2020, Virtual
               Event, China, July 25-30, 2020},
  pages     = {599--608},
  publisher = {{ACM}},
  year      = {2020},
  url       = {https://doi.org/10.1145/3397271.3401045},
  doi       = {10.1145/3397271.3401045},
}
```

