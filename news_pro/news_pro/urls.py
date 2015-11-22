from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'news_pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('app_news.urls', namespace='news')),\
    url(r'^admin/', include(admin.site.urls)),
)
