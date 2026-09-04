import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# 一旦有新消息到来，我就放在数据库中。
DB = ["nihao", "nibuhao", "老黄"]


def home(request):
    return render(request, 'home.html')


def send_msg(request):
    text = request.GET.get('text')
    DB.append(text)

    return HttpResponse("ok")


def get_msg(request):
    index = request.GET.get('index')  # 字符串类型
    index = int(index)

    context = {
        "data": DB[index:],
        "max_index": len(DB)  # 3
    }
    return JsonResponse(context)  # 数据序列化；响应头 application/json
