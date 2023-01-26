from django.shortcuts import render, HttpResponse,redirect


# Create your views here.


def index(request):
    print("index")

    return HttpResponse("OK")





