from django.shortcuts import render, redirect,HttpResponse

# Create your views here.
from cookie.models import UserInfo


def Shome(request):
    username = request.session.get("username")
    if username:
        return render(request, "Shome.html", {"username": username})
    else:
        return redirect("/session/login/")


def Slogin(request):
    if request.method == "GET":
        return render(request, "Slogin.html")

    else:
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        try:
            user = UserInfo.objects.get(user=user, pwd=pwd)

            request.session["username"] = user.user

            return redirect("/session/home/")
            # return HttpResponse("success!")


        except Exception as e:
            print(e)
            return redirect("/session/login/")




def Slogout(request):

    # request.session.flush()

    del request.session["username"]


    return redirect("/session/login/")


def shop(request):

    last_visit_time = request.session.get("last_visit_time")

    import datetime

    now = datetime.datetime.now().strftime("%Y-%m-%d %X")
    request.session["last_visit_time"] = now


    return render(request,"shop.html",{"last_visit_time":last_visit_time})