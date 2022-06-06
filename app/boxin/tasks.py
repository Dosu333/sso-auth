from celery import shared_task
from django.db.models import Avg, Q
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import NotificationMessage
from .notify import bulk_notification, send_notification


@shared_task
def send_notify():
    today_notification = NotificationMessage.objects.filter(
                                   ( Q(days_of_execution__contains=[str(datetime.now().weekday())]) & 
                                    (
                                        Q(time_of_execution__hour=datetime.now().time().hour)
                                        & Q(time_of_execution__minute=datetime.now().time().minute)
                                        )
                                   )| (
                                       Q(date_and_time_of_execution__date=datetime.now().date()) &
                                       Q(date_and_time_of_execution__time__hour=datetime.now().time().hour) &
                                       Q(date_and_time_of_execution__minute=datetime.now().time().minute)

                                   )
                                       )

    if today_notification.filter(for_all_consumers=True).exists():
        consumer_notification = today_notification.get(for_all_consumers=True)
        users_id = get_user_model().objects.filter(roles__contains=['CONSUMER'])
        bulk_notification(user_ids=users_id, title=consumer_notification.title, message=consumer_notification.message)

    if today_notification.filter(for_all_restaurants=True).exists():
        restaurant_notification = today_notification.get(for_all_restaurants=True)
        users_id = get_user_model().objects.filter(roles__contains=['RESTAURANT'])
        bulk_notification(user_ids=users_id, title=restaurant_notification.title, message=restaurant_notification.message)

    if today_notification.filter(Q(for_all_restaurants=False) & Q(for_all_consumers=False)).exists():
        specific_notification = today_notification.filter(Q(for_all_restaurants=False) & Q(for_all_consumers=False))
        for item in specific_notification:
            bulk_notification(user_ids=item.specific_users.all(), title=item.title, message=item.message)