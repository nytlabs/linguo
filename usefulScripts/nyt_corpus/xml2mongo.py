'''script to store NYT Articles in mongoDB'''

from collections import defaultdict
import logging, os, pymongo
import ujson as json
from lxml import etree

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class getInfo(object):

	def __init__(self, dir_path):
		self.path, self.index_fields = dir_path, set([])
		logger.info("Storing metadata of articles in mongodb @database = articles @collection = collection_1")
		#conn = pymongo.Connection
		self.data = pymongo.Connection().articles.collection_1
		self.improper = open('improper_files.log', 'w')
	
	def enterInfo(self):
		count = 1
		for year in os.listdir(self.path):
			if year != '.DS_Store':
				for month in os.listdir(self.path + year + '/'):
					if month != '.DS_Store':
						for day in os.listdir(self.path + year + '/' + month + '/'):
							if day != '.DS_Store':
								for news in os.listdir(self.path + year + '/' + month + '/' + day + '/'):
									if news != '.DS_Store':
										self.addXML(self.path + year + '/' + month + '/' + day + '/' + news , news[:-4])
										count  = count + 1
									if count % 10000 ==0:
										logger.info(" PROGRESS : @ %d " , count)

		return True

	def addXML(self, file_path, news_no):
		if self.data.find_one({'_id' :int(news_no) }):
			return
		try:
			root = etree.parse(open(file_path, "r"))			
			self.data.insert({'_id' : int(news_no), 'metadata': self.getDictionary(root) } )
		except: #except any error
			logger.info("Improper XML found. @file_path: %s ", file_path)
			self.improper.write( file_path + '\n')

	def getDictionary(self, root):
		index_cat = getIndexingSections(root)
		self.index_fields = self.index_fields |  set(index_cat.keys()) 
		return  {'heading' : getHeading(root), 'date' : getDate(root), 'body' :getBody(root), \
		'OnlineSections' : getOnlineSections(root), 'indexing_service': index_cat, 'taxonomic_class' : getTaxonomicClassifier(root) }
	

def getDate(root):
	try:
		date = int(handleException(root.xpath('/nitf/head/meta[@name="publication_day_of_month"]/@content')))
	except TypeError:
		date = ''

	try:
		month = int(handleException(root.xpath('/nitf/head/meta[@name="publication_month"]/@content')))
	except TypeError:
		month = ''

	try:
		year = int(handleException(root.xpath('/nitf/head/meta[@name="publication_year"]/@content')))
	except TypeError:
		year = ''

	day = handleException(root.xpath('/nitf/head/meta[@name="publication_day_of_week"]/@content'))

	return {"day_of_month" : date, "month": month, "year" : year, "day" : day}

def getBody(root):
	text_iter, body = root.findall('./body/body.content/block[@class="full_text"]/p'), ""
	for text in text_iter:
		body  = body + "\n " + text.findtext('.')
	return body

def getWriter(root):
	pass

def getEditor(root):
	pass

def getOnlineSections(root):
	return handleException(root.xpath('/nitf/head/meta[@name="online_sections"]/@content'))

def getIndexingSections(root):
	node, d = root.findall('./head/docdata/identified-content/'), defaultdict(list)
	for i in node:
		if "indexing_service" in i.attrib['class']:
			d[i.tag.replace('.', '(%dot%)')].append(i.findtext('.'))
	return dict(d)

def getTaxonomicClassifier(root):
	root = root.getroot()
	try: 
		tags,tag =  root.xpath('//classifier[@class = "online_producer" and @type = "general_descriptor"]'), []
		for i in tags:
			tag.append(i.text)
		return tag
	except:
		return []

def getHeading(root):
	try:
		x= root.findall('./body[1]/body.head/hedline/hl1')[0].findtext('.')
	except IndexError:
		x= None
	return x

def handleException(y):
	try:
		return y[0]
	except IndexError:
		return None


if __name__ =='__main__':
	dir_path = "/mnt/data/nyt_data/"
	obj = getInfo(dir_path)
	obj.enterInfo()

	logger.info('Executed gracefully.Writing data information in mongodb_article_info.txt file in nyt_corpus_unzip folder')

	with open('mongodb_article_info.txt', 'w') as f:
		f.write(json.dumps({'database': 'articles', 'collection':  'collection_1'}))

	with open('index_fileds.txt' ,'w') as f:
		f.write(str(obj.index_fields))

	obj.improper.close()
