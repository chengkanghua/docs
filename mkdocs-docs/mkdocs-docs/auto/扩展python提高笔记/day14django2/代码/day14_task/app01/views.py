from django.shortcuts import render
from app01 import models


def home(request):
    """ 个人首页 """
    # 当前用户
    user = request.GET.get("user")

    # 找到当前用户所有待处理的工单
    data_list = models.AuditTask.objects.filter(user=user, status=2).select_related("task")

    return render(request, 'home.html', {"data_list": data_list, "user": user})


def audit(request):
    """ 审批界面 """

    user = request.GET.get("user")
    task_id = request.GET.get("tid")

    # 可以再做一些细粒度的判断
    task_object = models.Task.objects.filter(id=task_id).first()

    return render(request, "audit.html", {'user': user, "task_id": task_id, "task_object": task_object})
