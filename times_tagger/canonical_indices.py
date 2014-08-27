import re, json, string, progressbar, codecs
import ujson as json
from collections import defaultdict


class build_dictionary(object):

	def __init__(self, file_name, tag):
		self.file_name, self.tag = file_name, tag
		self.super_dictionary = defaultdict(list)

	def dictionary(self):
		iterators = lineGenerator(self.file_name)
		count = max(enumerate(open(self.file_name)))[0]
		try:
			for i in xrange(count):
				self.insert(iterators.next())
		except StopIteration:
			pass

		return self.super_dictionary

 	#index line's variant against canonicals
	def insert(self, x):
		if re.findall("__TG" , x):
			self.insertWithContext(x)
		elif re.findall("__COND", x):
			self.insertWithTopic(x)
		else:
			self.insertSimple(x)

	def insertWithContext(self, x):
		canonical, context, topic, variant = extractWithContext(x)
		self.insertRule(canonical, context, topic, variant)

	def insertWithTopic(self,x):
		canonicals, context, topics, variant = extractWithTopic(x)
		for i,canonical in enumerate(canonicals):
			self.insertRule(canonical, context, [topics[i]], variant)

	def insertSimple(self, x):
		canonical,  context, topic, variant = extractWithContext(x)
		self.insertRule(canonical, context, topic, variant)

	def insertRule(self, canonical, context, topic, variant):
		#print canonical
		variant = re.split('\W+', variant)
		if canonical not in self.super_dictionary :
			self.super_dictionary[canonical] = [ variant, context, topic, self.tag ]
		else:
			C = self.super_dictionary[canonical]
			self.super_dictionary[canonical] = [ list( set(C[0]) | set(variant) ), list( set(C[1]).union(set(context)) ), list( set(C[2]).union(set(topic))), self.tag  ]

# _____________________________________________________________________________________________________

def lineGenerator(file_name):
	for line in codecs.open(file_name, 'r', encoding='utf-8'):
		yield line


def extractWithContext(line):
	context_start, context_end  = re.search("__TG[^:]*:{\([^,]*", line), re.search("\)}:",line)
	if  not context_start:
		variant, line = line[ : line.find(',') ], line[ (line.find(",")+1) : ]
		canonical = processCanonical( line[ : line.find('|')], switch = 1 )
		return canonical, [], [], variant
	else:
		context = line[context_start.end() : context_end.start()]
		context = re.sub(r'(\([^,]*,)|(\))',"", context )
		context= [j for i in context.split(",") for j in i.replace("\"","").split(" ")]
		canonical = processCanonical(line[ (line.find(')}:')+3) : line.find('|') ] , switch =2)
		return canonical, context, [],  line[ : line.find(',__') ]

def processCanonical(canonical, switch):
	#pattern_stripCanonical = "\(.*\)"
	canonical= re.sub(r'\\c', ',', canonical).replace(r'&#0038;',"&")
	if switch == 1 or switch == 2: # Normal or context
		canonical = canonical.strip()
	else: # With topics
		canonical, pattern = canonical.replace("\"",""), re.compile(r'(\|)|($)')
		canonical = canonical[: pattern.search(canonical).start()].strip()
	return canonical

def extractWithTopic(line):
	variant, line = line[ : line.find(',__') ], line[re.search(',__COND:', line).end() +1 :]
	topic, canonical, i, pattern = [], [], 0, re.compile(r'(\";)|($)')
	j, line, pos= line[  : pattern.search(line).end()+1], line[ pattern.search(line).end()+2 : ], 1
	while pos:
		tc= processTopicCanonicalPair(j)
		topic, canonical, pos = topic + [tc[0]], canonical + [tc[1]], pattern.search(line).end()
		j, line, i = line[ : pos+1] , line[pos+2 : ], i+1
	return canonical, [],  topic, variant

def processTopicCanonicalPair(pair):
	pair = pair.split("@")
	t,c = pair[0].replace("\"" , "") , processCanonical(pair[1], switch =3)
	return t,c


def combineDictionaries(list_of_dictionaries):
	super_dictionary={}
	for d in list_of_dictionaries:
		for k,v in d.iteritems():
			super_dictionary[k] = v
	return super_dictionary

# _____________________________________________________________________________________________________

def main():
	print "\nBuilding dictionaries..."

	bar = progressbar.ProgressBar(maxval=100, \
	widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
	bar.start()
	locations = build_dictionary("./ruleSet/locations-utf8.txt", "nytd_geo").dictionary()
	bar.update(20)
	topics = build_dictionary("./ruleSet/topics-utf8.txt", "nytd_topic").dictionary()
	bar.update(40)
	orgs = build_dictionary("./ruleSet/org_all-utf8.txt", "nytd_org").dictionary()
	bar.update(60)
	porg = build_dictionary("./ruleSet/porg-utf8.txt", "nytd_porg").dictionary()
	bar.update(80)
	persons = build_dictionary("./ruleSet/persons-utf8.txt", "nytd_per").dictionary()
	bar.finish()
	print "Dictionaries ready to combine..."

	d1, d2, d3, d4, d5 = set(porg.keys()), set(locations.keys()), set(topics.keys()), set(orgs.keys()),  set(persons.keys()),
	intersections = [d1==d2, d1==d3, d1==d4, d1==d5, d2==d3, d2==d4, d2==d5,d3==d4,d3==d5,d4==d5]
	list_of_dictionaries = [porg, locations, topics, orgs, persons]

	if True not in intersections:
		print "No duplicate keys found in dictionaries...\nCombining dictionaries...\n"
		super_dictionary = combineDictionaries(list_of_dictionaries)
		print "Variant/Context/Topics dictionary created.\n"
	else:
		print "Dictionaries have duplicate keys. Please check your data or modify the code."

	return super_dictionary
# _____________________________________________________________________________________________________

if __name__=='__main__':
	SD = main()
	#SD = build_dictionary("locations.txt", "nytd_geo").dictionary()
	f= open('./super_dictionary.json', 'w+')
	str_json = json.dumps(SD, ensure_ascii= False)
	f.write(str_json)
	f.close()

	print "Writing to redis..."

	#canonical_dictionary 
	import redis
	r=redis.StrictRedis(host='localhost', port =6379, db=9)
	for i,j in SD.iteritems():
		r.set(i,j)

	print "Data written to redis."

