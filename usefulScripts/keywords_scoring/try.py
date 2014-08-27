url = 'http://www.cnn.com/2014/07/19/world/europe/ukraine-malaysia-airlines-crash/'

## fetch html
import requests
r=  requests.get(url)
html = r.content

##nltk: fetch text by cleaning html
import nltk
text = nltk.clean_html(html)

##fetch text based on density :useful text
import usefulText as u
text = u.extract_text(html)


## unicode 
text = text.decode('utf-8','ignore')

## segment into sentences
import sys
sys.path.append('../version0.0/')
import segment_sentence as ss


def isProper(sentence):
	if len(sentence) <=5:
		return False

	if '|' in sentence:
		return False
	return True
	## add some more

segmentor = ss.segmentor(1)
sentences= eval(segmentor.segment(text, 0))['sentences'][:-5]
sentences =[sentence for sentence in sentences if isProper(sentence)] 

#### textblob
from textblob import TextBlob
tb = TextBlob(text)
np = tb.noun_phrases
n_counts = {}
for n in np:
	if all(len([ch for ch in word if ch.isalpha()]) > 2 for word in n.split()):
		n_counts[n] = n_counts.get(n, 0) +1
sorted_n = sorted(n_counts.iteritems(), key=lambda n: -n_counts[n])[:10]



### POS tagging: Keep Nouns
### Chunking of POS tagged: Keep NNP+
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
tagged = [nltk.pos_tag(sentence) for sentence in sentences]
grammar = '''NE : {<NNP|NNPS>*<DT>?<NNP|NNPS>+}
				 '''
chunker = nltk.RegexpParser(grammar)
trees = [chunker.parse(i) for i in tagged]
chunked = [extractNE(tree) for tree in trees]
chunked = [i for ls in chunked for i in ls]
fd = nltk.FreqDist(chunked)
chunks = fd.keys()

for i,v in fd.iteritems():
	if 

## Filter through difference in wording
import difflib
collapsed_words = [re.sub(' ', '', i) for i in chunks]
for v,string in enumerate(collapsed_words):
	for other_str in collapsed_words[v+1:]:
		diff = difflib.ndiff(string, other_str)
		diff_score = sum([1 for i in diff if re.search('[-+]', i)])
		#print diff_score, other_str, string
		if diff_score < 4:
			index = collapsed_words.index(other_str)
			collapsed_words.pop(index), chunks.pop(index) 

return chunks  # it contatins keywords extracted via above methodology
keywords.append(chunks)


### extract terms using topia
from topia.termextract import extract
extractor = extract.TermExtractor()
sentences = eval(segmentor.segment(text,1))['sentences'][:-5]
terms = sorted(extractor(" ".join(sentences)))
terms = [i for i in terms if filtered(i[0])]

def filtered(term):
	if not re.search('[a-zA-Z]+', term):
		return False
	if re.search('(PM|AM)', term):
		return False
	if isVerb(term):
		return False
	return True

keyowrds.append(terms[:5])

##Filter through frequency
fd = nltk.FreqDist(words)
total = sum([fd[i] for i in fd])
freq = [fd[i]/total for i in fd]

##bigrams and trigrams
tokens = nltk.word_tokenize(text)
bgm = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens)
scored = finder.score_ngrams(bgm.likelihood_ratio)

from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = BigramCollocationFinder.from_words([i for sentence in sentences for i in sentence])
fdr = [BigramCollocationFinder.from_words(sentence) for sentence in sentences]
ngrams = [fdr1.nbest(bigram_measures.pmi, 5) for fdr1 in fdr]
fdr = nltk.FreqDist([i for n in ngrams for i in n])
fdr.max()
good_sentences, stopwords=[], nltk.corpus.stopwords.words('english')
for sentence in sentences:
	good_sentence=[]
	for token in sentence:
		if token.lower() not in stopwords and 3<= len(token) <= 21:
			good_sentence.append(token)

	good_sentences.append(good_sentence)

fdr_filtered = [BigramCollocationFinder.from_words(sentence) for sentence in good_sentences]
fdr_filtered.apply_word_filter(filt1)
def filt1(x):
	if re.search('[(Fri)|((Sat)ur)|(Sun)|(Mon)|(Wed)|(Tues)|(Thurs)]?(day)', x):
		return True
ngrams = [fdr1.nbest(bigram_measures.jaccard, 1) for fdr1 in fdr_filtered]
# pmi, likelihood_ratio, jaccard, poisson_stirling

fdr_filtered = nltk.FreqDist([i for n in ngrams for i in n])
fdr_filtered._cumulative_frequencies()

keywords.append([i for i in fdr_filtered[:3]])

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = BigramCollocationFinder.from_words([i for sentence in sentences for i in sentence])
fdr = [BigramCollocationFinder.from_words(sentence) for sentence in sentences]
ngrams = [fdr1.nbest(bigram_measures.pmi, 5) for fdr1 in fdr]
fdr = nltk.FreqDist([i for n in ngrams for i in n])
fdr.max()



for sentence in sentences:
			good_sentence=[]
			for sentence_no, token in enumerate(sentence):
				if token.lower() not in self.exclude and self.no_below <= len(token) <= self.no_above: #note all punctuations will be removed in the length constraint
					good_sentence.append(token)



finder.nbest(bigram_measures.pmi, 10)
def filter_ngrams(x):
	if re.search('[a-zA-Z]', x):
		return True

finder.apply_word_filter(filter_ngrams)
finder.nbest(bigram_measures.pmi, 10)


print scored

## readability
import pprint
printp =pprint.PrettyPrinter()
printp.pprint(text)


## Pattern
from pattern.web import URL, plaintext
url = URL(url, method = GET)
text = url.download()
simple_text = plaintext(text, indetation = True)







#### Scoring:

scored = finder.score_ngrams( bigram_measures.likelihood_ratio  )
 
# Group bigrams by first word in bigram.                                        
prefix_keys = collections.defaultdict(list)
for key, scores in scored:
   prefix_keys[key[0]].append((key[1], scores))

good  = [i for sentence in tagged for i in sentence if filtered_tags(i)]

def filtered_tags((term, tag)):
	if re.search('NN(P|S)', tag) and len(term) > 3:
		return True
	return False
good_fd  = nltk.FreqDist(good)


### Works good!!!!!!
keywords = []
for i in good_fd:
	try:
		second = getSecond(i[0])
		if second:
			keywords.append(" ".join( [ i[0], second ] ))
	except:
		pass

def getSecond(term):
	index = 0
	while 1:
		second = prefix_keys[term][index][0]
		if len(second) >3 or second not in exclude or re.search('[A-Za-z]', second):
			return second
		else:
			index +=1
			if index == len(prefix_keys[term])-1:
				return False











