from django.shortcuts import render, HttpResponse


def index(request):
    print(request.user_object)
    return HttpResponse("...")
