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

    if today_notification.filter(for_all_users=True).exists():
        general_notification = today_notification.get(for_all_users=True)
        users_id = get_user_model().objects.all()
        bulk_notification(user_ids=users_id, title=general_notification.title, message=general_notification.message)

    if today_notification.filter(for_store_owners=True).exists():
        store_notification = today_notification.get(for_store_owners=True)
        users_id = get_user_model().objects.filter(roles__contains=['STORE_OWNER'])
        bulk_notification(user_ids=users_id, title=store_notification.title, message=store_notification.message)

    if today_notification.filter(for_regular_users=True).exists():
        regular_notification = today_notification.get(for_regular_users=True)
        users_id = get_user_model().objects.filter(roles__contains=['REGULAR'])
        bulk_notification(user_ids=users_id, title=regular_notification.title, message=regular_notification.message)

    if today_notification.filter(Q(for_all_users=False) & Q(for_store_owners=False) & Q(for_regular_users=False)).exists():
        specific_notification = today_notification.filter(Q(for_all_users=False) & Q(for_store_owners=False) & Q(for_regular_users=False))
        for item in specific_notification:
            bulk_notification(user_ids=item.specific_users.all(), title=item.title, message=item.message)