import beanstalkc
from flask import Flask
from flask import request
import numpy, redis, json
from flask import Flask, render_template
import logging

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def get():
	#expects json. when wrinting a json file, remember to putstring in unicode format
	try:
#		print request
		converted_dict = request.get_json()	
	except IndexError:
		print "Format not acceptable..."
#	print converted_dict.values()
	return converted_dict.values()[0]

app = Flask(__name__)
@app.route('/track_topics', methods = ['POST', 'GET'])
def store():
	if request.method == "POST":
		url = get()
#		print url
		beanstalk.put(str(url))
		return ""
	else:
		return ""

@app.route('/data',methods =['GET','POST'])
def send_stats():
	logging.info('getting stats from Redis')
	stats = eval(r.get('stats'))
	#print stats
	return json.dumps(stats)


@app.route('/topic_tracker',methods =['GET'] )
def send_java():
	logging.info('sending response with html')
	return render_template('stats.html', title = 'Topic Tracker')



if __name__ == "__main__":
	beanstalk = beanstalkc.Connection()
	r = redis.StrictRedis(host ='localhost', port = 6379, db= 5)		
	app.debug =True
	app.run(host ='0.0.0.0', port = 8888)