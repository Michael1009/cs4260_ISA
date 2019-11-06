
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json


print("Starting search_consumer.py", flush=True)
es = Elasticsearch(['es'])
while True:
    try:
        consumer = KafkaConsumer(
            'new-jersey-topic', group_id='jersey-indexer', bootstrap_servers=['kafka:9092'], api_version=(0, 10, 1))
        for message in consumer:
            print(json.loads((message.value).decode('utf-8')), flush = True)
            new_jersey_json = json.loads((message.value).decode('utf-8'))
            new_jersey_id = new_jersey_json['pk']
            if es.indices.exists(index="jersey_index"):
                es.index(index='jersey_index', doc_type='jersey',
                         id=new_jersey_id, body=new_jersey_json)
                es.indices.refresh(index="jersey_index")
    except Exception as e:
        print(e)
        continue
