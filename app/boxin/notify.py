from fcm_django.models import FCMDevice

def send_notification(user_ids, title, message):
    try:
        device = FCMDevice.objects.filter(user=user_ids).first()
        result = device.send_message(title=title,body=message,sound=True)
    except:
        pass

def bulk_notification(user_ids, title, message):
    try:
        devices = FCMDevice.objects.filter(user__in=user_ids)
        result = devices.send_message(title=title,body=message,sound=True)
    except:
        pass