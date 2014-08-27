import d3py, pandas, numpy, redis, json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/end1', methods =['GET'])
def send_fake():
	stats = [{'count': 0.4},{'count': 0.7},{'count': 0.6}]
	#stats = [1,2,3]
	return stats

if __name__ == "__main__":
	r = redis.StrictRedis(host ='localhost', port = 6379, db= 5)
	app.debug =True
	app.run(host ='0.0.0.0', port = 80)

