import pymongo, nltk, re, logging
from collections import defaultdict
from gensim import corpora, models
from nltk.stem.wordnet import WordNetLemmatizer


import sys
sys.path.append('../version0.0/')
import segment_sentence as SS

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class Corpora(object):
	def __init__(self,  mongo_Cursor, doc2bow = False, iterator_limit=None, filtered =None, exclude=None ,no_below =4, no_above = 21, sentence_segmentor_algorithm = 1):
		self.no_below, self.no_above = no_below, no_above
		if exclude==None:
			self.exclude = nltk.corpus.stopwords.words('english') # exclude these words
		self.corpus_cursor = [None, mongo_Cursor][isinstance(mongo_Cursor, pymongo.cursor.Cursor)]
		if self.corpus_cursor == None:
			raise TypeError('Wrong object passed. No Cursor to MongoDB found. Reinitialize.')

		#self.segmentor = SS.segmentor(sentence_segmentor_algorithm)
		if filtered:
			self.filtered = filtered
		else:
			self.filtered = self.DEFAULTFILTER

		self.iterator_limit = [iterator_limit, self.corpus_cursor.count()][iterator_limit == None]
		self.doc2bow = doc2bow
		self.lemmatizer = WordNetLemmatizer()

	def __iter__(self):
		'''To iterate through articles one by one; Use it as a Generator'''
		for no, i in enumerate(self.corpus_cursor[:self.iterator_limit]):
			body = i['metadata']['body']
			if no%100000 == 0:
				logger.info("Progress @ %d", no)
			if self.doc2bow:
				yield dictionary.doc2bow(self.process(body))
			else:
				yield self.process(body)

	def reset(self):
		self.corpus_cursor.rewind()

	def process(self, doc):
		doc=  doc.decode('utf-8','ignore')
		doc = nltk.WordPunctTokenizer().tokenize(doc.strip())
		doc = [self.lemmatizer.lemmatize(token.lower(), 'n') for token in doc if self.filtered(token)]
		return doc

	def DEFAULTFILTER(self, token):
		if len(token)< 4 or len(token) > 21:
			return False
		if token.lower() in self.exclude:
			return False
		if not re.search('[a-zA-Z]', token):
			return False
		return True

	def getSegmentor(self):
		''' Give back the sentence classifier'''
		return self.segmentor


	def insertInMongo(self, limit= None):
		'''Inserts the articles in mongoDB in Database = 'articles' and collection = 'processed_articles' '''
		self.corpora_cursor = pymongo.Connection().articles.processed_articles
		for an_article in self.corpus_cursor:
			identity, article = self.processArticle(an_article)
			self.corpora_cursor.insert({'_id' : identity, 'sentences':article, 'tags':an_article['metadata']['indexing_service']['classifier'] })

	def getCursor_to_processedArticles(self, limit = None):
		'''Return a cursor to preprocessed articles'''
		try:
			return [self.corpora_cursor.find()[:limit], self.corpora_cursor.find()][limit == None]
		except:
			raise ExecutionError('Call Object.insertInMongo() first to initiate the cursor attribute of Copora class')

	def processArticle(self, article):
		metadata = article['metadata']
		sentences = eval(self.segmentor.segment(metdata['body'], rtype =0))['sentences']
		return article['_id'], getRepTokens(sentences)


	def getRepTokens(self, sentences):
		for sentence in sentences:
			good_sentence=[]
			for sentence_no, token in enumerate(sentence):
				if token.lower() not in self.exclude and self.no_below <= len(token) <= self.no_above: #note all punctuations will be removed in the length constraint
					good_sentence.append(token)

		return processed_article.append(good_sentence)



def main():
	p = pymongo.Connection().articles.collection_1
	cpo = Corpora(mongo_Cursor = p.find(), iterator_limit = 1000000, doc2bow= False)
	'''for i in cpo:
		print i # prints list of tokens in each article'''
		# reset cpo before	

	logger.info("\n\n\n\nBuilding dictionary...\n\n\n\n")
	try: 
		dictionary = corpora.Dictionary(i for i in cpo)
	except KeyboardInterrupt:
		once_ids = [token for token, freq in dictionary.dfs.iteritems() if freq ==1]
		dictionary.filter_tokens(once_ids)
		dictionary.compactify()
		logger.info("\n\n\n\nSaving to id2word.dict\n\n\n\n")
		dictionary.save('id2word.dict')
		logger.info("\n\n\n\nSaved.\n\n\n\n")


	# remove those which appears once
	once_ids = [token for token, freq in dictionary.dfs.iteritems() if freq ==1]
	dictionary.filter_tokens(once_ids)
	dictionary.compactify()

	logger.info("\n\n\n\nSaving to id2word.dict\n\n\n\n")
	dictionary.save('id2word.dict')
	logger.info("\n\n\n\nSaved.\n\n\n\n")

	cpo.reset()

	logger.info("\n\n\n\nBuilding corpus matrix...\n\n\n\n")
	corpus = [dictionary.doc2bow(text) for text in cpo]
	logger.info("\n\n\n\nCorpus complete.\n\n\n\n")


	copora.MmCorpus.serialize('corpus.mm', corpus)

def main2():
	id2word = gensim.corpora.Dictionary.load_from_text('id2word.txt')
	mm = gensim.corpora.MmCorpus('corpus.mm')

	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100) 
	lsi = gensim.models.lsimodel.LsiModel(corpus = mm, id2word = id2word, num_topics = 100)

	lsi.save('model.lsi')
	lsi = models.LsiModel.load('model.lsi')

	## ---- train lda on tfidf ----
	lda =  gensim.models.ldamodel.LdaModel(corpus =mm , id2word = id2word, num_topics = 100, update_every =1, chunksize =10000, passes =1)

	## ---- prediction on new topic -----
	#doc_lda = lda[new_doc]





