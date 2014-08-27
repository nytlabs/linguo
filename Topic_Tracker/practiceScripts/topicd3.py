import numpy, redis, json
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/data',methods =['GET','POST'])
def send_stats():
	stats = eval(r.get('stats'))
	return stats

@app.route('/end1', methods =['GET','OPTIONS'])
def send_fake():
	stats = [{'prob': 0.4,'words': ['word', 'kill']},{'prob': 0.7,'words': ['jim', 'bob']},{'prob': 0.6, 'words': ['hill', 'valley']}]
	#stats = [1,2,3]
	return json.dumps(stats)


@app.route('/topic_tracker',methods =['GET'] )
def send_java():
	return render_template('stats.html', title = 'Topic Tracker')



if __name__ == "__main__":
	r = redis.StrictRedis(host ='localhost', port = 6379, db= 5)
	app.debug =True
	app.run(host ='127.0.0.0', port = 8888)




