from confluent_kafka import KafkaException

from event_listener import consumer


def main():
    event_listener = consumer.EventListener()
    try:
        while True:
            message = event_listener.listen()
            if not message:
                print("nothing")
                continue
            print(message)
    except KafkaException as e:
        print(f"[*] exception occurred: {e}")
    finally:
        event_listener.stop_listen()

if __name__ == "__main__":
    main()
