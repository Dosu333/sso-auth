from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class BoxinHero(BaseModel):
    AFFILIATE_CHOICES = [
        ('ASSOCIATE', 'ASSOCIATE'),
        ('HERO', 'HERO')
    ]

    fullname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    code = models.CharField(max_length=7, blank=True, null=True, unique=True)
    affiliate_type = models.CharField(max_length=10, choices=AFFILIATE_CHOICES, null=True,blank=True)
    referral_link = models.SlugField(max_length=255,blank=True, null=True)

    class Meta:
        ordering = ('fullname', )

    def __str__(self):
        return self.fullname
    
    def create_code(self):
        splitname = self.fullname.split()
        self.code = splitname[0][:3] + splitname[1][:2] + get_random_string(2)
        self.referral_link = f"https://login.boxin.ng/signup?referred_by={self.code}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.create_code()
        super().save(*args, **kwargs)


class NotificationMessage(BaseModel):
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ]

    days_of_execution = ArrayField(models.CharField(max_length=10, choices=DAY_CHOICES, null=True,blank=True), null=True, blank=True, size=7)
    title = models.CharField(max_length=225, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date_and_time_of_execution = models.DateTimeField(null=True, blank=True)
    time_of_execution = models.TimeField(null=True, blank=True)
    for_all_users = models.BooleanField(default=False)
    for_regular_users = models.BooleanField(default=False)
    for_store_owners = models.BooleanField(default=False)
    specific_users = models.ManyToManyField(get_user_model(), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
