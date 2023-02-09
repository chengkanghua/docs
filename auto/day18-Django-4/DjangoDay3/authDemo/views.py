from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import auth


def Ahome(request):
    print(request.user.username, bool(request.user.is_authenticated))

    if request.user.is_authenticated:
        return render(request, "Ahome.html")

    else:
        return redirect("/auth/login/")


def Alogout(request):
    auth.logout(request)

    return redirect("/auth/login/")


def Alogin(request):
    if request.method == "GET":

        return render(request, "Alogin.html")
    else:
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        # 去认证是否存在该用户
        user = auth.authenticate(username=user, password=pwd)
        if user:
            # request.session["_auth_user_id"]= user.id
            auth.login(request, user)

            return redirect("/auth/home/")
            # return HttpResponse("success!")

        else:
            return redirect("/auth/login/")


from django.contrib.auth.models import User




def Areg(request):
    # User.objects.create(username="alvin",password="123")
    # User.objects.create_user(username="alvin",password="123")
    User.objects.create_superuser(username="alvin",password="123",email="345@qq.com")
    return redirect("/auth/login/")


