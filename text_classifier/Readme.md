Multi-Class Text Classifier
========================================================================

This is an attempt to classify text articles via Google's Word2Vec representation of words as vectors. This has been done by preprocessing NYTimes Articles in Academic Corpus. 

Preprocessing Articles:
------------------------
NYTimes academic corpus has 1.8m articles. Out of those articles only 1.5m articles have tags given by taxonomists assisted by CatCon service. 

These articles are further processed to strip off all stopwords, convert words to their base form using WordNet Lemmatizer. (No stemming is done), replace numbers with 'num' and throwing out all punctuations.

Files :
-------
For the purpose of classifier we have taken articles which have tags present in atleast 100 articles. There are around 1,302,400 such articles in final data set. There are several files corresponding to information about corpus.
- text.txt : All preprocessed articles are present in this file. Each line corresponds to a article. Text in each line is preprocessed in a way explained above
- labels.txt : Each line in this file relates to same line in text.txt. Contents of this line is labels as were present in academic corpus. *Several labels are separated by ' %;% '* 
- line_indices.txt: text.txt is 2.8GB in size making it difficult to handle in memory. For this purpose whole string is not loaded in memory at same time. Rather a separate file which contains a json with keys as line number and length of text(text.txt) till that line number as values. 

Example : {1 : 0, 2:10023, 3:23122,...}

so that if someone wants to access text at line #3, all that needs to be done is to point file at 23122nd Character and read line using file.readline().

w2v_Classifier contains classes that will load all such files. w2v_Classifier.SetupClassifier contains seekline() function which accepts numbers. One can give line number (corresponding to text.txt) and it can return text in that line.
	
- nyt_ids.txt : this file contains Article IDs corresponding to NYT Academic Corpus as present in text.txt. So if #1 line says 193842, it means that text in #1 line of text.txt is from Article ID 193842. If all the articles are in mongoDB indexed with article IDs one can easily look at the article by calling find() function with key as '_id'.
- tag_counts.txt : It is json string with keys as 1013 unique labels and # of times those tags are present in 1,302,400 articles
- useful_ids.txt : These are Article IDs which have tags. Not all articles have tags and not all tags are present in more than 100 articles. 
- tag_stats.txt : This file contains labels and corresponding line# (not actual ArticleIDs) in text.txt which contains this label.
- doc_vec.npy : doc_vec.npy is numpy matrix of document vectors. It is 800MB in size. It contains 100 dimensional representation of document vectors. It is 1m X 100 shaped dense matrix. It need to be in memory in order to perform classification. It is formed by summing over word vectors in w2v_model.mod (formed by gensim)
- tag_vec.npy : it is similar to doc_vec.npy difference being that it contains representation of tag vectors formed by summing document vectors over a single tag.
- w2v_model.mod, w2v_model.mod.syn0.npy, w2v_model.mod.syn1.npy:  contains words and their vectors. It is used by gensim in to update word vectors and give out word vectors.
- Classifier's performance is given in w2v_Classifier.csv

Classification Task:
-------------------
Classification task is looked at from three different perspective. All in fact are Nearest Neighbor Classifiers. Metric of how close are two points to each other is given by:
a. Dot Products (abbreviated as dots)
b. Euclidean distance (abbreviated as dists)
c. Combination of both (abbreviates as dots_and_dists)

*There was also an attempt to classify based on tags but owing to very close clusters as depicted in t-SNE plot the idea was dropped.*

Classification app:
-------------------
This app can be started by running classifier.py and send request at :

- curl request:

curl ec2-54-198-18-10.compute-1.amazonaws.com:8888/track_topics -d @body.json -H "Content-Type: application/json"

where body.json looks like:
{"body": "your article goes here"}

- It returns json with key as labels




















