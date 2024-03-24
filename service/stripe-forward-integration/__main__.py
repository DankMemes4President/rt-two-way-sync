import os

from confluent_kafka import KafkaException
from dotenv import load_dotenv

from event_listener import consumer
from stripe_integration import StripeApi


def main():
    load_dotenv()
    event_listener = consumer.EventListener()
    db_cfg = {"dbname": os.getenv('POSTGRES_DB'), "user": os.getenv('POSTGRES_USER'),
              "password": os.getenv('POSTGRES_PASSWORD'), "host": "db", "port": "5432", }
    stripeApi = StripeApi(os.getenv('STRIPE_SECRET_KEY'), db_cfg)
    try:
        while True:
            message = event_listener.listen()
            if not message:
                # print("nothing")
                continue

            if message.operation_type == "DELETE":
                stripe_id = message.payload["stripe_id"]
                cust_id = message.payload["customer_id"]
                stripeApi.delete_customer(stripe_id, cust_id)
            else:
                cust_id = message.payload["id"]
                cust_name = message.payload["name"]
                cust_email = message.payload["email"]
                if message.operation_type == "INSERT":
                    stripeApi.create_customer(id=cust_id, name=cust_name, email=cust_email)
                elif message.operation_type == "UPDATE":
                    stripeApi.update_customer(id=cust_id, name=cust_name, email=cust_email)
                # elif message.operation_type == "DELETE":
                #     stripeApi.delete_customer(id=cust_id)
                else:
                    raise Exception("unknown operation type found")

    except KafkaException as e:
        print(f"[*] exception occurred: {e}")
    finally:
        event_listener.stop_listen()


if __name__ == "__main__":
    main()
