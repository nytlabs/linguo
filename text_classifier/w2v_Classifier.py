from collections import defaultdict
from textblob import TextBlob, Word
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from functools32 import lru_cache
from nltk.corpus import wordnet
from tsne import bh_sne
import re, json, logging, gensim, numpy, scipy, cython, pylab


logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class SetupClassifier(object):

	# load doc_vec only when it is present in the dir
	def __init__(self, load_doc_vec = True):
		self.model = gensim.models.Word2Vec.load('w2v_model.mod')
		self.file_index = json.loads(open('line_indices.txt','r').read())
		self.text_file = open('/mnt/data/text.txt','r')
		self.labels = open('/mnt/data/labels.txt','r').read().split('\n')
		self.training_articles = 1000000
		if load_doc_vec:
			self.load_doc_vec()
		else:
			self.create_trained_doc_vec(self.training_articles)

		self.label_count = defaultdict(int)
		logging.info('model, file_index, text_file and labels are now in RAM')


	# called once in starting. Takes lot of time
	def create_trained_doc_vec(self, training_articles =1000000):
		logging.info('Creating document vector for %d',training_articles,'articles using w2v_model.mod')
		self.doc_vec = numpy.zeros((training_articles,100)) #model has 100 dimensional vectors
		for v,line in enumerate(islice(self.text_file, training_articles)):
			if v%1000 ==0:
				logging.info('Progress @ %d', v)
			words = re.sub('\"','',line).strip().split()
			self.doc_vec[v,] = sum(model[word] for word in words if word in model)

		logging.info('doc_vec.npy saved in the same directory. Object also has doc_vec numpy in the RAM')
		numpy.save('doc_vec.npy')

	def load_doc_vec(self):
		self.doc_vec = numpy.load('doc_vec.npy')
		logging.info('loading doc_vec.npy in RAM')

	def count_labels(self, save = True):
		logging.info('counting number of articles present in each label')
		for i in self.labels:
			labels = re.sub('\"','',i).strip().split(' %;% ')
			for label in labels:
				self.label_count[label] +=1
		loggin.info('labels and their presence in number of articles are now in self.label_count')
		if save:
			self.save_label_count()

	def save_label_count(self):
		logging.info('saving self.label_count in count_tags.txt')
		with open('/mnt/data/count_tags.txt','a') as f:
			f.write(json.dumps(dict(self.label_count)))
		loggin.info('done')

	# memory friendly accessing of lines(i.e articles from text.txt)
	def seekline(self, line_no):
		self.text_file.seek(self.file_index[str(line_no)])
		return self.text_file.readline()

	def get_label_count(self):
		return self.label_count

	def map_label_to_articles(self):
		self.label_article_map = defaultdict(list)
		for v,i in enumerate(self.labels):
			labels = re.sub('\"','',i).strip().split(' %;% ')
			for label in labels:
				self.label_article_map[label].append(v)


