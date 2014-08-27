from bs4 import BeautifulSoup
import requests, pandas, pickle



class Blobber(object):
	def __init__(self):
		self.url_log = open('url_log.txt','a')
		self.classifier =  pickle.load(open('classifier.pickle'))

	def extract(self, url, threshold=0.5):
		response = requests.get(url)
		if response.status_code == 200:
			self.html = response.content
		else:
			return self.end()
		return self.extract_from_html(self.html, threshold)

	def extract_from_html(self, html, threshold =0.5):
		self.lines = []
		self.soup = BeautifulSoup(html)
		self.classify_p_tags()

	def classify_p_tags(self):
		p_tags = self.soup.find_all('p')
		for i in p_tags:
			p_tags_features =  features_from_p_tags(i)
			if self.classifier.classify(classifier_features(p_tags_features)):
				self.lines.append(unicode(i.string))
		return " ".join(self.lines)

	def end(self):
		self.url_log.write(url+'\n')
		print "Can't extract HTML from url. Bad Request.."

	def close(self):
		self.url_log.close()



def main(url):
	soup = BeautifulSoup(requests.get(url).content)
	text =[]
	p = soup.find_all('p')
	for v,i in enumerate(p):
		f = features_from_p_tags(i, v, len(p))
		if classifier.classify(classifier_features(f)):
			text.append(unicode(i.string))
		else:
			print 'A'
	return re.sub("\n",,""," ".join(text)) 




class DataSet(object):
	def __init__(self):
		creator = Blobber()	
		self.url_log = open('url_log.txt','a')
		self.log =open('data_set.txt', 'w+')
		self.data = []
		self.sample_size =0
		self.input_size =3
		self.output_size =1

	def create_data(self, url):
		self.url_log.write(url+'\n')
		_ = self.self_learn(url)

		return True

	def end_training(self):
		self.log.seek(0)
		samples = str(self.sample_size) + str(self.input_size) + str(self.output_size)+'\n'
		self.log.write(samples)
		self.log.close() 
		self.df = pandas.DataFrame(self.data)
		self.df.save('data_set.df')
		self.df.to_csv('data_set.csv')
		print "data_set.df contains binary version of dataframe and data_set.csv contains text file"

		return True

	def self_learn(self, url):
		response = requests.get(url)
		if response.status_code ==200:
			self.html = response.content
		else:
			return self.end()

		tb = BeautifulSoup(self.html)
		p_tags = tb.find_all('p')
		total = len(p_tags)
		for v,i in enumerate(p_tags):
			print i
			try:
				ok = input('Is this ok? [1/0]')

				density_value = round(density(i),4)
				length = len(unicode(i))
				percent_pos = round(float(v)/total,4)
				no_tags = count_tags(i)
				attrs = i.attrs
				class_attr = i.attrs['class'] if 'class' in i.attrs else 0		 
				result = {'attrs':attrs,'url': url,'density' : density_value, 'pos' : percent_pos, 'no_tags' : no_tags, 'class': class_attr }
				self.log.write(str(round(density_value, 4))+' '+ str(round(percent_pos,4))+' '+str(no_tags)+'\n')         
				if ok:
					self.log.write(str(1)+'\n')
					result['good/bad'] =1
				else:
					self.log.write(str(0)+ '\n')
					result['good/bad'] =0
				self.data.append(result)
				self.sample_size +=1
			except SyntaxError:
				print "skipping..."


		return False


		print "Can't extract HTML from url. Bad Request.."
	def end(self):


class Classifier(object):
	
	def __init__(self):
		seld.data = pandas.DataFrame.load('data_set.df')


	def featureSet(self):
		input_data = [(features(observation), observation['good/bad']) for observation in self.data]
		a= numpy.random.randint(0, self.data_size, int(data_size*0.8))
		b = list(set(numpy.arange(0,self.data_size,1)) - set(a))
		self.train_set, self.test_set =  [input_data[i] for i in a], [input_data[i] for i in b]


	def NBClassifier(self):
		self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
		self.accuracy = nltk.classify.accuracy(classifier, self.test_set)

	def Decision_tree_classifier(self):
		self.classifier = nltk.DecisionTreeClassifier.train(self.train_set)
		self.accuracy = nltk.classify.accuracy(classifier, self.test_set)

	def MaxentClassifier(self):
		self.classifier = nltk.DecisionTreeClassifier.train(self.train_set)
		self.accuracy = nltk.classify.accuracy(classifier, self.test_set)

	def dump_classifier(self):
		pickle.dump(self.classifier, open('classifier.pickle', 'wb'))
		return True

def classifier_features( observation):
	features = {}
	features['.com/'] = 1 if observation['url'][-5:] == '.com/' else 0
	features['class'] = 1 if observation['class'] else 0
	features['number of tags'] = observation['no_tags']
	features['position on page'] = observation['pos']
	return features


def features_from_p_tags(p_tag, position, total):
	density_value = round(density(p_tag),4)
	percent_pos = round(float(position)/total,4)
	no_tags = count_tags(p_tag)
	class_attr = p_tag.attrs['class'] if 'class' in p_tag.attrs else 0		 
	result = {'url': url,'density' : density_value, 'pos' : percent_pos, 'no_tags' : no_tags, 'class': class_attr }
	return result

def count_tags(tag):
	return sum(1 for i in tag if i.name != None)

def density(tag):
	return float(len(unicode(tag.get_text())+u''))/(len(unicode(tag)))


