import nltk
import json
from collections import defaultdict
from flask import request
from flask import Flask

'''
###	 Algorithm
### 1 : Decision Tree Classifier
### 2 : Naive Bayes Classifier
### 3 : Maximum Entropy Classifier
'''


class segmentor(object):

	def __init__(self, algorithm = 1):
		self.classifier, self.accuracy = getClassifier(algorithm)
		
	def segment(self, para, rtype):
		self.para, self.rtype = para.strip(), rtype
		words = getWords_and_punct(self.para)
		start,sents = 0,[]
		for i, word in enumerate(words):
			if word in '.?!' and i!=(len(words)-1) and self.classifier.classify(punct_features(words,i)) == True:
				sents.append(words[start: i+1])
				start = i+1
		if start < len(words):
			sents.append(words[start:])
		return self.getOutput(sents)

	def getOutput(self, sents):
		output = defaultdict(list)
		output["accuracy"] = self.accuracy
		output["Number_of_sentences"] = len(sents)
		output['sentences'] =  [sent for sent in sents] if not self.rtype else [self.getSentence(sent) for sent in sents]
		return dict(output)
		#return json.dumps(dict(output), indent =4, sort_keys=False) +"\n"

	def getSentence(self, x):
		chars_in_x =0
		for i in x:
			chars_in_x = chars_in_x + len(i)
		counter = chars_in_x
		while len( self.para[:counter+1].replace(" ", "") ) < chars_in_x: 
			counter = counter + 1

		sent = self.para[ : counter+1]
		self.para =  self.para[counter+1 : ]
		return sent

def getWords_and_punct(para):
	return	nltk.WordPunctTokenizer().tokenize(para)

def punct_features(tokens, i):
		return {'next-word-capitalized': tokens[i+1][0].isupper(),
				'prevword' : tokens[i-1].lower(), # last three words increased the naive bayes classifier performance from 92% to 96%
				# but has no effect on Decsion tree classifier
				'punct' : tokens[i],
				'prev-word-is-one-char' : len(tokens[i-1]) == 1}

def getTrain_and_Test_set():
	sents, tokens, boundaries, offset = nltk.corpus.treebank_raw.sents(), [], set(), 0

	for sent in sents:
		tokens.extend(sent)
		offset+= len(sent)
		boundaries.add(offset -1)

	featuresets = [(punct_features(tokens,i), (i in boundaries)) for i in range(1,len(tokens) -1) if tokens[i] in '.?!']
	size = int(len(featuresets) * 0.1)
	train_set, test_set = featuresets[size:], featuresets[:size]
	return train_set, test_set

def getClassifier(algorithm):
	train_set, test_set = getTrain_and_Test_set()
	if algorithm ==1:
		classifier = nltk.DecisionTreeClassifier.train(train_set)
		return classifier, nltk.classify.accuracy(classifier, test_set)
	elif algorithm ==2:
		classifier = nltk.NaiveBayesClassifier.train(train_set)
		return classifier, nltk.classify.accuracy(classifier, test_set)
	else:
		classifier = nltk.MaxentClassifier.train(train_set, algorithm ='megam', trace =0)
		return classifier, nltk.classify.accuracy(classifier, test_set)

def getPara():
  #expects json. when wrinting a json file, remember to putstring in unicode format
  try:
    converted_dict= request.get_json()	
  except IndexError:
    print "Format not acceptable..."
  return converted_dict.values()[0] # No need to worry about key name...Make sure first value passed in json is sentence/para, etc.

app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
	return "\nNot a good request.\n\nSpecify function name after the address.\nExample: localhost:80/func_name\n\n"

@app.route('/segment_text_return_listOfwords', methods=['GET', 'POST'])
def process_request1():
	if request.method == "POST":
		para = getPara()
		return obj.segment(para, rtype =0)
	else:
		return "Only POST requests are accepted. No text found. Try Again...\n"

@app.route('/segment_text_return_sentences', methods=['GET', 'POST'])
def process_request2():
	if request.method == "POST":
		para = getPara()
    		return obj.segment(para, rtype = 1)

#_-_-_-_-_-_-_-_-_-_-_-_-#_-_-_-_-_-_-_-_-_-_-_-_-#_-_-_-_-_-_-_-_-_-_-_-_-#_-_-_-_-_-_-_-_-_-_-_-_-#_-_-_-_-_-_-_-_-_-_-_-_-

if __name__ == "__main__":
  obj = segmentor()
  app.debug=True
  app.run(host='0.0.0.0', port =8888) #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
