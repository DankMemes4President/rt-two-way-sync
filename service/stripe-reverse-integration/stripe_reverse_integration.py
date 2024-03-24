import psycopg2


class CustomerDbAdapter:
    def __init__(self, db_cfg):
        conn = psycopg2.connect(dbname=db_cfg["dbname"], user=db_cfg["user"], password=db_cfg["password"],
                                host=db_cfg["host"], port=db_cfg["port"])
        conn.autocommit = True
        self.conn = conn
        cur = conn.cursor()
        cur.execute("SET SESSION myapp.reverse_trigger_off = TRUE")
        cur.close()
        print("[*] connected to postgres")

    def create_customer(self, stripe_id, name, email):
        print("[*] create customer called!")
        cur = self.conn.cursor()
        create__customer__sql = "INSERT INTO customers (name, email) VALUES  (%s, %s) RETURNING ID"
        create__stripe_integration__sql = "INSERT INTO stripe_integration (customer_id, stripe_id) VALUES (%s, %s)"
        try:
            cust_data = (name, email)
            cur.execute(create__customer__sql, cust_data)
            customer_id = cur.fetchone()[0]
            strip_data = (customer_id, stripe_id)
            cur.execute(create__stripe_integration__sql, strip_data)
        except Exception as e:
            print(f"[*] error : {e}")
        finally:
            cur.close()

    def update_customer(self, stripe_id, name, email):
        print("[*] update customer called!")
        cur = self.conn.cursor()
        # fetch__strip_id__from__customer_id = "SELECT stripe_id FROM stripe_integration WHERE customer_id = %s"
        fetch__customer_id__from__stripe_id = "SELECT customer_id FROM stripe_integration WHERE stripe_id=%s"
        update__customer_details = "UPDATE customers SET name=%s, email=%s WHERE id=%s"
        try:
            cur.execute(fetch__customer_id__from__stripe_id, (stripe_id,))
            cust_id = cur.fetchone()[0]
            cur.execute(update__customer_details, (name, email, cust_id))
        except Exception as e:
            print(f"[*] error : {e}")
        finally:
            cur.close()

    def delete_customer(self, stripe_id):
        print("[*] delete customer called!")
        cur = self.conn.cursor()
        try:
            delete__stripe_id = "DELETE FROM stripe_integration WHERE stripe_id=%s"
            cur.execute(delete__stripe_id, (stripe_id,))
        except Exception as e:
            raise e
        finally:
            cur.close()
        # try:
        #     check_if_record_exists = "SELECT customer_id FROM stripe_integration WHERE stripe_id = %s;"
        #     cur.execute(check_if_record_exists, (stripe_id,))
        #     row = cur.fetchone()
        #
        #     if row:
        #         customer_id = row[0]
        #         delete_row = "DELETE FROM customers WHERE id = %s;"
        #         cur.execute(delete_row, (customer_id,))
        #     else:
        #         print("[*] no record found in customers table")
        #
        #     delete_row_stripe_integration = "DELETE FROM stripe_integration WHERE stripe_id = %s;"
        #     cur.execute(delete_row_stripe_integration, (stripe_id,))
        # except Exception as e:
        #     print(f"[*] error : {e}")
        # finally:
        #     cur.close()
