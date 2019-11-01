
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json


print("Starting view_count.py", flush=True)
while True:
    try:
        consumer = KafkaConsumer(
            'new-view-topic', group_id='view-indexer', bootstrap_servers=['kafka:9092'], api_version=(0, 10, 1))
        es = Elasticsearch(['es'])
        for message in consumer:
            print(json.loads((message.value).decode('utf-8')), flush=True)
            new_view_json = json.loads((message.value).decode('utf-8'))
            user_id = new_view_json['user_id']
            jersey_id = new_view_json['jersey_id']

            f = open("/app/batch/view_count.log", "a")
            print("Writing to view_count.log", flush=True)
            f.write(str(user_id)+','+str(jersey_id)+"\n")
            f.close()
    except Exception:
        continue
