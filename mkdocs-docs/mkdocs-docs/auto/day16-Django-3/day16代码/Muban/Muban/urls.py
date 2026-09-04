"""Muban URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path

from app01.views import index,order
from app01.views import add_stu,select_stu,delete_stu,update_stu,select_stu2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('order/', order),
    path('add_stu/', add_stu),
    path('select_stu/', select_stu),
    path('select_stu2/', select_stu2),
    re_path('delete_stu/(\d+)', delete_stu),
    re_path('update_stu/(\d+)', update_stu),
]
