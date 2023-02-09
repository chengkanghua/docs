from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

import datetime
import json


def timer(request):
    now = datetime.datetime.now().strftime("%Y/%m/%d %X")
    # return HttpResponse(now)

    return render(request, "app01/timer.html", {"showNow": now})


def login(request):
    if request.method == "GET":
        # 获取登录页面
        return render(request, "login.html")

    else:

        # print(request.POST)
        # print(request.body, type(request.body))  # 请求体原数据
        #
        # data = json.loads(request.body.decode())
        # print(data["username"])

        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        if user == "rain" and pwd == "123":
            # return HttpResponse("登录成功")
            return redirect("/timer/")
        else:
            return HttpResponse("用户名或者密码错误！")




"""
http/1.1  301  

location:/timer/



"""