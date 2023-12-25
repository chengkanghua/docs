from django.shortcuts import render


def index(request):
    qq_group_num = request.GET.get('num')
    return render(request, 'index.html', {"qq_group_num": qq_group_num})
