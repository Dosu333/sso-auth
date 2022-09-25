from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.core.management import call_command
from django.contrib.auth import get_user_model
from .utils import send_email
from core.celery import APP
from twilio.rest import Client
from sendgrid import SendGridAPIClient
from .utils import add_user_to_contacts
from datetime import datetime
import requests, time, os


@APP.task()
def send_new_user_email(email_data):
    html_template = get_template('emails/new_user_welcome_template.html')
    text_template = get_template('emails/new_user_welcome_template.txt')
    html_alternative = html_template.render(email_data)
    text_alternative = text_template.render(email_data)
    send_email('Verify Email',
               email_data['email'], html_alternative, text_alternative)


@APP.task()
def send_registration_email(email_data):
    html_template = get_template(
        'emails/account_verification_template.html')
    text_template = get_template(
        'emails/account_verification_template.txt')
    html_alternative = html_template.render(email_data)
    text_alternative = text_template.render(email_data)
    send_email('Account Verification',
               email_data['email'], html_alternative, text_alternative)


@APP.task()
def send_password_reset_email(email_data):
    html_template = get_template('emails/password_reset_template.html')
    text_template = get_template('emails/password_reset_template.txt')
    html_alternative = html_template.render(email_data)
    text_alternative = text_template.render(email_data)
    send_email('Password Reset',
               email_data['email'], html_alternative, text_alternative)

# @APP.task()
# def send_contacts_to_sendgrid():
#     ten_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=10)
#     new_users = get_user_model().objects.filter(created_at__minute__gte=ten_minutes_ago.minute).values_list('email', 'firstname', 'lastname')

#     for user in new_users:
#         add_user_to_contacts(user)

@APP.task()
def add_user_to_contacts(email, first_name, last_name):
    sg = SendGridAPIClient(os.environ.get('SENDGRID_ADD_AND_UPDATE_KEY'))

    data = {
        "list_ids": ['57786ec5-35a1-41ef-9383-a81885dc5c15', ],
        "contacts": [
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name
            }
        ]
    }
    time.sleep(600)
    sg.client.marketing.contacts.put(request_body=data)


@APP.task()
def admin_marketplace_notify():
    client = Client()
    admin_to_numbers = ['+2347056918098', '+2348136800327', '+2349077499434', '+2348111761948']
    url = "http://3.14.60.165:6080/api/v1/admin/droppers"
    res = requests.get(url, verify=False)
    response = res.json()
    now = datetime.now()
    
    for order in response['orders']:
        if str(datetime.now().date()) == order['date'] and datetime.fromtimestamp(float(order['timestamp'])).time().minute == (datetime.now().time().minute - 1) and datetime.fromtimestamp(float(order['timestamp'])).time().hour == (datetime.now().time().hour - 1):
            dist = round(float(order['delivery_distance'])/1000, 1)
            fee = order['delivery_fee']

            if int(fee) == 0:
                if dist <= 4:
                    fee = 200
                else:
                    fee = dist * 60

            body = f"{order['customer_name']} just ordered a meal from {order['store_name']}. The meal is to be delivered to {order['customer_location']}. You can reach {order['customer_name']} via this phone number {order['customer_phone_number']}. This order is {order['status']}.  The delivery fee is {fee}. For more info on this order, check the app."
            for number in admin_to_numbers:
                client.messages.create(from_='whatsapp:+12312625574', to=f'whatsapp:{number}', body=body)
