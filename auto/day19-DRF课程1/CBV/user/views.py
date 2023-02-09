from django.shortcuts import render, HttpResponse
from django.views import View

from django.core import serializers


# Create your views here.

# FBV模式
def login(request):
    if request.method == "GET":
        return HttpResponse("GET...")
    else:
        return HttpResponse("POST...")


# CBV模式
class LoginView(View):

    def dispatch(self, request, *args, **kwargs):
        print("dispatch...")
        # 引用父类方法
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return HttpResponse("LoginView GET...")

    def post(self, request):
        return HttpResponse("LoginView POST...")

    def delete(self, request):
        return HttpResponse("LoginView DELETE")