class NNClassifier(SetupClassifier):

	def __init__(self, load_doc_vec =True):
		SetupClassifier.__init__(self, load_doc_vec)
		self.lemmatize = (lru_cache(maxsize = 50000))(WordNetLemmatizer().lemmatize)
		self.exclude = set(stopwords.words('english'))
		logging.info('classifier ready')
		self.article = None
		self.doc_vec_norms = numpy.linalg.norm(numpy.asarray(self.doc_vec, dtype = numpy.float32), axis =1)


	def clean_article(self, article):
		self.article = self.clean(article)

	## body clean
	def clean(self, body):
		try:
			body = TextBlob(body)
			tags = body.tags
			tags = [(self.num_or_not(i[0]), self.pos(i[1])) for i in tags if self.is_word(i[0])] ##store tuples
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

	'''keep only those words which are | adjective | verb | noun | adverb |'''
	def pos(self,tag):
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

	def num_or_not(self,token):
		if re.search('[0-9]', token):
			return u'NUM'
		return token

	#article_no translates to line number in the text.txt file
	def article2vec(self, article = None):
		vec = sum(self.model[word] for word in re.sub('\"','',article).strip().split() if word in self.model)
		return vec

	def getLabels(self, labels_index):
		return re.sub('\"','',self.labels[labels_index]).strip().split(' %;% ')
	
	def TopTenDots(self, vec):
		# assumption here is that doc_vec is 1m X 100 and vec is 1 X 100
		if numpy.dot(vec,vec) ==0. :
			logging.info('article vector has 0 norm. words in article might not be representative of learned representaitons.')
			return []
		with numpy.errstate(divide ='ignore'):
			projections = numpy.dot(vec, self.doc_vec.T)/numpy.dot(vec, vec)
			cosine_angles = numpy.where( self.doc_vec_norms !=0., projections/self.doc_vec_norms, -2)
		return numpy.argsort(cosine_angles)[-10:][::-1]

	def TopTenDists(self, vec):
		#  doc_vec is 1m X 100 and vec is 1 X 100
		norms = batch_diff_and_norms(self.doc_vec,vec)
		return numpy.argsort(norms)[:10]

	def BestLabels(self, Topn, threshold, nearest_docs):
		print Topn, threshold, nearest_docs,
		self.info += str(Topn)+ ' '+ str(threshold) + ' '+ str(nearest_docs) +' '
		#self.log.write(' '+str(Topn) + ' '+str(threshold) + ' '+str(nearest_docs))
		predicting_labels = [self.getLabels(i) for i in nearest_docs[:Topn]]
		set_labels = set(reduce(list.__add__, predicting_labels))
		return set([ i for i in set_labels if prob(i, predicting_labels) >= threshold ])

	def BestLabelsProbability(self, Topn,nearest_docs):
		predicting_labels =  [self.getLabels(i) for i in nearest_docs[:Topn]]
		set_labels = set(reduce(list.__add__,predicting_labels))
		probability = defaultdict(float)
		for label in set_labels:
			probability[label] = prob(label, predicting_labels)
		return probability

	def TopCombined(self, vec, Topn):
		near = numpy.concatenate((self.TopTenDots(vec)[:Topn],self.TopTenDists(vec)[:Topn]), axis = 1)
		return near

	def classify(self, article_text, formatted = False ,dots=True, Topn =5, threshold=0.5, ret_prob = True, combined = False):
		if not formatted:
			self.clean_article(article_text)
		else:
			self.article = article_text

		article_vec = self.article2vec(self.article)

		if self.article and dots and not combined:
			nearest_docs = self.TopTenDots(article_vec)
		elif self.article and not dots and not combined:
			nearest_docs = self.TopTenDists(article_vec)
		elif self.article and combined:
			nearest_docs = self.TopCombined(article_vec, Topn)
		else:
			logging.info('can\'t predict, string is empty. error might be because of stringtype')
			self.end()
			return set([])
		if ret_prob:
			labelset = self.BestLabelsProbability(Topn, nearest_docs)
		else:
			labelset = self.BestLabels(Topn,threshold, nearest_docs)

		return labelset

	def end(self):
		logging.info('Classification not done. Check text article for encoding and format')

	def article_tsne(self, sample_size, pca = False):
		samples = numpy.random.randint(0,1000000,sample_size )
		self.doc_2d = bh_sne(self.doc_vec[samples , ], pca_d = pca)

