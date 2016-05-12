# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
import logging`

from django.core.management.base import NoArgsCommand
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from app_news.models import ArticleModel, StatisticArticle

logger = logging.getLogger('error')

class Command(NoArgsCommand):
    def handle(self, **options):
        now_minus_hour = datetime.today() - timedelta(hours=1)
        last_statistics_time = StatisticArticle.objects.filter(datetime__gte=now_minus_hour).exists()
        if not last_statistics_time:
            recipient_list = ['ilya.batozskiy@raccoongang.com',
                              'employer.email']
            subject, from_email = 'Some problems on News Server', 'no-reply@news.com'
            last_working_time = StatisticArticle.objects.all().order_by('datetime').\
                                                 last().datetime.replace(tzinfo=None)
            not_working = (datetime.today().replace(tzinfo=None) -  last_working_time).total_seconds() / 3600.0
            logger.error('Check time %, last working time %s' % 
                         (str(datetime.today()), str(last_working_time)))
            text_content = 'Щось зламалося на сервері, оновлень нема вже більше %i годин(и)' % not_working
            msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            msg.send()
