from django.contrib import admin
from .models import NewsModel, ArticleModel

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class NewsResource(resources.ModelResource):

    class Meta:
        model = NewsModel


class NewsModelAdmin(ImportExportModelAdmin):
    resource_class = NewsResource

admin.site.register(NewsModel, NewsModelAdmin)
# admin.site.register(NewsModelAdmin)

class ArticleResource(resources.ModelResource):

    class Meta:
        model = ArticleModel

class ArticleModelAdmin(ImportExportModelAdmin):
    resource_class = ArticleResource

admin.site.register(ArticleModel, ArticleModelAdmin)
