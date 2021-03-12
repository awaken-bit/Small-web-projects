import os  
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerydjango.settings')
app = Celery('celerydjango')  
app.config_from_object('django.conf:settings', namespace='CELERY')  
app.autodiscover_tasks()  


app.conf.beat_schedule = {
    'creating_post': {
        'task': 'main.tasks.information_panel',
        'schedule': 30.0,
    },
}