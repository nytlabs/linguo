from collections import defaultdict
import redis, logging, os, json , ujson
from lxml import etree


logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

class getInfo(object):

	def __init__(self, dir_path):
		self.path= dir_path
		logger.info("Storing data in redis simultaneously @db = 4")

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
		root = etree.parse(open(file_path, "r"))
		Body = getBody(root)
		open('/mnt/data/nyt/articles_txt/'+news_no+'.txt', 'w').write(ujson.dumps(Body, ensure_ascii = False))
		json.dump(getDictionary(root, Body), open('/mnt/data/nyt/articles_json/'+news_no+'.json', 'w'))
		
def getDictionary(root, Body):
	return {'heading' : getHeading(root), 'date' : getDate(root), 'body' : Body, \
	'OnlineSections' : getOnlineSections(root), 'indexing_service': getIndexingSections(root) }
 
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


def getOnlineSections(root):
	return handleException(root.xpath('/nitf/head/meta[@name="online_sections"]/@content'))

def getIndexingSections(root):
	node, d = root.findall('./head/docdata/identified-content/'), defaultdict(list)
	for i in node:
		if "indexing_service" in i.attrib['class']:
			d[i.tag].append(i.findtext('.'))
	return dict(d)


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
	dir_path = "/mnt/data/nyt/nyt_data/"
	getInfo(dir_path).enterInfo()
	logger.info('Executed gracefully.')
