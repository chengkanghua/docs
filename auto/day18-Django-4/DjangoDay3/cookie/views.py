from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from cookie.models import UserInfo


def login(request):
    if request.method == "GET":

        return render(request, "login.html")

    else:
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        try:
            user = UserInfo.objects.get(user=user, pwd=pwd)

            # res = HttpResponse("登录成功")
            res = redirect("/home/")
            # 对响应体设置cookie
            res.set_cookie("isLogin", "true", max_age=10)
            res.set_cookie("username", user.user, max_age=10)
            return res


        except Exception as e:
            print(e)
            return redirect("/login/")


def home(request):
    print("home")

    if request.COOKIES.get("isLogin") == "true":
        username = request.COOKIES.get("username")
        return render(request, "index.html", {"username": username})

    return redirect("/login")
