import gensim
model = gensim.models.Word2Vec.load('w2v_model.mod')

limit = 1000000
doc_vec = numpy.ndarray(shape = (100, limit))

#not used
def line(limit):
	for line in islice(open('text.txt','r'), limit):
		yield sum(model[word] for word in line.split())

## Creating dcoument vector
f=  open('text.txt', 'r')
doc_vec = numpy.zeros((1000000,100))
for v, line in enumerate(islice(f,limit)):
	words = re.sub('\"','',line).strip().split()
	doc_vec[v,] = sum(model[word] for word in words if word in model)

numpy.save('doc_vec.npy', doc_vec)
numpy.load('doc_vec.npy')



## one liner
doc_vec = array([sum(model[word] for word in re.sub('\"','', line).strip().split()) for v,line in enumerate(f.readline()) if v < 1000000])

#### Label statistic
labels = open('labels.txt','r').read().split('\n')
count = defaultdict(int)
for i in test.labels[:1000000]:
	i = re.sub('\"', '',i).strip()
	labels = i.split(" %;% ")
	for it in labels:
		count[it]+=1

with open('tag_counts.txt', 'a') as f:
	f.write(json.dumps(dict(count)))

##### Accessing text.txt content easily : store indices
f= open('text.txt','r')
file_index, length, index = {}, 0, 0
for line in f:
	file_index[index] = length 
	length += len(line)
	index += 1

with open('line_indices.txt','w') as f:
	f.write(json.dumps(file_index))

### Access particular line_number
import json
file_index= json.loads(open('line_indices.txt','r').read())
def seekline(f ,line_no):
	f.seek(file_index[str(line_no)])
	return f.readline()

#### store closest matches in test set (top 50 matches)
## max line number is 1320399
def distances(doc_vec, vec):
	diff_dist = numpy.subtract(doc_vec, vec)
	dist = [numpy.sqrt(i.dot(i)) for i in diff_dist]
	return sorted( enumerate(dist), key = lambda x: x[1] )[:50]

def cosine_angles(doc_vec, vec):
	vec_dots = numpy.dot(doc_vec, vec)/numpy.dot(vec,vec)
	doc_vec_dots = [numpy.sqrt(numpy.dot(i,i)) for i in doc_vec]
	angles = [numpy.arccos(j/i) *360/2/numpy.pi for i,j in zip(doc_vec_dots, vec_dots)]
	return sorted(enumerate(angles), key =  lambda x: x[1] )[:50]

import numpy, gensim
from collections import defaultdict 
model = gensim.models.Word2Vec.load('w2v_model.mod')
f= open('text.txt', 'r')
ind_dist, ind_angle = defaultdict(list), defaultdict(list)
import re
for i in xrange(1000000, 1320400):
	i=1000050
	line = seekline(f,i)
	vec = sum(model[word] for word in re.sub('\"','',line).strip().split() if word in model)
	ind_dist[i].append(distances(doc_vec, vec))
	ind_angle[i].append(cosine_angles(doc_vec, vec))

with open('test_dist.txt', 'w') as f, open('test_angles.txt','w') as l:
	f.write(json.dumps(ind_dist)), l.write(json.dumps(ind_angle))

#### Calculating Accuracy by Hamming Distance

model = gensim.models.Word2Vec.load('w2v_model.mod')

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def article2vec(x):
	f.seek(x)
	article = f.readline()
	vec = sum(model[word] for word in re.sub('\"','',article).strip().split() if word in model)
	return vec

def BestTenDots(doc_vec, vec):
	dots = numpy.dot(vec, doc_vec.T)
	return numpy.argsort(dots)[:10]

def getLabels(i):
	return re.sub('\"','',labels[i]).strip().split(' %;% ')

def BestLabels(Topn, threshold, nearest_docs):
	labels = reduce(list.__add__, [getLabels(i) for i in nearest_docs[:Topn]])
	set_labels = set(labels)
	return set([i for i in set_labels if prob(i, labels) > threshold ])

def prob(label, labels):
	return labels.count(i)/len(labels)

def HammingDistance(actual, tagged):
	return float(len(actual & tagged))/float(len(actual | tagged))

## Dot product
total_hd = 0
sample =  numpy.random.randint(1000000, 1320400, 10000)
for v,i in enumerate(sample):
	if v%5 == 0:
		logging.info('Progress @ %d', v)
	article_vec = article2vec(i)
	nearest_docs = BestTenDots(doc_vec, article_vec)
	actual_labels = set(getLabels(i))
	tag_labelset = BestLabels(5, 0.5, nearest_docs)
	hd = HammingDistance(actual_labels, tag_labelset)
	total_hd += hd
	del nearest_docs,article_vec

average_hd = total_hd/10000


## Distance
def BestTenDist(doc_vec, article_vec):
	diff = (doc_vec - article_vec)
	norms = [numpy.sqrt(numpy.dot(i,i)) for i in diff]
	return argsort(f)[:10]
 
total_hd = 0
sample =  numpy.random.randint(1000000, 1320400, 10000)
for v,i in enumerate(sample):
	if v%5 == 0:
		logging.info('Progress @ %d', v)
		article_vec = article2vec(i)
	nearest_docs = BestTenDist(doc_vec, article_vec)
	actual_labels = set(getLabels(i))
	tag_labelset = BestLabels(5, 0.5, nearest_docs)
	hd = HammingDistance(actual_labels, tag_labelset)
	total_hd += hd
average_hd = total_hd/10000




!@#!@#!$@~%!@%!@#%@#!%@%!@#%!@#%!@%!@#%!@#%@!%@!#%!@#$@#$!@#$@#%!@!@%@#
import sys
sys.path.append('/home/ubuntu/texttools/lda')
import w2v_Classifier as c

test = c.TestNNClassifier()
test.Decide_dot_dist()



a = numpy.random.randint(1000000, 1302400, 6)
for i in a:
	print i, test.classify(test.seekline(i)), test.getLabels(i)


#### Initialize
import numpy, json
doc_vec = numpy.load('doc_vec.npy')
file_index = json.loads(open('line_indices.txt', 'r').read())


## extract labels
## angle:


labels[]

## precision
## recall
## f1
## accuracy



### implement other 3

### LSI onliune


