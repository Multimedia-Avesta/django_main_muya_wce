import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muya_wce.settings')

app = Celery('muya_wce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
