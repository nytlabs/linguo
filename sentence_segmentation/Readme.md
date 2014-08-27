Sentence Segmentation
========

Sentences are segmented via classification problem. All that needs to be done is to classify '.', '?' or '!' as end of a sentence o not.

There are three classifiers that are used for this purpose:
 - Decision Tree Classifier
 - Naive Bayes Classifier
 - Maximum Entropy Classifier

Features of Classifiers are as follows:

1. next-word-capitalized : if next word to any of .?! is capitalized or not
2. prevword : which word is the previous word
3. punct : What punctation is it : ., ? or !
4. prev-word-one-char :  if previous word is one character

*segmentor class initiates a classifier and can then be used continuously to segment sentences.*

*Features can be altered by changing the function punct_features()*

Once the service is running, requests can be made to service using curl.

Submit request:

1. If you want return type to be list of sentences where each sentence is itself a list of words: 

<pre>curl ec2-54-198-18-10.compute-1.amazonaws.com:8888/segment_text_return_listOfwords -d @test6.json -H "Content-Type: application/json"</pre>

2. If you want return type to be just a list of sentences where each sentence is a string:

<pre>curl ec2-54-198-18-10.compute-1.amazonaws.com:8888/segment_text_return_sentences -d @test6.json -H "Content-Type: application/json"</pre>

where test.json looks like this:

{"paragraph":"Former Vice President Dick Cheney told conservative radio host Laura Ingraham that he \"was honored\" to be compared to Darth Vader while in officer. And the sentence goes on..."}

*Note: Double quotes are important and key is not important. You can give any key you want.*

**Result of request will be a JSON**
<pre>
{
	'accuracy': 0.9738
	'Number_of_sentences' : 4
	'sentences':['sentence1', 'sentence2'] # depends on return type
}
</pre>






 






