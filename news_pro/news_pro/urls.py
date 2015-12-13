from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^', include('app_news.urls', namespace='news')),
    url(r'^admin/', include(admin.site.urls)),
)
