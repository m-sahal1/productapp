# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')

app = Celery('myapp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'base.tasks.send_email_updates_to_staff',  # Task path
        'schedule': 6.0,  # Schedule the task to run every 6 seconds
        'args': (None,)
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
