from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'wallet'

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('web_hook/', web_hook, name='web_hook')
]
