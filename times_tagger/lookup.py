from flask import request
from flask import Flask
from nltk.corpus import stopwords
import string, json, itertools, ast
import nltk
from collections import defaultdict
import redis

# _____________________________________________OBJECT________________________________________________________

class entity_Extractor(object):

  def __init__(self):
    self.ref_dictionary = redis.StrictRedis(host='localhost', port =6379, db=8)
    self.canonical_dictionary = redis.StrictRedis(host='localhost', port=6379, db=9)
    grammar = '''NE : {<NNP|NNPS>*<DT>?<NNP|NNPS>+}
             '''
    self.chunker = nltk.RegexpParser(grammar) 
    print "Ready to serve..."
    
  def extract(self, sentence):
    NE = extractNE(sentence, withClass = True)
    index, final, output = 0, [], []

    if len(NE)>=1:
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

        output.append({"position": x ,"entity": i, "new_variant" : not_found, "add_new_variant": add_new_variant, "tag_found": tag_found,\
        "times_tags" : times_tags, "add_new_tag" : add_new_tag})
     
      return getOutput(output)

    else:
      return getOutput([])

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
      #print type(str(i))
      #print self.canonical_dictionary.get(str(i))
      try:
        formatted_options.append({"name": i, "tag": eval(self.canonical_dictionary.get( str(i) ))[3] })
      except:
        print "Canonical %s not found in canonical dictionary...", i
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
    except:
      if i[1] in ['NNP','NNPS']:
        ne.extend(i[0])
    else:
      ne.extend([" ".join( [ j[0] for j in i.leaves() ] ) ])
  return ne

def extractNEwithClass(tree):
  ne = defaultdict(list)
  for i in tree:
    try:
      i.node
    except:
      if i[1] in ['NNP','NNPS']:
        ne['noun_phrase_leave'].append(i[0])
    else:
      ne[i.node].append( " ".join( [ j[0] for j in i.leaves() ] ) ) 
  return [i for key,value in dict(ne).iteritems() for i in value]

def getSentence():
  #expects json. when wrinting a json file, remember to putstring in unicode format
  try:
    converted_dict= request.get_json()	
  except IndexError:
    print "Format not acceptable..."
  return converted_dict.values()[0]

def getOutput(final):
  if len(final)==0:
    return json.dumps({'results_found' : False, 'search_results':  final}, indent = 4)
  else:
    return json.dumps({'results_found' : True,'search_results' : final}, indent =4, sort_keys=False)

# ______________________________________________APPLICATION_______________________________________________________

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def display_message():
  return "\nNot a good request.\n\nSpecify function name after the address.\nExample: localhost:80/func_name\n\n"

@app.route('/tagger', methods=['GET', 'POST'])
def process_request():
  if request.method == "POST":
    sentence= getSentence()
    return obj.extract(sentence) +"\n"
  else:
    return "Only POST requests are accepted. No text found. Try Again...\n"

# ___________________________________________________MAIN_______________________________________________________

if __name__ == "__main__":
  obj = entity_Extractor()
  app.debug=True
  app.run(host='0.0.0.0', port =80) #, use_reloader= False) # Without app.reloader it will run twice. and it will not debug
  # app.run(debug=True)
