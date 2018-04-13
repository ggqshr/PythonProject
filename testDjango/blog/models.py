# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=32, default="Title")
    content = models.TextField(null=True)
    pub_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.title
