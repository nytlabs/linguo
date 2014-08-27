from flask import Flask
from flask import request
import json

import sys
sys.path.append('./keyword_extrcation')
sys.path.append('./sentence_segmentation')
sys.path.append('./times_tagger')
import segment_sentence
import key_score
import lookup




def get():
	#expects json. when wrinting a json file, remember to putstring in unicode format
	try:
		print request
	converted_dict = request.get_json()	
	except IndexError:
		print "Format not acceptable..."
	return converted_dict.values()[0]

# final is a dictionary
def getOutput(final):
  if len(final)==0:
    return json.dumps({'result_found' : False, 'results':  {}}), "\n"
  else:
    return json.dumps({'result_found' : True,'results' : final}, indent =4, sort_keys=False) + "\n"


app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
	return "\nNot a good request.\n\nSpecify function name after the address.\nExample: localhost:80/func_name\n\n"

@app.route('/extract_keywords', methods = ['GET','POST'])
def process_request3():
	if request.method == "POST":
		url = get()
		_ = key_extractor.prism(url)
		t = key_extractor.title()
		t = key_extractor.nltk_keys()
		t = key_extractor.scored()
		return getOutput(t)
	else:
		return "Only POST requests are accepted. No text found. Try Again...\n"

@app.route('/segment_text_return_listOfwords', methods=['GET', 'POST'])
def process_request1():
	if request.method == "POST":
		para = get().decode('utf-8', 'ignore')
		return segmentor.segment(para, rtype =0)
	else:
		return "Only POST requests are accepted. No text found. Try Again...\n"

@app.route('/segment_text_return_sentences', methods=['GET', 'POST'])
def process_request2():
	if request.method == "POST":
		para = get().decode('utf-8', 'ignore')
    	return segmentor.segment(para, rtype = 1)
#	else:
#		return "Only POST requests are accepted. No text found. Try Again...\n"


@app.route('/extract_entity', methods=['GET', 'POST'])
def process_request4():
  if request.method == "POST":
    sentence= get().decode('utf-8', 'ignore')
    return entity_extractor.extract(sentence)
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"


if __name__ == '__main__':
	key_extractor = key_score.keyword_extractor()
	segmentor =  segment_sentence.segmentor(1)
	entity_extractor = extractor.entity_Extractor()
	app.debug=True
 	app.run(host='0.0.0.0', port =8888) #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
 