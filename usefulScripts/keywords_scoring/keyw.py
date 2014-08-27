import requests, usefulText # directory shoud be same

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


class keyword_extractor(object):

	def __init__(self, url):
		r= requests.get()
		html = r.content
		self.text = usefulText.extract_text(html).decode('utf-8', 'ignore')  ## Scope of improvement
		self.segmentor = ss.segmentor(1)


	def nltk_keys(self):
		sentences= eval(self.segmentor.segment(self.text, 0))['sentences'][:-5] #ignore last five because of improper extraction
		sentences =[sentence for sentence in sentences if isProper(sentence)]

		### POS tagging: Keep Nouns
		### Chunking of POS tagged: Keep NNP+
		tagged = [nltk.pos_tag(sentence) for sentence in sentences]
		grammar = '''NE : {<NNP|NNPS>*<DT>?<NNP|NNPS>+}
						 '''
		chunker = nltk.RegexpParser(grammar)
		trees = [chunker.parse(i) for i in tagged]
		chunked = [extractNE(tree) for tree in trees]
		chunked = [i for ls in chunked for i in ls]
		fd = nltk.FreqDist(chunked)
		chunks = fd.keys()


	def filter_by_diff_string(self):
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

	def topia(self):
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

		return terms

	def bg_tg_nltk(self):
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

		return fdr_filtered.keys()

	def textblob(self):
		#### textblob
		from textblob import TextBlob
		tb = TextBlob(text)
		np = tb.noun_phrases
		n_counts = {}
		for n in np:
			if all(len([ch for ch in word if ch.isalpha()]) > 2 for word in n.split()):
				n_counts[n] = n_counts.get(n, 0) +1
		sorted_n = sorted(n_counts.iteritems(), key=lambda n: -n_counts[n])[:10]

	def scoring(self):





	def svm_keywords(self):







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



