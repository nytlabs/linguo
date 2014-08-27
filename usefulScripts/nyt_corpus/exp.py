import pymongo, nltk
from collections import defaultdict

p= pymongo.Connection().articles.collection_1
corpus_pointer =p.find() # cursor object

import sys
sys.path.append('../version0.0/')
import segment_sentence as ss

text= l[0]['metadata']['body']
segmentor= ss.segmentor(1) # train by decision tree classifier
sentences = eval(segmentor.segment(text, rtype =0))['sentences']

corpus = defaultdict(list)

## Query
l=[]
for i in p.find():
	try: 
		if set(['ACQUIRED IMMUNE\nDEFICIENCY SYNDROME (AIDS)', 'ACQUIRED IMMUNE', 'ACORN STAKES (HORSE RACE)', 'ADDENDA']).intersection(set(i['metadata']['indexing_service']['classifier'])):
			l.append({'id': i['_id'],'year': i['metadata']['date']['year'], 'day_of_month': i['metadata']['date']['day_of_month'],\
				'month' : i['metadata']['date']['month']} )
			
	except:
		pass

## Getting tags
f= open('tags.txt', 'r')
f.readline()
f.readline()
tags = set([])
for i in f:
	tags.add(i.strip())

tags2 =set([i.lower() for i in tags])

## Query
from collections import defaultdict
count = defaultdict(int)
no_common, no_class, classs =0,0,0
for i in p.find():
	try:
		clsfr = i['metadata']['taxonomic_class']
		clsfr = [it.lower() for it in clsfr]
		common = tags2.intersection(set(clsfr))
		if common:
			for it in common:
				count[it]+=1
		else:
			no_common +=1
		classs +=1
	except:
		no_class +=1
j=0
for i,v in dict(count).iteritems():
	j+=v

## v<100 1975;  v<50 1588; v<10 734; v<5 455; v<3 273; v==1 153; v>800 409 v> 500 526
## v>= 400 607 v>=200 881

c=0
for i,v in dict(count).iteritems():
	if v >=200:
		c+=1
