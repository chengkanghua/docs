from django.contrib import admin
from django.urls import path, re_path

from article import views

urlpatterns = [

    re_path('^(\d{4})$', views.article_year),
    re_path('(?P<year>\d{4})/(?P<month>\d{2})', views.article_month),  # article_month(request,year=2000,month=12)

]
