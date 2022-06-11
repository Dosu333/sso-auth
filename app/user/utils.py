from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.core.files import File
from urllib.request import urlretrieve
from .models import Token
from .tasks import send_new_user_email


def send_email(subject, email_from, html_alternative, text_alternative):
    msg = EmailMultiAlternatives(
        subject, text_alternative, settings.EMAIL_FROM, [email_from])
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)


def resend_mail(user):
    token = Token.objects.filter(user=user).first()
    user_data = {'id': user.id, 'email': user.email, 'fullname': f"{user.lastname} {user.firstname}",
                    'url': f"{settings.CLIENT_URL}/signup/?token={token.token}"}
    send_new_user_email(user_data)


async def create_file_from_image(url):
    return File(open(url, 'rb'))
