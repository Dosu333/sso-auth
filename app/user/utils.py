from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.core.files import File
from urllib.request import urlretrieve
from sendgrid import SendGridAPIClient
import os


def send_email(subject, email_from, html_alternative, text_alternative):
    msg = EmailMultiAlternatives(
        subject, text_alternative, settings.EMAIL_FROM, [email_from])
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)

def add_user_to_contacts(user):
    sg = SendGridAPIClient(os.environ.get('SENDGRID_ADD_AND_UPDATE_KEY'))

    data = {
        "list_ids": ['57786ec5-35a1-41ef-9383-a81885dc5c15', ],
        "contacts": [
            {
                "email": user[0],
                "first_name": user[1],
                "last_name": user[2]
            }
        ]
    }

    sg.client.marketing.contacts.put(request_body=data)

async def create_file_from_image(url):
    return File(open(url, 'rb'))
