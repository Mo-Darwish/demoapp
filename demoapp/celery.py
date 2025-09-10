import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoapp.settings')

app = Celery('demoapp' ,
             broker=os.getenv('CELERY_BROKER_URL'),
             backend=os.getenv('CELERY_RESULT_BACKEND')
            )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = "UTC"
# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True