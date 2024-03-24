import os

from fastapi import FastAPI
from stripe_reverse_integration import CustomerDbAdapter

app = FastAPI()


@app.post("/webhook")
async def webhook(payload: dict):
    print(payload)
    cust_id = payload['data']['object']['id']
    cust_name = payload['data']['object']['name']
    cust_email = payload['data']['object']['email']
    op_type = payload['type']

    db_cfg = {"dbname": os.getenv('POSTGRES_DB'), "user": os.getenv('POSTGRES_USER'),
              "password": os.getenv('POSTGRES_PASSWORD'), "host": "db", "port": "5432", }
    customerDbClient = CustomerDbAdapter(db_cfg)

    if op_type == "customer.created":
        customerDbClient.create_customer(cust_id, cust_name, cust_email)
    elif op_type == "customer.updated":
        customerDbClient.update_customer(cust_id, cust_name, cust_email)
    elif op_type == "customer.deleted":
        customerDbClient.delete_customer(cust_id)
    else:
        print("[*] unexpected event received")
