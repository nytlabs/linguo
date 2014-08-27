'''experimental script for trying nad tesing lda model'''


import pymongo

p=pymongo.Connection().articles.collection_1

import numpy
start = 1165027
stop = 1855646
length  = stop-start+1
all_entries = numpy.arange(start, stop+1, step =1)
train_set= numpy.random.randint(start, stop, int(length*0.8)) 
test_set = set(all_entries) -  set(train_set)

## find out number of entries from 2000 to 2007 with taxonomic classifier
from collections import defaultdict
count = defaultdict(int)
no_common, no_class, classs =0,0,0
for no in all_entries:
	try:
		clsfr = p.find({'_id': no})[0]['metadata']['taxonomic_class']
		clsfr = [it.lower() for it in clsfr]
		common = tags2.intersection(set(clsfr))
		if common:
			for it in common:
				count[it]+=1
				classs +=1
			else:
				no_common+=1
	except:
		print no
		no_class +=1	

1310 tags from 2000 to 2007

length of all_entries = 690620
classs = 1615710
no_common= 500090
no_class = 1

articles with labels = 190530
train = 190530 *0.8 = 152424.0
test = 38106.0



count # each tag's frequency
no_common = 500090  #number of articles which do not have common elements



#### For all entries
import json
count2 = defaultdict(int)
no_common, no_class, classs, id =0,0,0, []
for i in p.find():
	try:
		clsfr = i['metadata']['taxonomic_class']
		clsfr = [it.lower() for it in clsfr]
		common = tags2.intersection(set(clsfr))
		if common:
			id.append(i['_id'])
			for it in common:
				count2[it]+=1
				classs +=1
		else:
			no_common+=1
	except:
		print no,
		no_class +=1	

with open('useful_ids.txt', 'w') as f:
	f.write(json.dumps(id))




##### Calculate tagwise separation

stats =defaultdict(list)
for v,line in enumerate(labels):
	tags = re.sub('\"','',line).strip().split(' %;% ')
	for i in tags:
		stats[i].append(v)
