class TestNNClassifier(NNClassifier):

	def __init__(self):
		NNClassifier.__init__(self)
		self.doc_2d_learned=False


	def test(self,dot=True, sample_size =10000, Topn =5,formatted = False,threshold =0.5, combined = False):
		#self.log.write('Smaple_size : '+' Topn '+  str(Topn) + ' threshold: '+ str(threshold)+' Dot Products = ' + str(dot) + '\n')
		logging.info('Sample_Size : %d, Topn: %d, threshold: %f, Dot_Products = %r', sample_size, Topn, threshold, dot)
		dots = True if dot else False	
		self.total_hd =0.0
		sample  = numpy.random.randint(1000000,1320399,sample_size)
		for v,i in enumerate(sample):
			print i,
			#self.log.write(str(i))
			self.info =str(i)+' '
			article = self.seekline(i)
			tag_labelset = self.classify(article, formatted = formatted, dots = dots, Topn =Topn, threshold =threshold, ret_prob = False, combined = combined)
			actual_labels = set(self.getLabels(i))
			
			hd = HammingDistance(actual_labels, tag_labelset)
			#print i, actual_labels, tag_labelset, hd
			print hd
			self.info += str(hd) +'\n'
			#self.log.write(' ' + str(hd)+'\n')
			self.total_hd += hd
			#self.log.write(self.info)
			if v%5 == 0:
				#self.log.write('Progress @' + str(v) +'Total Hamming Distance = ' + str(self.total_hd))
				logging.info('Progress @ %d, Total Hamming Distance = %f, ',v, self.total_hd)
				#print '@%d',v,' hd = %f\n',hd ,'Actual Labels = %s\n', actual_labels, 'tag_labelset =%s\n', tag_labelset)
		return self.total_hd/ sample_size

	def AUC(self,dot =True, sample_size=100, Topn = 5, formatted = False, start_threshold = 0,threshold_step = 0.1, end_threshold =1, combined = False , save = False):
		hd = []
		steps = numpy.arange(start_threshold, end_threshold,  threshold_step)
		for threshold in steps:
			self.log.write('Progress @ threshold = ' + str(threshold)+'\n')
			logging.info('Progress @ threshold = %f', threshold)
			if threshold ==1:
				hd.append(0)
			else:
				hd.append(self.test(dot, sample_size, Topn, formatted,threshold, combined))

		result = {'Top N Articles':Topn,'steps':steps, 'hd': hd}
		if save:
			f = open('/mnt/data/obs/hd_threshold_'+str(Topn)+'_'+str(sample_size),'w')
			f.write(json.dumps(result))
			f.close()
		return result

	def DecideTopn(self, dot =True, sample_size=100, formatted = False, combined = False):
		self.all_hd =[]
		if combined:
			candidate_topn = [1,2,3,4]
		else:
			candidate_topn = [1,2,3,4,5,6,7,8,9]
		for Topn in candidate_topn:
			result = {'Topn' :Topn , 'result': self.AUC(dot, sample_size= sample_size,Topn=Topn,formatted = formatted, combined = combined ,save= False)}
			self.all_hd.append(result)

		with open('All_Topn.txt_'+str(sample_size)+'_'+str(dot)+'_C'+str(combined),'w') as f:		
			f.write(str(self.all_hd))

	def Decide_dot_dist(self):
		self.log = open('/mnt/data/obs/log.txt','w')
		sample_size = [100]
		for i in sample_size:
			self.log.write('\n\n--SAMPLE SIZE--\n\n'+ str(i)+'\n\n')
			logging.info('\n\n--SAMPLE SIZE--\n\n %d', i)
			self.DecideTopn(dot = False, sample_size = i, formatted = False, combined = True)
			#self.DecideTopn(dot = False, sample_size = i, formatted = False, combined = False)
			self.DecideTopn(dot = True, sample_size = i, formatted = False, combined = False)
		self.log.close()


	def test_dist(self, Topn=5, threshold =0.5, sample_size =10000):
		return self.test(dot =False, Topn =5, threshold =0.5, sample_size =10000)

	def AUC_dist(self, start_threshold =0, threshold_step =0.1, end_threshold =1, Topn=5):
		return self.AUC(dot =False,start_threshold =0, threshold_step =0.1, end_threshold =1, Topn=5 )

	def article_tsne_plot(self, sample_size = 200000):
		self.article_tsne(sample_size)
		self.tag_2d_learned = True
		font = { 'fontname':'Tahoma', 'fontsize':0.5, 'verticalalignment': 'top', 'horizontalalignment':'center' }
		pylab.subplots_adjust(bottom =0.1)
		pylab.scatter(self.doc_2d[:,0], self.doc_2d[:,1], marker = '.' ,cmap = pylab.get_cmap('Spectral'))
		pylab.title('NYT Tagged Articles (1991-2007)')
		pylab.xlabel('X')	
		pylab.ylabel('Y')
		pylab.savefig('/mnt/data/article_plot', bbox_inches ='tight', dpi = 1000, orientation = 'landscape', papertype = 'a0')
		pylab.close()

	## Combination of dist and dot >> TO DO
	def test_dot_dist(self):
		pass

	def random_guess(self):
		labels = self.labels
		tag_counts = json.load(open('tag_counts.txt'))
		keys = tag_counts.keys()
		total = len(labels)
		values = [i/float(total) for i in tag_counts.values()]
		total_hd =0
		for i in range(100000):
			guess = [keys[v] for v,i in enumerate(keys) if numpy.random.binomial(1,values[v])==1]
			article = numpy.random.randint(len(labels))
			try:
				guess = set(reduce(list.__add__, [ re.sub('\"', '', i).strip().split(' %;% ') for i in guess]))
			except:
				guess = set([])
			article = set(labels[article].strip().split(' %;% '))
			hd = HammingDistance(guess, article)
			total_hd += hd
		average = total_hd/100
		return average

