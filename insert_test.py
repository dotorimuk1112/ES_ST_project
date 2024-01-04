from datetime import datetime
from elasticsearch import Elasticsearch
import config

es = Elasticsearch('http://localhost:9200')
INDEX = 'ins_test'

all_documents = []
for data in config.arr:
    all_documents.extend(data['cube_history'])
for i, doc in enumerate(all_documents):
    es.index(index=INDEX, body=doc, id=i+1)

result = es.search(index=INDEX, body={"query": {"match_all": {}}, "size": 10})
hits = result['hits']['hits']
for hit in hits:
    print(hit['_source'])