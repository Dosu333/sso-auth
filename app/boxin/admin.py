from django.contrib import admin
from .models import *

class NotificationMessageAdmin(admin.ModelAdmin):
    search_fields = ['title', 'messsage'],
    list_display = ['title', 'message', 'date_and_time_of_execution', 'days_of_execution', 'time_of_execution']
    list_filter = ['for_all_consumers', 'for_all_restaurants', 'days_of_execution']
    ordering = ['-created_at']


admin.site.register(NotificationMessage)
admin.site.register(BoxinHero)