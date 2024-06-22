# celery_app.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Market.settings')

app = Celery('Market')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'deactivate_inactive_users': {
        'task': 'Post.tasks.deactivate_inactive_users',
        'schedule': crontab(minute='*/1'),  # Runs every minute
    },
    'inactive_users': {
        'task': 'Post.tasks.inactive_users',
        'schedule': crontab(minute='*/1'),
    }
}
