import json
import random
import pytz
from datetime import datetime, timedelta
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TaskSchedule, TaskHost
from django.conf import settings
from celery.schedules import schedule
from django_celery_beat.tzcrontab import TzAwareCrontab
from rest_framework import status

class PeriodView(APIView):
    # 获取计划任务的周期类型数据返回给客户端
    def get(self,request):
        data = TaskSchedule.period_way_choices
        return Response(data)


class TaskView(APIView):
    def get(self,request):
        # 1. 获取任务列表数据返回给客户端
        task_list = PeriodicTask.objects.all()
        results = [{
            "id": task.id,
            "name": task.name,
            "enabled": task.enabled,
            "type": "普通计划任务" if isinstance(task.schedule, schedule) else ("周期计划任务" if isinstance(task.schedule, TzAwareCrontab) else "定时一次任务"),
        } for task in task_list]

        # todo 2. 去redis中获取每个任务的执行结果展示给客户端

        return Response(results)

    def post(self, request):
        task_data = request.data
        period_way = task_data.get('period_way')  # 计划任务的周期类型
        hosts_ids = task_data.get('hosts')  # 计划任务的执行的远程主机列表
        task_cmd = task_data.get('task_cmd')  # 计划任务要执行的任务指令
        period_content = task_data.get('period_content')  # 计划任务的周期的时间值
        task_name = task_data.get('task_name')  # 任务名称，注意不能重复

        try:
            PeriodicTask.objects.get(name=task_name)
            task_name = f"{task_name}-{str(random.randint(1000, 9999))}"
        except:
            pass

        if period_way == 1:  # 普通周期任务,默认单位为秒数，可以选择修改
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=int(period_content),
                period=IntervalSchedule.SECONDS,
            )
            period_obj = PeriodicTask.objects.create(
                interval=schedule,    # we created this above.
                name=task_name,        # simply describes this periodic task.
                task='schedule_task',  # name of task.
                args=json.dumps([task_cmd, hosts_ids]),
                expires=datetime.utcnow() + timedelta(minutes=30)
            )
            period_beat = period_obj.id
        elif period_way == 2:  # 一次性任务
            period_beat = 1
            pass
        else:  # cron任务
            period_content_list = period_content.split(" ")
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=period_content_list[0],
                hour=period_content_list[1],
                day_of_week=period_content_list[2],
                day_of_month=period_content_list[3],
                month_of_year=period_content_list[4],
                timezone=pytz.timezone(settings.TIME_ZONE)
            )

            period_obj = PeriodicTask.objects.create(
                crontab=schedule,    # we created this above.
                name=task_name,        # simply describes this periodic task.
                task='celery_tasks.tasks.schedule_task',  # name of task.
                args=json.dumps([task_cmd, hosts_ids]),
            )
            period_beat = period_obj.id

        # 保存任务
        task_schedule_obj = TaskSchedule.objects.create(**{
            'period_beat': period_beat,  # celery-beat的任务id值
            'period_way': period_way,
            'task_cmd': task_cmd,
            'period_content': period_content,
            'task_name': task_name,
            'period_status': 1,  # 默认为激活状态
        })

        for host_id in hosts_ids:
            TaskHost.objects.create(**{
                'tasks_id': task_schedule_obj.id,
                'hosts_id': host_id,
            })

        return Response({'errmsg': 'ok'})

class TaskDetaiView(APIView):
    def put(self, request, pk):
        """激活/禁用计划任务"""
        try:
            task = PeriodicTask.objects.get(id=pk)
        except:
            return Response({"errmsg":" 当前任务不存在 ！"}, status=status.HTTP_400_BAD_REQUEST)

        task.enabled = not task.enabled
        task.save()

        return Response({"errmsg": "ok"})