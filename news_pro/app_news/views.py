from django.shortcuts import render
from django.views.generic import (View, ListView, DetailView, edit, TemplateView,
                                  CreateView)
from django.shortcuts import redirect

from models import ArticleModel, get_today_visits, StatisticArticle
from feed import get_new_articles, check_articles_shares
# Create your views here.

class Index(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['last_news'] = ArticleModel.objects.all().order_by('-datetime')[:10]

        return context

def get_articles_from_pravda(request):
    get_new_articles()
    return redirect('news:index')


def get_shares(request):
    check_articles_shares()
    return redirect('news:index')


def get_time(request):
    get_today_visits()
    return redirect('news:index')


class AllNews(ListView):
    model = ArticleModel

    def get_context_data(self, **kwargs):
        context = super(AllNews, self).get_context_data(**kwargs)
        context['object_list'] = ArticleModel.objects.all().order_by('-datetime')

        return context


class OneNews(DetailView):
    model = ArticleModel

    def get_context_data(self, **kwargs):
        context = super(OneNews, self).get_context_data(**kwargs)
        context.update({
            'shares': StatisticArticle.objects.filter(article=self.object)
        })
        return context