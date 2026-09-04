from django.db import models
from host.models import Host


# Create your models here.
class TaskSchedule(models.Model):
    period_way_choices = (
        (1, '普通计划任务'),  # 普通的异步任务
        (2, '定时一次任务'),  # 定时一次异步任务
        (3, '周期计划任务'),  # 定时多次异步任务
    )

    status_choices = (
        (1, '激活'),
        (2, '停止'),
        (3, '报错'),
    )

    period_beat = models.IntegerField(verbose_name='任务ID', help_text='django-celery-beat调度服务的任务ID，方便我们通过这个id值来控制celery的任务状态', null=True, blank=True)
    task_name = models.CharField(max_length=150, unique=True, verbose_name='任务名称')
    task_cmd = models.TextField(verbose_name='任务指令')
    period_way = models.IntegerField(choices=period_way_choices, default=1, verbose_name='任务周期方式')
    period_content = models.CharField(max_length=32, verbose_name='任务执行周期')
    period_status = models.IntegerField(choices=status_choices, default=1)

    class Meta:
        db_table = "schedule_taskschedule"
        verbose_name = "任务记录表"
        verbose_name_plural = verbose_name


class TaskHost(models.Model):
    tasks = models.ForeignKey('TaskSchedule',on_delete=models.CASCADE,verbose_name='执行的任务')
    hosts = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='任务执行主机')

    class Meta:
        db_table = "schedule_taskhost"  # 切换选中内容中的字母大小写：ctrl+Shift+U
        verbose_name = "任务和主机的关系表"
        verbose_name_plural = verbose_name
