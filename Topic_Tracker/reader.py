from textblob import TextBlob, Word
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from functools32 import lru_cache
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
import gensim, requests, redis, re
import logging, beanstalkc, operator

import sys
sys.path.append('../usefulScripts')
import usefulText

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class TopicTracker(object):
	
	def __init__(self, num_topics= 4):
		self.dictionary = gensim.corpora.Dictionary()
		self.lemmatize = (lru_cache(maxsize = 50000))(WordNetLemmatizer().lemmatize)
		self.exclude = set(stopwords.words('english'))
		self.num_topics = num_topics
		self.HTMLTextBlobber = usefulText.HTMLTextBlob()
		self.formatted_text = []
		self.corpus =[]
		self.url_counter =0
		self.redis = redis.StrictRedis(host='localhost', port =6379, db=5)
		logging.info('Tracker initiated...')
		self.log = open('log.txt','a')	
	
	def update_lda(self):
		logging.info('Reseting parameters of LDA. Learning model again...')
		self.lda = gensim.models.ldamodel.LdaModel(self.corpus,id2word= self.dictionary, num_topics =self.num_topics)
		self.send_stats()

	def send_stats(self):
		probs = self.lda[self.corpus]
		self.stats = defaultdict(float)
		for article_stats in probs:
			for topic_no, prob in article_stats:
				self.stats[topic_no] += prob

		total = sum(self.stats.values())
		for i in self.stats:
			self.stats[i] = self.stats[i]/total
		logging.info('Sending Statistics to Redis')
		self.stats = dict(self.stats)
		self.update_redis()

	def update_redis(self):
		logging.info('updating redis...')
		self.redis.set('stats', self.getResults())


 	def getResults(self):
 		logging.info('sending results to redis')
 		self.words()
 		self.results = []
 		for (key,value) in self.stats.iteritems():
 			self.results.append({'prob': value, 'words': self.topic_words[key]})
 		
 		return self.results.sort(key = operator.itemgetter('prob'))

	def words(self):
		self.topic_words= defaultdict(list)
		for i in range(0, self.num_topics):
 			temp = self.lda.show_topic(i, 10)
 			for term in temp:
 				self.topic_words[i].append(term[1])
 		return self.topic_words


	def add_to_corpus(self, url):
		try:
			response = requests.get(url, timeout =1)
			if response.status_code == 200:
				html = response.content
				logging.info('adding to corpus')		
				self.url_counter +=1
				body = getText(html)
				#print len(body)
				text = self.clean(body)
				#print text
				self.formatted_text.append(text)
				logging.info('Adding url_content to corpus %d', self.url_counter)
				self.dictionary.add_documents([text])
				#print self.dictionary
				self.corpus.append(self.dictionary.doc2bow(text))
				#print self.corpus
			else:
				self.log.write(url +'\n')
		except:
			logging.info('Bad URL: %s',url)
			return

	## body clean
	def clean(self, body):
		try:
			body = TextBlob(body)
			tags = body.tags
			tags = [(num_or_not(i[0]), pos(i[1])) for i in tags if self.is_word(i[0])] ##store tuples
			#.decode('utf-8', 'ignore')
			words = [self.lemmatize(i, t).lower() for i,t in tags if t]
			return words
		except:
			return ""

	def is_word(self, word):
		if len(word) <4 or len(word) > 20:
			return False
		if word in self.exclude:
			return False
		return True

'''keep only those words which are | adjective | verb | noun | adverb |'''
def pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def num_or_not(token):
	if re.search('[0-9]', token):
		return u'NUM'
	return token

def getText(html):
	soup = BeautifulSoup(html)
	return " ".join([unicode(i.string) for i in soup.find_all('p') if i.string !=None])


def tracker():
	topic_tracker = TopicTracker(num_topics = 20)
	count = 0
	while True:
		logging.info("getting job")
		job = beanstalk.reserve()
		logging.info("job found")
		url = job.body
		logging.info('url : %s', url)
		count +=1
		lda = 0
		if count % 100 == 0  or (count %25 ==0 and not lda):
			topic_tracker.update_lda()
			lda =1
		if count % 25 ==0 and lda:
			topic_tracker.send_stats()
		topic_tracker.add_to_corpus(url)
		job.delete()

		
if __name__== '__main__':
	r = redis.StrictRedis(host ='localhost', port = 6379, db= 5)
	beanstalk = beanstalkc.Connection()
	logging.info('Reseting tracker...')
	tracker()	





