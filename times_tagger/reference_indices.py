import string, re
import ujson as json
import numpy as np
from nltk.corpus import stopwords
from collections import defaultdict

class build_Mdictionary(object):

  def __init__(self, file_name, super_dictionary_name):
    self.file_name, self.super_dictionary_name = file_name, super_dictionary_name
    self.Mdict, self.uniqueTags, self.super_dictionary= defaultdict(list), [],  {}
    self.super_dictionary= json.load(open(self.super_dictionary_name,"r"))

  def createMultiDict(self):
    print "Modifying the Master Dictionary with entries in Super Dictionary..."
    temp_d = self.MD_modified_by_SD()
    print "Appending the new entries in Super Dictionary to Multi Dictionary..."
    self.SD_appended_to_MD(temp_d)
    return self.Mdict, self.uniqueTags

  # indexing canonical names with their tokens (words in canonical) from tags.tsv file
  def MD_modified_by_SD(self):
    count, iterators = max(enumerate(open(self.file_name)))[0], lineGenerator(self.file_name)
    trans, temp_d = string.maketrans('\n', '\t'), {}# because there are \n characters on each line

    try:
      for i in xrange(count):
        line = string.translate(iterators.next(), trans).split('\t')[:-1]
        if line[1] in self.super_dictionary:
         lookup = self.super_dictionary[line[1]] 
        else:
          lookup = [re.split('\W+', line[1]),[],[], line[0]]
          self.super_dictionary[line[1]] = lookup
        temp_d[line[1]] = ""
        line_words = list( set(re.split('\W+', line[1])) | set(lookup[0]) )
        if line[0] not in self.uniqueTags:
          self.uniqueTags = self.uniqueTags +[line[0]]
        for c in line_words:
          self.Mdict[c].append(line[1])

    except StopIteration:
      pass

    return temp_d

  # there are entries in rule sets which are not present in tags.tsv file
  # this might be because I was given only 4 files
  def SD_appended_to_MD(self, temp_d):
    for k,v in self.super_dictionary.iteritems():
      if k not in temp_d:
        for c in v[0]:
          self.Mdict[c].append(k)

# _____________________________________________________________________________________________________

def lineGenerator(file_name):
  for line in open(file_name):
    yield line

# _____________________________________________________________________________________________________


if __name__=="__main__" :
  e = build_Mdictionary("tags.tsv", "super_dictionary.json")
  Mdict, uniqueTags = e.createMultiDict()
  f= open('./master_dictionary.json', 'w+')
  json.dump(Mdict,f, ensure_ascii= False)

  print "Multi-dictionary dumped to master_dictionary.json in the same directory."
  print "Writing to redis..."
  
  # Reference dictionary
  import redis
  r= redis.StrictRedis(host='localhost', port= 6379, db=8)
  for i,j in Mdict.iteritems():
    r.set(i,j)

  #update canonical dictionary
  r = redis.StrictRedis(host = 'localhost', port = 6379, db =9)
  for i,j in e.super_dictionary.iteritems():
    if not r.exists(i):
      r.set(i,j)

  print "DONE"
