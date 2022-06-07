from django.contrib import admin
from .models import *

class NotificationMessageAdmin(admin.ModelAdmin):
    search_fields = ['title', 'messsage'],
    list_display = ['title', 'message', 'date_and_time_of_execution', 'days_of_execution', 'time_of_execution']
    list_filter = ['for_all_users', 'for_store_owners', 'days_of_execution', 'for_regular_users']
    ordering = ['-created_at']


admin.site.register(NotificationMessage)
admin.site.register(BoxinHero)