class ClusterClassifier(TestNNClassifier):

	def __init__(self, load =True):
		TestNNClassifier.__init__(self)
		self.tag_2d_learned=False
		try:
			if load:
				self.tag_vec = numpy.load('tag_vec.npy')
				self.tag_vec_mean = numpy.load('tag_vec_mean.npy')
		except:
			logging.info('tag_vec.npy can not be loaded, classifier can not work without tag_vec matrix')

		self.tags =[]

	def cluster_tags(self):
		self.map_label_to_articles()
		logging.info('Map from label to articles created.')
		self.number_of_labels = len(self.label_article_map)
		self.tag_vec = numpy.zeros((self.number_of_labels, 100))
		self.tag_vec_mean = numpy.zeros((self.number_of_labels, 100))

		for label_index,(label,doc_ids) in enumerate(self.label_article_map.iteritems()):
			if label_index % 200 == 0:
				logging.info('Progress @ label index %d' ,label_index )
			self.tag_vec[label_index,] = sum(self.doc_vec[doc_id,] for doc_id in doc_ids if doc_id <1000000)
			self.tag_vec_mean[label_index, ] = self.tag_vec[label_index, ]/ len(doc_ids) 
			self.tags.append(label) ## indexing of labels
		
		logging.info('saving tag vectors in tag_vec.npy and tag_vec_mean.npy')
		numpy.save('tag_vec.npy', self.tag_vec)
		numpy.save('tag_vec_mean.npy', self.tag_vec_mean)
		return self.tag_vec

	def classify(self, article, formatted=False, radius = 0.5):
		if not formatted:
			self.clean_article(article_text)
		else:
			self.article = article_text	
		article_vec = self.article2vec(self.article)
		tags = self.BestTags(article_vec)

		## TO DO probability related to tags
		return tags 

	def BestTags(self, vec):
		diff =  (tag_vec - article_vec)
		norms = [numpy.sqrt(numpy.dot(i,i)) for i in diff]
		predict =[]
		for v,i in enumerate(norms):
			if i < radius:
				predict.append(self.tags[v])
		return predict

	def tag_tsne(self):
		self.tag_2d = bh_sne(self.tag_vec)
		self.tag_2d_learned = True

	def tag_tsne_plot(self, label_plot = False):
		if not self.tag_2d_learned:
			self.tag_tsne()
		logging.info('plotting results')
		font = { 'fontname':'Tahoma', 'fontsize':0.5, 'verticalalignment': 'top', 'horizontalalignment':'center' }
		pylab.subplots_adjust(bottom =0.1)
		pylab.scatter(self.tag_2d[:,0], self.tag_2d[:,1], marker = '.' ,cmap = pylab.get_cmap('Spectral'))
		pylab.title('NYT Tagged Article Labels(1991-2007)')
		pylab.xlabel('X')
		pylab.ylabel('Y')
		if label_plot:
			logging.info('Adding text to plot')
			for label, x, y in zip(self.tags, self.tag_2d[:, 0], self.tag_2d[:, 1]):
				pylab.annotate(
					label, 
						xy = (x, y), xytext = None,
						ha = 'right', va = 'bottom', **font)
		else:
			pass

		pylab.savefig('/mnt/data/tag_plott', bbox_inches ='tight', dpi = 1000, orientation = 'landscape', papertype = 'a0')
		pylab.close()

	def tag_article_tsne_plot(self, sample_size = 20000):
		samples = numpy.random.randint(0,1000000,sample_size )
		self.combined_matrix = numpy.concatenate((self.doc_vec[samples, ],self.tag_vec), axis =0)
		self.combined_2d = bh_sne(self.combined_matrix)

		font = { 'fontname':'Tahoma', 'fontsize':0.1, 'verticalalignment': 'top', 'horizontalalignment':'center' }
		pylab.subplots_adjust(bottom =0.1)
		pylab.scatter(self.combined_2d[:sample_size+1,0], self.combined_2d[:sample_size+1,1], marker = '.' ,cmap = pylab.get_cmap('Spectral'))
		pylab.scatter(self.combined_2d[sample_size+1:,0], self.combined_2d[sample_size+1:,1], marker ='x' , cmap =pylab.get_cmap('Spectral'))
		pylab.title('NYT Articles and Labels(1991-2007)')
		pylab.xlabel('X')	
		pylab.ylabel('Y')
		for label, x, y in zip(self.tags, self.combined_2d[sample_size+1:, 0], self.combined_2d[sample_size+1:, 1]):
			    pylab.annotate(
			        label, 
			        xy = (x, y), xytext = None,
			        ha = 'right', va = 'bottom', **font)
			        #,textcoords = 'offset points',bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
			        #arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))		

		pylab.savefig('/mnt/data/tag_article_plot', bbox_inches ='tight', dpi = 1000, orientation = 'landscape', papertype = 'a0')
		pylab.close()

## TO DO
class TestClusterClassifier(ClusterClassifier):

	def __init__(self):
		ClusterClassifier.__init__(self)




def batch_diff_and_norms(big_mat, vec, batch_size =3000):
	n = big_mat.shape[0]
	d2 = numpy.empty(n)
	for start in range(0, n, batch_size):
		end = min(start + batch_size, n)
		c2 = big_mat[start:end] - vec
		d2[start:end] = numpy.linalg.norm(c2, axis=1)
	return d2


def HammingDistance(set1, set2):
	return float(len(set1 & set2))/float(len(set1 | set2))

def prob(label, labels):
	count =0
	for i in labels:
		if label in i:
			count +=1	
	return float(count)/float(len(labels))



def main():
	test = TestNNClassifier()
	print test.test()












