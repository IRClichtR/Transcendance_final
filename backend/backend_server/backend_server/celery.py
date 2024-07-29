from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('Django_SETTINGS_MODULE','backend_server.settings')
app = Celery('backend_server', broker='redis://localhost:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_serializer = 'json'
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content='json',
    task_track_started=True,
    task_time_limit=30 * 60,
)