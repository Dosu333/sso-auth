
from django.core.files import File
from urllib.request import urlretrieve
import uuid
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from .managers import CustomUserManager
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string


USER_ROLE = (
    ('CONSUMER', 'CONSUMER'),
    ('ADMIN', 'ADMIN'),
    ('RESTAURANT', 'RESTAURANT'),
    ('DRIVER', 'DRIVER'),
    ('SUPERADMIN', 'SUPERADMIN'),
    ('STORE_OWNER', 'STORE_OWNER'),
    ('REGULAR', 'REGULAR'),
)

GENDER_OPTION = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE')
)

TOKEN_TYPE = (
    ('ACCOUNT_VERIFICATION', 'ACCOUNT_VERIFICATION'),
    ('PASSWORD_RESET', 'PASSWORD_RESET'),
)


def default_role():
    return ['REGULAR']


class User(AbstractBaseUser, PermissionsMixin):
    HOW_EXPENSIVE = [
        ('1', 'CHEAP'),
        ('2', 'AVERAGE'),
        ('3', 'EXPENSIVE')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        _('email address'), null=True, blank=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to='users/', blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, null=True)
    roles = ArrayField(models.CharField(max_length=20, blank=True,
                                        choices=USER_ROLE), default=default_role, size=6)
    businessname =  models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    referred_by = models.CharField(max_length=225, blank=True, null=True)
    referred_by_user = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    referred_by_hero = models.CharField(max_length=225, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email

    def save_last_login(self):
        self.last_login = datetime.now()
        self.save()


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    token_type = models.CharField(
        max_length=100, choices=TOKEN_TYPE, default='ACCOUNT_VERIFICATION')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(timezone.utc)
        time_diff = now - self.created_at
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.user.verified = True
        self.user.save()

    def generate(self):
        if not self.token:
            self.token = get_random_string(120)
            self.save()

    def reset_user_password(self, password):
        self.user.set_password(password)
        self.user.save()
