from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.core.management import call_command
from .utils import send_email
from core.celery import APP
from twilio.rest import Client
from datetime import datetime
import requests


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
# def admin_marketplace_notify():
#     client = Client()
#     admin_to_numbers = ['+2347056918098', '+2348136800327', '+2349077499434']
#     url = "http://3.14.60.165:6080/api/v1/admin/droppers"
#     res = requests.get(url, verify=False)
#     response = res.json()
#     now = datetime.now()
    
#     for order in response['orders']:
#         if str(now.date()) == order['date'] and datetime.fromtimestamp(float(order['timestamp'])).time().minute == now.time().minute:
#             items = []
#             body = f"{order['customer_name']} just ordered a meal from {order['store_name']}. The meal is to be delivered to {order['customer_location']}. You can reach {order['customer_name']} via this phone number {order['customer_phone_number']}. This order is {order['status']}. For more info on this order, check the app."
#             for number in admin_to_numbers:
#                 client.messages.create(from_='+12312625574', to=number, body=body)
