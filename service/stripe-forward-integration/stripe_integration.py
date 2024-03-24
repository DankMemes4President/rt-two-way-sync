import psycopg2
import stripe


class StripeApi:
    # dummy functions for all three actions
    def __init__(self, stripe_secret_key, db_cfg):
        conn = psycopg2.connect(dbname=db_cfg["dbname"], user=db_cfg["user"], password=db_cfg["password"],
                                host=db_cfg["host"], port=db_cfg["port"])
        conn.autocommit = True
        self.conn = conn
        cur = conn.cursor()
        cur.execute("SET SESSION myapp.reverse_trigger_off = FALSE")
        cur.close()
        print("[*] connected to postgres")
        stripe.api_key = stripe_secret_key
        self.client = stripe

    def create_customer(self, id, name, email):
        print("[*] create customer called!")
        cur = self.conn.cursor()
        create__customer__sql = "INSERT INTO stripe_integration (customer_id, stripe_id) VALUES (%s,%s)"
        try:
            customer = self.client.Customer.create(name=name, email=email, metadata={"fwd-push": True})
            data = (str(id), customer.id)
            cur.execute(create__customer__sql, data)
        except Exception as e:
            raise e
            print(f"[*] error : {e}")
        finally:
            cur.close()

    def update_customer(self, id, name, email):
        print("[*] update customer called!")
        cur = self.conn.cursor()
        fetch__strip_id__from__customer_id = "SELECT stripe_id FROM stripe_integration WHERE customer_id = %s"
        try:
            print("hi")
            cur.execute(fetch__strip_id__from__customer_id, str(id))
            stripe_id = cur.fetchone()[0]
            self.client.Customer.modify(stripe_id, name=name, email=email, metadata={"fwd-push": True})
        except Exception as e:
            raise e
            print(f"[*] error : {e}")
        finally:
            cur.close()

    def delete_customer(self, stripe_id, cust_id):
        print("[*] delete customer called!")
        cur = self.conn.cursor()
        # check__if__record__exists = "SELECT EXISTS(SELECT 1 FROM customers WHERE id=%s);"
        try:
            # cur.execute(check__if__record__exists, (str(cust_id)))
            # record_exists = cur.fetchone()[0]
            # if record_exists:
            #     delete__customer__record = "DELETE FROM customers WHERE id=%s"
            #     cur.execute(delete__customer__record, (str(cust_id)))
            self.client.Customer.delete(stripe_id, metadata={"fwd-push": True})
        except Exception as e:
            raise e
        # check__if__record__exists = "SELECT EXISTS(SELECT 1 FROM stripe_integration WHERE customer_id = %s);"
        #
        # try:
        #     cur.execute(check__if__record__exists, str(id))
        #     record_exists = cur.fetchone()[0]
        #
        #     if record_exists:
        #         delete__row = "DELETE FROM stripe_integration WHERE customer_id = %s;"
        #         cur.execute(delete__row, str(id))
        # except Exception as e:
        #     raise e
        #     print(f"[*] error : {e}")
        # finally:
        #     cur.close()
