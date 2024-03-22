import json
import time
import uuid
from confluent_kafka import Consumer, KafkaError, KafkaException


class EventObject:
    def __init__(self, unparsed_message):
        parsed_msg = json.loads(unparsed_message.value().decode('utf-8'))
        self.table_name = parsed_msg[0]
        self.operation_type = parsed_msg[1]
        self.payload = parsed_msg[2]

    def __repr__(self):
        return str({"table_name": self.table_name, "operation_type": self.operation_type, "payload": self.payload})


class EventListener:
    def __init__(self, kafka_server="mq:9092", kafka_topic=["changes"], kafka_group_id=uuid.uuid4()):
        self.kafka_config = {'bootstrap.servers': kafka_server, 'group.id': kafka_group_id}
        # self.kafka_server = kafka_server
        self.kafka_topic = kafka_topic
        self.kafka_group_id = kafka_group_id
        self.consumer = Consumer(self.kafka_config)
        self.consumer.subscribe(kafka_topic)

    def listen(self, timeout=1.0):
        # inbuilt polling in this
        msg = self.consumer.poll(timeout=timeout)
        if not msg:
            return None

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                return None
            elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                # in this context this only happens when the mq is empty and producer has not yet created the
                # topic.
                print("[*] could not find topic, sleeping for 5s...")
                time.sleep(5)
                return None
            else:
                # Handle other errors
                print(f"[*] error: {msg.error()}")
                raise KafkaException(msg.error())
        # Process message
        message = EventObject(msg)
        self.consumer.commit()
        return message

    def stop_listen(self):
        self.consumer.close()
