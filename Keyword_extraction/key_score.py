from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.corpus import stopwords
import operator
import segment_sentence as ss
import nltk, math, requests, re


import sys
sys.path.append('./usefulScripts/')
import usefulText

class keyword_extractor(object):

	def __init__(self):
		self.segmentor = ss.segmentor(1)
		grammar = '''NE : {<NNP|NNPS>*<DT>?<NNP|NNPS>+}
						 '''
		self.chunker = nltk.RegexpParser(grammar)

		self.phrases = None
		months = ['January','Jan.', 'February','Feb.','March','Mar.', 'April','Apr.', 'May', 'June', 'July','August', 'Aug.',\
		 'Spetember','Sept.','October','Oct.', 'November','Nov.','December','Dec.' ]
		days = ['Sunday', 'Sun.', 'Tuesday', 'Tu.', 'Tue.', 'Tues.', 'Thursday','Th.', 'Thurs.', 'Thur.', 'Thu.', 'Monday',\
		'Mon.', 'Wednesday','Wed.', 'Friday','Fri.', 'Saturday','Sat.']
		self.exclude = set(stopwords.words('english') + months+ days)
		self.stopwords = stopwords.words('english') + ['A' ,'An']

		self.HTMLTextBlobber = usefulText.HTMLTextBlob()

	def prism(self, url, low_threshold =0.5, up_threshold =1):
		response = requests.get(url)
		if response.status_code == 200:
			html = response.content
		else:
			return self.end()
		## Scope of improvement
		#self.text = #self.HTMLTextBlobber.extract_from_html(html, low_threshold, up_threshold).decode('utf-8', 'ignore') 
		self.soup = BeautifulSoup(html)
		self.text = " ".join([unicode(i.string) for i in self.soup.find_all('p') if i.string != None])#self.HTMLTextBlobber.extract_from_html(html, low_threshold, up_threshold).decode('utf-8', 'ignore')  ## Scope of improvement


	def title(self):
		text = self.soup.title.string
		text = text[:text.find('|')]
		nps = self.chunker.parse(nltk.pos_tag(nltk.word_tokenize(text)))
		self.phrases = extractNE(nps)
		return self.phrases

	def nltk_keys(self):
		sentences =  self.segmentor.segment(self.text, 0)['sentences'][:-5] #ignore last five because of improper extraction
		sentences =[sentence for sentence in sentences if isProper(sentence)]
		self.sentences = sentences

		### POS tagging: Keep Nouns
		### Chunking of POS tagged: Keep NNP+
		tagged = [nltk.pos_tag(sentence) for sentence in sentences]
		trees = [self.chunker.parse(i) for i in tagged]
		chunked = [extractNE(tree) for tree in trees]
		chunked = [(i,no+1) for no,ls in enumerate(chunked) for i in ls]
		chunked = [i for i in chunked if self.filtered(i[0])]
		chunked = strip_stops(chunked,self.stopwords)
		self.chunked = [i for i in chunked if i[0].count(' ') <4]
		return self.chunked

	def filtered(self, term):
		if not re.search('[a-zA-Z0-9]+', term):
			return False
		if re.search('(PM|AM)', term):
			return False
		#if re.search('\w+[A-Z]+', term):
		#	return False
		if re.search('[^a-zA-Z0-9- .]', term):
			return False
		if len(term)<3:
			return False
		if term in self.exclude:
			return False
		return True

	def scored(self):
		d = defaultdict(float)
		## normal text
		for i, no in self.chunked:
			d[i] += score(i,no) ### frequency taken into account by successively adding

		## title	
		if self.phrases:
			for i in self.phrases:
				d[i] +=fn1(i.count(' '))	
		##normalization
		d =  dict(d) 
		total = sum(d.values())
		for i in d:
			d[i] = d[i]/total
		return sorted(d.iteritems(), key = operator.itemgetter(1))[::-1]

	def end(self):
		print "Can't access the url. Bad Request."

def isProper(sentence):
	if len(sentence) <=5:
		return False

	if '|' in sentence:
		return False
	return True
	## add some more

def extractNE(tree):
	ne =[]
	for i in tree:
		try:
			i.node
		except AttributeError:
			pass
		else:
			ne.extend([" ".join( [ j[0] for j in i.leaves() ] ) ])
	return ne

def score(term, no):
	ngrams = term.count(' ')
	return math.exp(fn1(ngrams)) * math.exp(-fn2(no))

### ngrams
def fn1(x):
	return math.pow(x,0.5)

### sentence sequence
def fn2(x):
	return math.pow(x,1/4)


def strip_stops(terms, stopwords):
	for term, no in terms:
		tokens = term.split()
		if tokens[0].lower() in stopwords:
			term = " ".join(tokens[1:])
	return terms


'''
## run
reload(key_score)
url ='http://www.foxnews.com/politics/2014/07/27/chairmen-house-senate-veterans-affairs-committees-reach-tentative-agreement-on/'
import key_score as k
j= k.keyword_extractor()
_ =j.prism(url)
t = j.title()
n = j.nltk_keys()
s = j.scored()
'''


# (\w*[a-z][A-Z][a-z]\w*)
#\w+[A-Z]+
#(?!^)\b([A-Z]\w+) to match words with cap letters in between