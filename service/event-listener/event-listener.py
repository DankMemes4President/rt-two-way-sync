import time

from confluent_kafka import Consumer, KafkaError

kafka_server = "mq:9092"
kafka_topic = "changes"
kafka_group_id = "1"

kafka_config = {'bootstrap.servers': kafka_server, 'group.id': kafka_group_id, 'auto.offset.reset': 'earliest'}

consumer = Consumer(kafka_config)
consumer.subscribe([kafka_topic])

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if not msg:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition, ignore
                continue
            elif msg.error() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                # in this context this only happens when the mq is empty and producer has not yet created the topic.
                print("[*] could not find topic, sleeping for 5s...")
                time.sleep(5)
                continue
            else:
                # Handle other errors
                print(f"[*] error: {msg.error()}")
                break

            # Process message
        print(f"[*] received message: {msg.value().decode('utf-8')}")
# except Exception as e:
#     print(f"[*] exited due to {e}")
finally:
    consumer.close()
