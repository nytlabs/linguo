'''script which was used for processing NYT articles. This was run before generating text.txt'''

from textblob import TextBlob, Word
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from functools32 import lru_cache
from nltk.corpus import wordnet
import re, json, pymongo, logging

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class simpleDocs(object):
	def __init__(self):
		## Lemmatizer with cache
		self.lemmatize = (lru_cache(maxsize = 50000))(WordNetLemmatizer().lemmatize)
		self.exclude = set(stopwords.words('english'))
		self.tag_count = eval(open('count_tags.txt', 'r').read())
		self.tagset = set(self.tag_count.keys())
		self.conn = pymongo.Connection().articles.collection_1
		self.excluded_articles = 0
		logger.info("Instance created.")

	def convertDocs(self, limit = None):
		if not limit:
			useful_ids = eval(open('useful_ids.txt').read())
		else:
			useful_ids = eval(open('useful_ids.txt').read())[: limit]

		logger.info("Writing output")
		with open('/mnt/data/text.txt', 'a') as f, open('/mnt/data/labels.txt', 'a') as l, open('/mnt/data/nyt_ids.txt','a') as h:
			for v, i in enumerate(useful_ids):
				article = self.conn.find({'_id' : int(i)})[0]
				body = article['metadata']['body']
				labels =  article['metadata']['taxonomic_class']
				body, labels = self.clean(body),self.filter_labels(labels)
				if labels and body:
					if v%1000 == 0:
						logger.info('Progress @ %d, Skipped : %d', v, self.excluded_articles)
					#f.write(json.dumps(body).decode('utf-8', 'ignore')+'\n' )
					#l.write(json.dumps(labels).decode('utf-8', 'ignore')+'\n')
					h.write(json.dumps(i).decode('utf-8', 'ignore')+'\n')

				else:
					self.excluded_articles+=1

		logger.info("Excluded_articles : %d", self.excluded_articles)


		## body clean
	def clean(self, body):
		try:
			body = TextBlob(body)
			tags = body.tags
			tags = [(num_or_not(i[0]), pos(i[1])) for i in tags if self.is_word(i[0])] ##store tuples
			words = [self.lemmatize(i, t).lower().decode('utf-8', 'ignore') for i,t in tags if t]
			return " ".join(words)
		except:
			return ""

	def is_word(self, word):
		if len(word) <4 or len(word) > 20:
			return False
		if word in self.exclude:
			return False
		return True

	## process label
	def filter_labels(self, labels):
		labels = [label.lower() for label in labels]
		labels = [label for label in labels if label in self.tagset and self.tag_count[label] > 100]
		return " %;% ".join(labels)





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



if __name__ == '__main__':
	simpleDocs().convertDocs()





