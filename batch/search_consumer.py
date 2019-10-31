
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer(
    'new-jersey-topic', group_id='jersey-indexer', bootstrap_servers=['kafka:9092'], api_version=(0, 10, 1))
es = Elasticsearch(['es'])

while True:
    for message in consumer:
        new_jersey_json = json.loads((message.value).decode('utf-8'))
        new_jersey_id = new_jersey_json['pk']
        es.index(index='jersey_index', doc_type='jersey',
                 id=new_jersey_id, body=new_jersey_json)
        es.indices.refresh(index="jersey_index")
