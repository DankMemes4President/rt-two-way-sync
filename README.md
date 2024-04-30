# Realtime-Two-Way-Sync

## Deployment

1. `$ docker built -t rtws-base:latest . -f base/Dockerfile`
This will create a base docker image for other images.
2. We’ll require two environment variables files
    1. .env.kafka
    2. ./db/.env.db 
    3. service/stripe-forward-integration/.env.stripe
3. `$ docker-compose up --build -d`  
This will create all the necessary service containers
4. `$ ngrok http 8080`
This will create a ngrok domain for our webhook

---

### .env.kafka

```
ZOOKEEPER_CLIENT_PORT: 2181
ZOOKEEPER_TICK_TIME: 2000
KAFKA_BROKER_ID: 1
KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://mq:9092
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

### .db/.env.db

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

### service/stripe-forward-integration/.env.stripe

```
STRIPE_SECRET_KEY="YOUR_STRIPE_KEY"
```

---

## System Architecture

![system-architechture .png](./assets/system-architechture%20.png)

We have the following services in our system.

- **customer_db:** This is a basically the `__main__.py` file in the root of the project. We use this service to interact with out database.
- **postgres_to_kafka:** This service allows us to listen the changes on postgres using polling and pushes out new events to the ‘changes’ topic in the kafka message queue.
- **stripe_forward_integration:** This service basically acts as a events listener service which listens for changes in the database.
- **stripe_reverse_integration:** This service allows us to catch events from stripe using a webhook and then push those changes to the database.

### Outward Sync flow

1. Changes to our customer catalogue database is base using this service, we can create/delete/update/list all the customer in our catalogue.
2. These changes are pushed to the message queue using a combination of postgres database triggers and `pg_notify`. We first insert/update/delete data on the database which in turn calls the trigger function. In this trigger function we use `pg_notify` to send events to postgres’ `changes` channel.
3. These events are picked up by postgres_to_kafka service and pushed to the `changes` topic on the kafka message queue.
4. We continuously listen to new messages on this topic and call necessary functions from stripe_forward_integration to perform the necessary changes to stripe database using its API.

### Inward Sync flow

1. changes are made on the stripe dashboard.
2. Stripe makes a request to our exposed webhook which allows us to capture data.
3. We use this data to make changes to the database using stripe_reverse_integration’s functions and classes.

### Potential Problems

There are two loops that exist in our flow

1. When we push changes to the database from our stripe_reverse_integration service, normally our triggers would start getting executed which means the trigger function will send out the event to `changes` channel. This is a problem because we just needed to save our changes to the database in our reverse sync flow, but now we have initiated the outward sync flow too.
To fix this problem I decided to use session variables in postgres. We make our trigger function logic conditional and accordingly set session variables in different services to allow for conditional triggering of our trigger function logic.
2. When we make changes to the strip database using its API, it automatically sends back a request to our webhook which initiates the inward-sync flow and creates duplicate entries. To fix this, we use metadata on each customer object on stripe. When creating/updating/deleting we set a variable in the metadata key value pair to true. Now we check for this boolean on our webhook handler, and accordingly process the request if its bool is false or if the metadata itself isn’t present. One problem we face here is that whenever we want to update/create customers from the stripe dashboard, we need to either set this bool to false or alternatively remove this bool entirely for this flow to work.

---

### Extending our project to Salesforce Customer Catalogue

[reference docs](https://developer.salesforce.com/docs/commerce/commerce-api/references/customers?meta=Summary)

We’ll need to create an extra service for our salesforce feature.
A class with methods for auths, creating/updating and deleting a customer would be needed.
A new table to track customer IDs for salesforce will also be needed to be built and accordingly the trigger logic will be updated (this is mainly on the deletion aspect, creation and updating will remain the same)
We can either use a different topic to grant us more control over which service we want to send our customer data to, or we can use the same ‘changes’ topic as well. Using our message queue and events_listener library the addition of this service would be very modular and decoupled from the rest of the project.

### Extending our project to Invoice Catalogue

Here we can again use a different topic in the message queue and leverage its pubsub features to get a decoupled and more granualar control over the execution of our services.

We can simply send out events on the `invoice` channel from our customer_db service and hence pickup and generate invoices from our invoices service.
