import gensim, pymongo, logging, sys, re
from pattern.en import parse

'''practice script to run lda on NYT articles'''
## get articles directly from mongoDB
## throw into simple line splitter
## make word2vec of all words
# LSA with/without word2vec  --> Spectral Clustering
# LDA model
# DMR
#
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__) 

class MySentences(object):
	def __init__(self):
		self.data = pymongo.Connection().articles.collection_1
		logger.info('\n\n\n\nIterator ready.\n\n\n\n')
		self.log =open('lda_log.txt', 'w')

	def __iter__(self):
		try:
			for count,i in enumerate(self.data.find({})[: 1100000]):
				try:
					if count % 10000 == 0:
						logger.info('Progress: @ %d article', count)						
					for line in i['metadata']['body'].split('\n'):
						tokens = processNumbers(line.split())
						yield tokens			
				except:
					logger.info('\n\nImproper file encountered. Writing it in log.\n\n')
					self.log.write(str(i)+ '\n\n\n')
					yield []
		finally:
			self.log.close()

def processSentence(sentence):
	tokens = lemmatize(sentence)
	tokens = processNumbers(tokens)
	return tokens

def lemmatize(sentences, allowed_tags = re.compile('(NN|VB|JJ|RB)')):
	tokens =[]
	if not sentences:
		return []	
	
	for sentence in parse(sentences, lemmata = True).split():
		print sentence
		for token,tag,_,_,lemma in sentence:
			print lemma
			if 2<= len(lemma) <= 15 and not lemma.startswith('_'):
				if allowed_tags.match(tag):
					tokens.append(lemma)
	return tokens

def processNumbers(tokens):
	for v, token in enumerate(tokens):
		if re.search(r'\d', token):
			tokens[v] = 'NUM'
	return tokens

def buildW2Vmodel(file_name):
	logger.info('building Word2Vec model using simple split function')
	sentences = MySentences()
	model = gensim.models.Word2Vec()
	logger.info ('\n\n\n\nBuilding Vocabulary...\n\n\n\n')
	model.build_vocab(sentences)
	logger.info('\n\n\n\nLearning NNET parameters...\n\n\n\n')
	model.save(file_name)
	logger.info('\n\n\n\nSuccessfully executed. Model saved as %s in the same folder.\n  Exiting gracefully.\n\n\n\n', file_name)

if __name__ == '__main__':
	buildW2Vmodel('simple_line_split_model')




 
