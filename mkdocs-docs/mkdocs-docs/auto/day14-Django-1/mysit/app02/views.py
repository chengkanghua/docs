from django.shortcuts import render, HttpResponse


# Create your views here.

def index(request):
    # 请求方式
    print(request.method) # GET
    # 请求的url路径
    print(request.path)  # /
    print(request.get_full_path())  # /?a=1
    print(request.META.get("REMOTE_ADDR"))

    # 请求数据
    print(request.GET)
    print(request.POST)

    return HttpResponse("OK")



