Keyword Extraction
==================

This keyword extractor is designed for the purpose of extracting key terms from urls.

Keywords in this code are considered as Noun Phrases. This definition can be relaxed by changing grammar of Regular Expression chunker.
     	
<pre>grammar = '''NE : { &lt;NNP|NNPS&gt;*&lt;DT&gt;?&lt;NNP|NNPS&gt;+}'''</pre>

This indicates that chunker will give chunks corresponding to above parts of speech tags. NE is just a key with which chunker will refer to results.
More abour RegexpChunker can be read from here: http://www.nltk.org/book/ch07.html

 
It involves three broad steps:

1. Text Extraction from urls : This is done using BeautifulSoup in python. Code uses only p tags for this purpose. In order to classify if p tag is useful or not there need to be a classifier which is not used here as of now.

2. Noun Phrase Chunking: Regexp Chunker of nltk does this fairly easily

3. Scoring of Keywords: Keywords are looked at two different positions: title and body. 
 - NPs from title are given weight of sqrt(ngrams) where ngrams is number of words in phrase and sqrt is square root function
 - NPs form body are given weight of math.exp(sqrt(ngrams)) * math.exp(-(position)^0.25), where position is sentence number in which phrase occurs. 										      

	*more words in phrase ==> higher weight because frequency of such phrases goes down*
	
	*if the phrase is appearing later in body, it is given less weight (indicated by higher value of position)*
	
	*exponential function is used so that changes in value is not drastic*

How to use it?
------------
It can be used interactively as well as a service. Given a url, it will give out keywords with their scores
<pre>
{
	'God': 0.341
	'Arthur' :0.234
}


</pre>



