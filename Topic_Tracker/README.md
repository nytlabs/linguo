***TOPIC TRACKER***

**What is it?**

Topic Tracker is aimed at keeping track of what is being read or talked about most in the lab. 
It accepts url links in the form of JSON with "Content-Type: application/json". 
Typical JSON file will look like this:

{"url":"http://www.zephoria.org/thoughts/archives/2014/07/09/alice-goffman-on-the-run.html"}

*NOTE : quotes here should be double quotes or url will not be processed*

**How does it work?**

It uses LDA Model by David Blei implemented in Gensim Library of Python. It is coded in Python 2.7. 

0. User sends in the url through (A) below
1. beanstalk is used to handle queue of urls
2. text is extracted from each url
3. dictionary is formed with text as the urls are being added
4. after first 25 urls LDA Model is trained and stats about number of topics are send to Redis
5. after every 25 urls thereafter stats are computed on accumulated corpus (corpus is just the accumulation of all text) and send to Redis
6. after every 100 urls LDA Model is retrained and stats 
7. On the other end stats can be viewed through (B) below


**How to use it?**

(A) To Submit url links:

 curl ec2-54-198-18-10.compute-1.amazonaws.com:8888/track_topics -d @url.json -H "Content-Type: application/json"

(B) To view Topic Statistics

 http://ec2-54-198-18-10.compute-1.amazonaws.com:8888/topic_tracker
