from flask import Flask
from flask import request
import w2v_Classifier

def get():
	#expects json. when wrinting a json file, remember to putstring in unicode format
	try:
		print request
		converted_dict = request.get_json()	
	except IndexError:
		print "Format not acceptable..."
	return converted_dict.values()[0]


app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
	return "\nNot a good request.\n\nSpecify function name after the address.\nExample: localhost:80/func_name\n\n"


@app.route('/classify', methods=['GET', 'POST'])
def process_request():
  if request.method == "POST":
    text= get().decode('utf-8', 'ignore')
    return json.dumps({'labels': classifier.classify(text, formatted = False ,dots=True, Topn =6, threshold=0.5, ret_prob = True, combined = False)})
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"



if __name__ == '__main__':
	# this will take 2.5 GB of memory spacee
	classifier = w2v_Classifier.NNClassifier()
	app.debug=True
 	app.run(host='0.0.0.0', port =8888) #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug

