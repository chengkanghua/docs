"""CBV URL Configuration

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

from user.views import login, LoginView
from drfdemo.views import StudentView,StudentDetailView,PublishView,PublishDetailView,AuthorView,AuthorDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', login),
    path('login/', LoginView.as_view()),
    path('student/', StudentView.as_view()),
    re_path('student/(\d+)/', StudentDetailView.as_view()),

    path('publish/', PublishView.as_view()),
    re_path('publish/(\d+)/', PublishDetailView.as_view()),

    path('author/', AuthorView.as_view()),
    re_path('author/(?P<pk>\d+)/', AuthorDetailView.as_view()),  # foo(request,pk=12)
]

'''
 path('login/', LoginView.as_view()),
 path('login/', View.view),

一旦浏览器发起get请求 /login/   --- > View.view()

def View.view():
     http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

     self = cls(**initkwargs)
     return self.dispatch(request, *args, **kwargs)



def dispatch(self,request, *args, **kwargs):


    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    
    return handler(request, *args, **kwargs)



######################### APIView #############################



 path('student/', StudentView.as_view()),
 path('student/', View.view),

一旦浏览器发起get请求 /student/   --- > View.view()

def View.view():
     http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

     self = cls(**initkwargs)
     return self.dispatch(request, *args, **kwargs)



def APIView.dispatch(self,request, *args, **kwargs):

    # 构建新的request对象
    request = self.initialize_request(request, *args, **kwargs)
    # 执行三个组件：认证、权限、限流
    self.initial(request, *args, **kwargs)
    # 基于反射分发逻辑 
    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
    
    return handler(request, *args, **kwargs)
     


     

'''
