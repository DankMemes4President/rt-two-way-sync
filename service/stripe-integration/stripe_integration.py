import stripe


class StripeApi:
    # dummy functions for all three actions
    def __init__(self, stripe_secret_key):
        stripe.api_key = stripe_secret_key
        self.client = stripe

    def create_customer(self, id, name, email):
        print("[*] create customer called!")
        # customer = self.client.Customer.create(
        #     name=name,
        #     email=email
        # )
        # print(customer)
    def update_customer(self):
        print("[*] update customer called!")

    def delete_customer(self):
        print("[*] delete customer called!")
