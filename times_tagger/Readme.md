**Tagger: Tagging articles with Times Tags corresponding to Named Entities**

*Named Entities in any article can be PERSON, ORGANIZATION, FACILITY*

Rules by CatCon Service is in the form of text file, one for each category. This algorithm was coded using 4 rules set named : locations.txt, org_all.txt, persons.txt, porg.txt, topics.txt. For the purpose of POS tagging and handling non-ascii characters all text files were converted to utf-8 before being used. Conversion of files to utf-8 encoding was done by opening and saving file with utf-8 encoding in TextEdit. 

* Canonical Names are names as are used to tag articles. These are decided by taxonomists. 
* Variants of canonical names are as present in rule corresponding in rule sets. Each canonical can be referred to by different names and each time it is a rule is recorded in database mentioning variant and corresponding canoncical

**Algorithm**

- Tag input with Parts of Speech. Named entities are words tagged with proper nouns. Proper nouns are abbreviated as NNP in nltk.
- lookup named entity in dictionary. 

*There are two dictionaries which are used for indexing.* 

a. Reference Dictionary: It stores all tokens and corresponding canonical names.
Example :

'Obama' : ['Barack Obama: The Story (Book)', 'Everyday Icon: Michelle Obama and the Power of Style (Book)', 'Obama, Barack Hussein Sr', 'Obama, Barack'...]

b. Canonical Dictionary: Keys here are canonical names as present in tags.tsv file. Each key then point to a list of lists. 
Example:
'50 Cent' : [[u'Curtis', u'Jackson', u'50', u'Cent', u'Fifty'], [u'', u'Curtis', u'Rapper', u'50', u'Cent', u'Fifty', u'Rap', u'Jackson', u'RFapper'], [], 'nytd_per']

Here 

 - list #1 represents all tokens with which 50 Cent can be referred to. All **variants** are captured in this list.
 
 - list #2 represents all tokens which can be used as **context**. If these words appear in a sentence, it is a good indication that sentence is about 50 Cent. This thing becomes clearer from rule set

 - list #3 represents **topics** in context of which a particular canonical name is related to exclusively.

Example : John Huston is a variant that can refer to two canonical names: Huston, John M (if article is related to Movies) or Huston, John R (if article is related to Golf)
Rule set related to this looks like this:
 John Huston,__COND:"Movies"@"Huston\c John M|nosection::::::http://topics.nytimes.com";"Golf"@"Huston\c John R"
'__COND' is representative of Topics

 - Element #4 in list is a times macro tag. These are macro tags as present in tags.tsv
 
*['nytd_des', 'nytd_geo', 'nytd_org', 'nytd_per', 'nytd_porg', 'nytd_topic', 'nytd_ttl']*

*NOTE: In this service only list#1 is utilized as it is an attempt to capture variants only. Context and Topics are not captures in this service*

**Lookup Algorithm**
Example: 'Barack Obama'
 - Split entity at whitespaces. Here it will be 'Barack', 'Obama'
 - Lookup each token in reference dictionary and collect canonicals from all tokens. [['can1', 'can2', 'can3'] , ['can1', 'can2', 'can3'] ]
 - Once all the options are found. Return intersection of all lists. Here: ['can1','can3'] 


**Setting up Redis Database**

 - Canonical indices are set up in Redis @ db = 9. It is done by running canonical_indices.py from command line. Alternatively one can also set up redis interactively by creating instance of class defined in script

 - Reference Dictionary is first formed in RAM and then set up in Redis Database at db = 8. It is done by running reference_indices.py from command line. Alternatively one can also set up redis interactively by creating instance of class defined in script. 

**Using it as an API**

lookup.py is implemented to be used as an app. It uses Flask Library. 
Once the lookup.py is run through command line. API is ready to accept requests. 

requests need to be POSTed at 

curl http://ec2-54-198-18-10.compute-1.amazonaws.com:80/tagger -d @bigram.json -H "Content-Type:application/json"

where bigram.json looks like this:

{"bigram" : "New Delhi"}


*json files are corresponding dictionaries in text form*
 



