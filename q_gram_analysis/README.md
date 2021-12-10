The home directory contains the following different directories/file:
1. synth_data : synth_data contains synthetic DNA dataset of different error rate generated from NUS CS6219 Minilab1.
2. dna_clustering : dna_clustering contains code to generate binary embeddings for q-gram. The code is from NUS CS6219 Minilab1.
3. preprocess.py : process the embeddings generated from dna_clustering to format suitable for accuracy_checker.py
4. accuracy_checker.py : takes in the binary embeddings and the actual DNA strands to get the accuracy illustrated in the presentation.


Env Requirement
- Minilab1 env
- numpy
- Levenshtein