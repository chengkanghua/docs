"""DrfDemo URL Configuration

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
from django.urls import path, include, re_path
from viewApp.views import AuthorView, AuthorDetailView, PublishView,BookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("app01/", include("app01.urls")),

    path("authors/", AuthorView.as_view()),
    re_path("authors/(\d+)", AuthorDetailView.as_view()),

    # path("publishes", PublishView.as_view()),
    # # url:publishes/1     get(request,pk=1)
    # re_path("publishes/(?P<pk>\d+)", PublishDetailView.as_view()),

    # viewSet版本：
    # url:get 请求publishes/
    path("publishes", PublishView.as_view({"get": "list", "post": "create"})),
    # url:publishes/1     get(request,pk=1)
    re_path("publishes/(?P<pk>\d+)", PublishView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),


    # book
    # url:get 请求publishes/
    path("books", BookView.as_view({"get": "list", "post": "create"})),
    # url:publishes/1     get(request,pk=1)
    re_path("books/(?P<pk>\d+)", BookView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"})),

]

"""


class PublishView(ViewSetMixin, APIView):
    def list(self, request):
        return Response("list...")

    def create(self, request):
        return Response("create...")

    def single(self, request, pk):
        return Response("single...")

    def edit(self, request, pk):
        return Response("edit...")


path("publishes", PublishView.as_view({"get": "list", "post": "create"})),
path("publishes", PublishView.ViewSetMixin.view),


# 一旦用户get  请求访问：url:/publishes/ 执行view(request)
# 一旦用户post 请求访问：url:/publishes/ 执行view(request)
# 一旦用户get  请求访问：url:/publishes/1 执行view(request)


def view():

    actions = {"get": "single", "put": "edit"}
    
    for method,action in actions.items():
        handler = getattr(self, action)
        setattr(self, method, handler)  # self.get = single方法  self.post = edit方法
        
    return self.dispatch(request, *args, **kwargs)
    
    
def dispatch(request, *args, **kwargs):
           
       handler = getattr(self, request.method.lower())  # self.get:  single方法
       response = handler(request, *args, **kwargs)  # self.single方法()
     
    
"""
