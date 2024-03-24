import os
import sys

from dotenv import load_dotenv

from service.customer_db.customer_db import CustomerDbAdapter

load_dotenv(dotenv_path="db/.env.db")


def main():
    db_cfg = {"dbname": os.getenv('POSTGRES_DB'), "user": os.getenv('POSTGRES_USER'),
              "password": os.getenv('POSTGRES_PASSWORD'), "host": "localhost", "port": "5432", }
    customerDbClient = CustomerDbAdapter(db_cfg)

    while True:
        try:
            print("\n[1] create customer\n[2] update customer\n[3] delete customer\n[4]fetch all customers")
            user_command = input("\nplease select a command: ")
            if user_command == "1":
                name = input("\nenter name: ")
                email = input("\nenter email: ")
                customerDbClient.create_customer(name, email)
            elif user_command == "2":
                print("\ncustomers: ")
                customerDbClient.fetchAllcustomers()
                id = input("\ncustomer id to edit: ")
                name = input("\nnew name: ")
                email = input("\nnew email: ")
                customerDbClient.update_customer(id, name, email)
            elif user_command == "3":
                print("\ncustomers: ")
                customerDbClient.fetchAllcustomers()
                id = input("\ncustomer id to delete: ")
                customerDbClient.delete_customer(id)
            elif user_command == "4":
                print("\n")
                customerDbClient.fetchAllcustomers()
            else:
                print("\nplease select a valid option")
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"something went wrong: {e}")


if __name__ == "__main__":
    main()
