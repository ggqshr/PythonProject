# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models


# Register your models here.
class ArticleAmin(admin.ModelAdmin):
    list_display = ('title', 'content','pub_time')
    list_filter = ('pub_time',)


admin.site.register(models.Article, ArticleAmin)
