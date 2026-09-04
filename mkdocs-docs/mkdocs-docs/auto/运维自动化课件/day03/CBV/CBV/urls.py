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
from django.urls import path, re_path

from sers import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register('publish', views.PublishView)
router.register('author', views.AuthorView)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('book/', views.book),
    # path("book/", views.BookView.as_view())

    path("sers/book/", views.BookView.as_view()),
    re_path("sers/book/(\d+)", views.BookDetailView.as_view()),

    # path("sers/publish/", views.PublishView.as_view()),
    # re_path("sers/publish/(?P<pk>\d+)", views.PublishDetailView.as_view()),

    #     path("sers/author/", views.AuthorView.as_view()),
    #     re_path("sers/author/(?P<pk>\d+)", views.AuthorDetailView.as_view())

    # viewset
    # path("sers/publish/", views.PublishView.as_view({"get": "list", "post": "create"})),
    # re_path("sers/publish/(?P<pk>\d+)",
    #         views.PublishView.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),

    # path("sers/author/", views.AuthorView.as_view({"get": "list", "post": "create"})),
    # re_path("sers/author/(?P<pk>\d+)",
    #         views.AuthorView.as_view({"get": "retrieve", "delete": "destroy", "put": "update"})),
]

urlpatterns += router.urls

'''
#------------------------------------------------ CBV

class BookView(View):
     

    def get(self, request):
        return HttpResponse("View GET请求...")

    def post(self, request):
        return HttpResponse("View POST请求...")

    def delete(self, request):
        return HttpResponse("View DELETE请求...")

class View:
    
    
    def as_view(cls):
         def view():
              # cls: BookView
              self = cls() # BookView()
              return self.dispatch(request, *args, **kwargs)
              
         return view
         
    def dispatch(self, request, *args, **kwargs):
   
        handler = getattr(self, request.method.lower())   # self.post    
        return handler(request, *args, **kwargs) # BookView： post()




path("book/", views.BookView.as_view())
path("book/", View.view)



# 一旦用户访问book，比如get请求访问/book/

get请求访问/book/ => view()  => return self.dispatch()  =》 return get()
post请求访问/book/ => view()  => return self.dispatch()  =》 return post()


'''

'''
#------------------------------------------------ DRF的APIView


from rest_framework.views import APIView


class BookView(APIView):

    def get(self, request):
        print("get方法已经执行")
        return HttpResponse("APIView GET请求...")

    def post(self, request):
        return HttpResponse("APIView POST请求...")

    def delete(self, request):
        return HttpResponse("APIView DELETE请求...")

class APIView：

      def as_view(cls):
          view = super().as_view()
          
          return view
          
      def dispatch(self, request, *args, **kwargs):
          # 构建新的request对象
          request = self.initialize_request(request, *args, **kwargs)
          self.request = request
          # 初始化：认证、权限、限流组件三件套
          self.initial(request, *args, **kwargs)
                self.perform_authentication(request)
                self.check_permissions(request)
                self.check_throttles(request)
          
          # 分发逻辑
          handler = getattr(self, request.method.lower())   # self.post    
          return handler(request, *args, **kwargs)
          
              
   
class View:
    
    
    def as_view(cls):
         def view():
              # cls: BookView
              self = cls() # BookView()
              return self.dispatch(request, *args, **kwargs)
              
         return view
         
    def dispatch(self, request, *args, **kwargs):
   
        handler = getattr(self, request.method.lower())   # self.post    
        return handler(request, *args, **kwargs) # BookView： post()






path("book/", views.BookView.as_view())
path("book/", View.view)
# 一旦用户访问book，比如get请求访问/book/

get请求访问/book/ => view()  => return self.dispatch()  =》 return get()
post请求访问/book/ => view()  => return self.dispatch()  =》 return post()


'''
