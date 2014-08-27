function Map(){
	//find indexing services list in the database
	var tags = this.metadata.indexing_service.classifier;

	if (tags == null){
		return;
	} 

	for (var i =0; i < tags.length; i++){
		emit(tags[i], {count : 1});
	}

}

function Reduce(key, values){
	var total = 0;
	for (var i= 0; i< values.length; i++){
		total += values[i].count;
	}

	return {count: total};
}


function Map2(){
	var body = this.metadata.body;

	if (body ==null){
		return;
	}

	emit(Integer.toString(body.length), {count : 1})
}

function Reduce2(key, values){
	var total = 0;
	for(var i =0; i< values.length; i++){
		total += values[i].count;
	}
	return {count: total}
}

// To run the query in python
from bson.code import Code
p=pymongo.Connection().articles.collection_1

map = Code(open('map1.js', 'r').read())
reduce = Code(open('reduce1.js','r').read())

results = p.map_reduce(map, reduce, "results",full_response = True)
results = p.map_reduce(map, reduce, "results",full_response = False)


from collections import defaultdict
count = defaultdict(int)
for result in results.find():
	count[result['_id']] = result['value']['count']

count =0

for i in p.find():
	try:
		f.write(str(i['metadata']['indexing_service']['classifier'])
		count = count +1
	except:
		pass


text= l[0]['metadata']['body']
segmentor= ss.segmentor(1) # train by decision tree classifier
sentences = eval(segmentor.segment(text, rtype =0))['sentences']


