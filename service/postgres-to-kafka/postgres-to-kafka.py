import os
import time

import psycopg2
from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import AdminClient, NewTopic
from dotenv import load_dotenv

load_dotenv()

# connecting and listening to postgres queue
conn = psycopg2.connect(dbname=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'),
                        password=os.getenv('POSTGRES_PASSWORD'), host="db", port="5432", )
conn.autocommit = True
cur = conn.cursor()
cur.execute("LISTEN changes")
print("[*] connected to postgres")

# pushing those changes to kafka mq
kafka_config = {'bootstrap.servers': 'mq:9092', }
producer = Producer(kafka_config)
admin_client = AdminClient(kafka_config)
topic_created = False
while True:
    if not topic_created:
        topic = NewTopic('changes')
        admin_client.create_topics([topic])
    # except KafkaException as e:
    #     print(f'[*] something went wrong: {e}')
    conn.poll()
    # print(conn.notifies)
    if conn.notifies:
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(notify.payload.encode('utf-8'))
            producer.produce('changes', value=notify.payload.encode('utf-8'))
            producer.flush()

    # print("[*] polling...")
    time.sleep(3)
