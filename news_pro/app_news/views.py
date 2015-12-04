#! /usr/bin/python
# -*- coding: utf-8 -*-

import xlwt
import StringIO
from datetime import timedelta, datetime

from django.views.generic import (View, ListView, DetailView, edit, TemplateView,
                                  CreateView)
from django.shortcuts import redirect
from django.http import HttpResponse


from models import ArticleModel, get_visits, StatisticArticle
from feed import get_pravda_articles, check_articles_shares, get_site_ua_articles
# Create your views here.

c

class Index(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['last_news'] = ArticleModel.objects.all().order_by('-datetime')[:10]

        return context


class AllNews(ListView):
    model = ArticleModel

    def get_context_data(self, **kwargs):
        from_date = self.request.GET.get('from')
        to_date = self.request.GET.get('to')
        text_to_find = self.request.GET.get('find')
        num_of_shares = self.request.GET.get('shares')
        order = self.request.GET.get('order')
        context = super(AllNews, self).get_context_data(**kwargs)
        if 'source' in self.kwargs:
            source = self.kwargs['source']
            articles = ArticleModel.objects.filter(source=source).order_by('-datetime')
        else:
            source = '0'
            articles = ArticleModel.objects.all().order_by('-datetime')
        context.update({'from':from_date,'to':to_date,'shares':num_of_shares,
                        'order':order,'text':text_to_find,'source':source})
        if from_date and to_date:
            to_date = datetime.strptime(to_date,"%Y-%m-%d")+timedelta(days=1)
            articles = articles.filter(datetime__range = (from_date, to_date))
        if num_of_shares:
            exclude_articles = [each.id for each in articles if each.shares_fb_total+each.shares_vk_total < int(num_of_shares)]
            articles = articles.exclude(id__in=exclude_articles)
        if text_to_find:
            articles = articles.filter(title__icontains=text_to_find)
        if order == '2':
            articles = reversed(sorted(articles, key=lambda t: t.shares_fb_total))

        context['object_list'] = articles

        return context


class OneNews(DetailView):
    model = ArticleModel

    def get_context_data(self, **kwargs):
        context = super(OneNews, self).get_context_data(**kwargs)
        context.update({
            'shares': StatisticArticle.objects.filter(article=self.object)
        })
        return context


def start(request):
    redirect('')

class SourceChoice(TemplateView):
    template_name = 'app_news/choice.html'

def get_articles(request):
    get_pravda_articles()
    get_site_ua_articles()
    return redirect('news:index')


def get_shares(request):
    check_articles_shares()
    return redirect('news:index')


def get_time(request):
    get_visits()
    return redirect('news:index')


def save_to_excel(request):
    pk = int(request.GET.get('pk'))
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Новина")

    article = ArticleModel.objects.get(pk=pk)
    statistics = StatisticArticle.objects.filter(article=article)


    style_string = "font: italic on"
    style = xlwt.easyxf(style_string)

    sheet.write(0, 0, article.title, style)

    style_string = "font: bold on; borders: bottom double"
    style = xlwt.easyxf(style_string)

    column_names = ['Час запросу', 'Shares FB',	'Shares VK', 'Attendance',	'Internet час']
    for i in range(len(column_names)):
        sheet.write(1, i, column_names[i], style)
    i=2
    for each in statistics:
        sheet.write(i,0,each.datetime.strftime("%d-%m-%y %H:%M"))
        sheet.write(i,1,each.shares_fb)
        sheet.write(i,2,each.shares_vk)
        sheet.write(i,3,each.attendance)
        sheet.write(i,4,each.internet_time)
        i+=1

    a = StringIO.StringIO()
    book.save(a)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=news#%s.xls' % article.id
    response.write(a.getvalue())
    a.close()
    return response