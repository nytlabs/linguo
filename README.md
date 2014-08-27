linguo
======

![linguo robot](http://4.bp.blogspot.com/_W2b7qR0wkBs/SdPz9CyWMOI/AAAAAAAAANo/M0znxgvTURI/s320/linguo1.jpg)

linguo is a set of services that provide NLP facilities

This repository contains various tools that one might encounter while dealing with text data. These are also provided in shape of services.

There are 6 services two of which are not implemented as a service but can be done via python's Flask Library.

1. times_tagger : This folder contains scripts to tag articles with times tags. More information is inside the folder.

2. sentence_segmentation : Scripts in this folder are aimed at providing web service to identify sentences from a body of text. It is not an easy task to identify sentences as there are instances where periods are not used as end of a sentence.

3. keyword_extraction : Scripts in this folder are aimed at extraction of keywords from urls.

4. topic_tracker : It is an attempt to summarize topics that are being read by an individual or a group of people.
 
5. text_classifier : It is an attempt to classify text into labels as give in Times taxonomy. Multi-Label Classification is done by using Google's Word2Vec representation of word as 100 dimensional vectors.

6.  html_text_extractor : Given an url, it contains massive amount of text but not all text contains core information (about which the page is). This is an attempt to build a classifier on p tags in html to classify if its good or bad.

After talking to people, I found that there are libraries like goose(https://github.com/grangier/python-goose) and reporter(https://pypi.python.org/pypi/reporter/0.1.2) that does exact same thing so I recommend use of those libraries.

7. usefulScripts : It contains all the scripts which were helpful in preprocessing articles, querying mongoDB or experimenting with LDA. 

*app.py script combines all the services. It might not work because of relocation of other scripts.*
