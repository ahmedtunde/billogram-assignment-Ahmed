from __future__ import absolute_import, unicode_literals
from billogram import settings
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billogram.settings')

#Configuring Celery settings
app = Celery('config')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

max_timeout_in_seconds = 3 * 31 * 24 * 60 * 60
app.conf.broker_transport_options = {
    "visibility_timeout": max_timeout_in_seconds}

#Scheduling some jobs
app.conf.beat_schedule = {
    'send-notification-of-discount-code-to-user': {
        'task': 'send_notification_of_discount_code_to_user',
        'schedule': crontab(minute=0, hour=1),
    },
    'send-notification-of-discount-usage-to-brand': {
        'task': 'send_notification_of_discount_usage_to_brand',
        'schedule': crontab(minute=0, hour=1)
        
    },
}
