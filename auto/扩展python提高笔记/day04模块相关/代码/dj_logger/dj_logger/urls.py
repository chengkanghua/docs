"""dj_logger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import logging

from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse
# from django.conf import global_settings
# from dj_logger import settings
from django.conf import settings  # 应该用这个


def index(request):
    logger_object = logging.getLogger("error")
    logger_object.error("错误了")

    return HttpResponse('成功')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
]
