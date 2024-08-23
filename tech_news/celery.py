from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tech_news.settings')
app = Celery('tech_news')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-scraper-every-day': {
        'task': 'scraperbs4.tasks.run_scraper',
        'schedule': timedelta(hours=12),
        'args': (1, 10)
    }

}
