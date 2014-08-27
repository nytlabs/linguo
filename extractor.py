from flask import request
from flask import Flask
from nltk.corpus import stopwords
import string, json, itertools, ast
import nltk
from collections import defaultdict
import redis

import sys
sys.path.append('./SetRedis/')
import sentence_manipulation as SM

# Will give an error if Mdictionary does not have keys in super_dicitonary_name file # ne: Named Entity
# _____________________________________________OBJECT________________________________________________________

class entity_Extractor(object):

  def __init__(self):
    self.ref_dictionary = redis.StrictRedis(host='localhost', port =6379, db=3)
    self.canonical_dictionary = redis.StrictRedis(host='localhost', port=6379, db=2)
    print "Ready to serve..."
    
  def extract(self, sentence):
    index, final, NE, output = 0, [], extractNE(sentence, withClass = False), defaultdict(dict)

    for x,i in enumerate(NE):
      times_tags, not_found = self.lookup(i)
      add_new_variant, tag_found, add_new_tag =0, 0, 0

      if times_tags and not_found==[]:
        tag_found =1
      elif not_found and times_tags == []:
        add_new_tag = 1
      elif not_found and times_tags:
        tag_found, add_new_variant =1,1
      elif not_found==[] and times_tags ==[]:
        add_new_tag =1

      output[str(x)]={"Entity": i, "new_variant" : not_found, "add_new_variant": add_new_variant, "tag_found": tag_found,\
      "Times Tag" : times_tags, "add_new_tag" : add_new_tag}
   
    return getOutput(output)

  def lookup(self, NE):
    parts, index, options_list, NotInDictionary = NE.split(), 0, [], []
    while index < len(parts):
      if self.ref_dictionary.exists(parts[index]):
        options_list.append( eval(self.ref_dictionary.get(parts[index])))        
      else:
        NotInDictionary.append( parts[index] )
      index = index +1

    return self.getCommon(options_list), NotInDictionary

  def getCommon(self, options_lists):
    canonical_names_set = [set(sub_list) for sub_list in options_lists]
    try:
      common_canonical = set.intersection(*canonical_names_set)
    except:
      common_canonical = set([])
    return self.format(common_canonical)

  def format(self, options):
    formatted_options = []
    for i in options:
      formatted_options.append({"Name": i, "Tag": eval(self.canonical_dictionary.get(i))[3] })
    return formatted_options

# ____________________________________________FUNCTIONS_________________________________________________________

def extractNE(sentence, withClass):
  words = nltk.word_tokenize(sentence)# Extract words from sentence: Stopwords removed, punctuations removed
  if withClass:
    tree = nltk.ne_chunk(nltk.pos_tag(words), binary = False)
    return extractNEwithClass(tree)
  else:
    tree = nltk.ne_chunk(nltk.pos_tag(words), binary = True)
    return extractNEwithoutClass(tree)

def extractNEwithoutClass(tree):
  ne =[]
  for i in tree:
    try:
      i.node
    except AttributeError:
      pass
    else:
      ne.extend([" ".join( [ j[0] for j in i.leaves() ] ) ])
  return ne

def extractNEwithClass(tree):
    ne = defaultdict(list)
    for i in tree:
      try:
        i.node
      except AttributeError:
        pass
      else:
        ne[i.node].append( " ".join( [ j[0] for j in i.leaves() ] ) ) 
    return dict(ne)

def extractall(s):
  return extractNE(nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(s))))

def doall(s):
  return nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(s)))

def stanNER():
  st = NERTagger('/Users/206268/Projects/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz','/Users/206268/Projects/stanford-ner/stanford-ner-3.4.jar')
  answer = st(s.split()) # s is an ASCII coded string

def getSentence():
  #expects json. when wrinting a json file, remember to putstring in unicode format
  try:
    converted_dict= request.get_json()	
  except IndexError:
    print "Format not acceptable..."
  return converted_dict.values()[0]

def getOutput(final):
  if len(final)==0:
    return json.dumps({'Result' : "Entities not found", 'Search Results':  {}}), "\n"
  else:
    return json.dumps({'Result' : "Entities found",'Search Results' : final}, indent =4, sort_keys=False) + "\n"

# ______________________________________________APPLICATION_______________________________________________________

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
  return "\nNot a good request.\n\nSpecify function name after the address.\nExample: localhost:80/func_name\n\n"

@app.route('/extract_entity', methods=['GET', 'POST'])
def process_request():
  if request.method == "POST":
    sentence= getSentence()
    return obj.extract(sentence)
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"

# ___________________________________________________MAIN_______________________________________________________

if __name__ == "__main__":
  obj = entity_Extractor()
  app.debug=True
  app.run(host='0.0.0.0', port =80) #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
