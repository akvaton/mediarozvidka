from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_pro.settings')

app = Celery('app_news')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.CELERYBEAT_SCHEDULE = {
    'get_new_articles_and_shares': {
        'task': 'app_news.tasks.GetNewsAndShares',
        'schedule': crontab(minute='*/15')
    }
}
