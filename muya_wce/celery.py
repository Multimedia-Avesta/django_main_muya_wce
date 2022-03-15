import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muya_wce.settings')

app = Celery('muya_wce')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Tasks which have not been completed are cancelled and their execution is terminated; task is returned to queue
# See: https://docs.celeryproject.org/en/stable/userguide/configuration.html#worker-cancel-long-running-tasks-on-connection-loss
app.conf.worker_cancel_long_running_tasks_on_connection_loss = True
app.autodiscover_tasks()
