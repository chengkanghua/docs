from django.shortcuts import render, HttpResponse

# Create your views here.

# FBV
# def book(request):
#     if request.method == "GET":
#         return HttpResponse("GET请求...")
#
#     else:
#         return HttpResponse("POST请求...")

# CBV模式

# from django.views import View
#
#
# class BookView(View):
#
#     def dispatch(self, request, *args, **kwargs):
#         print("hello world")
#         ret = super().dispatch(request, *args, **kwargs)
#         return ret
#
#     def get(self, request):
#         print("get方法已经执行")
#         return HttpResponse("View GET请求...")
#
#     def post(self, request):
#         return HttpResponse("View POST请求...")
#
#     def delete(self, request):
#         return HttpResponse("View DELETE请求...")


#################################################################


from rest_framework.views import APIView



class BookView(APIView):

    def get(self, request):

        print("get方法已经执行")
        print("query_params:", request.query_params)
        return HttpResponse("APIView GET请求...")

    def post(self, request):
        print("data:", request.data)  # 请求体数据
        return HttpResponse("APIView POST请求...")

    def delete(self, request):
        return HttpResponse("APIView DELETE请求...")
