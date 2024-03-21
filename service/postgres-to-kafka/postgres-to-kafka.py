import os

import psycopg2
from dotenv import load_dotenv
from confluent_kafka import Producer

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
while True:
    conn.poll()
    # print(conn.notifies)
    if conn.notifies:
        while conn.notifies:
            notify = conn.notifies.pop(0)
            print(notify.payload.encode('utf-8'))
            producer.produce('changes', value=notify.payload.encode('utf-8'))
            producer.flush()

    # print("[*] polling...")
