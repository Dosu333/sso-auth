import os, requests

class VirtualBankAccount:
    def __init__(self, first_name, last_name, phone, email):
        self.url = 'https://api.paystack.co/'
        self.key = os.environ.get('PAYSTACK_SECRET_KEY')
        self.headers = {'Authorization': f'Bearer {self.key}'}
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email

    def create_customer(self):
        url = self.url + 'customer'
        data = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone
        }

        res = requests.post(url, data=data, headers=self.headers)
        response = res.json()

        if response['status']:
            return response['data']['customer_code']
        return None

    def create_virtual_bank_account(self):
        url = self.url + 'dedicated_account'
        customer = self.create_customer()
        data = {
            'customer': customer,
            'preferred_bank': "wema-bank"
        }

        res = requests.post(url, data=data, headers=self.headers)
        response = res.json()
        print(response)
        response = {
            'account_no': response['data']['account_number'],
            'bank': response['data']['bank']['slug'],
            'account_name': response['data']['account_name'],
            'customer': customer
        }
        return response

# vba = VirtualBankAccount('John', 'Doe', '+2347031589736', 'vladamir1865@gmail.com')

# print(vba.create_virtual_bank_account())

# url = "https://api.paystack.co/dedicated_account/requery?account_number=8202631367&provider_slug=wema-bank&date=2022-11-04"
# header = {'Authorization': 'Bearer sk_live_1f8ae1ccc890d9f02883efd429cd91d75fec15d1'}

# r = requests.get(url=url, headers=header)

# print(r.json())