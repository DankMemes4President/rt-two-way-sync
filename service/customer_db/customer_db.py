import psycopg2


class CustomerDbAdapter:
    def __init__(self, db_cfg):
        conn = psycopg2.connect(dbname=db_cfg["dbname"], user=db_cfg["user"], password=db_cfg["password"],
                                host=db_cfg["host"], port=db_cfg["port"])
        conn.autocommit = True
        self.conn = conn
        cur = conn.cursor()
        cur.execute("SET SESSION myapp.reverse_trigger_off = FALSE")
        cur.close()
        print("[*] connected to postgres")

    def create_customer(self, name, email):
        cur = self.conn.cursor()
        create__customer__sql = "INSERT INTO customers (name, email) VALUES  (%s, %s)"
        try:
            cur.execute(create__customer__sql, (name, email))
            # result = cur.fetchone()
            print(f"[*] customer created")
        except Exception as e:
            raise e
        finally:
            cur.close()

    def update_customer(self, id, name, email):
        cur = self.conn.cursor()
        update__customer_details = "UPDATE customers SET name=%s, email=%s WHERE id=%s"
        try:
            cur.execute(update__customer_details, (name, email, id))
            # result = cur.fetchone()
            print(f"[*] customer updated")
        except Exception as e:
            raise e
        finally:
            cur.close()

    def delete_customer(self, id):
        cur = self.conn.cursor()
        delete__stripe_record = "DELETE FROM stripe_integration WHERE customer_id=%s"
        try:
            cur.execute(delete__stripe_record, id)
            print(f"[*] customer deleted")
        except Exception as e:
            raise e
        finally:
            cur.close()

    def fetchAllcustomers(self):
        cur = self.conn.cursor()
        fetch__all__customers = "SELECT * FROM customers"
        try:
            cur.execute(fetch__all__customers)
            result = cur.fetchall()
            print(f"[*] fetched all customers:")
            for i in result:
                print(f"{i[0]} | {i[1]} | {i[2]}")
        except Exception as e:
            raise e
        finally:
            cur.close()
