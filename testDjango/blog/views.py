# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
import models


# Create your views here.
def hello(request):
    articals = models.Article.objects.all()
    return render(request, "blog/index.html", {"articals": articals})


def article_page(request, id):
    article = models.Article.objects.get(pk=id)
    return render(request, 'blog/article_page.html', {"article": article})


def edit_page(request, id):
    if str(id) == '0':
        return render(request, 'blog/edit_page.html')
    else:
        art = models.Article.objects.get(pk=id)
        return render(request, 'blog/edit_page.html', {'article': art})


def edit_action(request):
    id = request.POST.get('id', '0')
    title = request.POST.get("title", "TITLE")
    content = request.POST.get('content', 'CONTENT')
    if str(id) == '0':
        models.Article.objects.create(title=title, content=content)
        articles = models.Article.objects.all()
        return render(request, 'blog/index.html', {'articals': articles})

    else:
        article = models.Article.objects.get(pk=id)
        article.title = title
        article.content = content
        article.save()
        return render(request, 'blog/article_page.html', {'article': article})


def posttest(request):
    name = request.POST.get("name")
    pwd = request.POST.get("pass")
    print name
    return render(request, 'blog/posttest.html', {"name": name, "pass": pwd})
