from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json

# Create your views here.
from ajaxApp.models import UserInfo


def reg(request):
    return render(request, "reg.html")


def ajax_reg(request):
    print(request.POST)
    user = request.POST.get("user")

    ret = UserInfo.objects.filter(name=user)
    res = {"state": False, "msg": None}
    if ret:
        res["state"] = True
        res["msg"] = "该用户已经存在！"

    return HttpResponse(json.dumps(res,ensure_ascii=False),content_type="json")
    # return JsonResponse(res)