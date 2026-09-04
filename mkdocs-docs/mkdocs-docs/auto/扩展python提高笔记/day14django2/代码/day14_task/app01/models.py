from django.db import models


class Task(models.Model):
    """ 工单/任务表，请假/购买/调休... """
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="描述", null=True, blank=True)


class AuditTask(models.Model):
    """ 审批记录 """
    task = models.ForeignKey(verbose_name="任务/工单", to="Task", on_delete=models.CASCADE)

    status_choices = (
        (1, "未审批"),
        (2, "待审批"),
        (3, "通过"),
        (4, "未通过"),
    )
    status_mapping = {
        1: "lightgrey",
        2: "lightgreen",
        3: "green",
        4: "red",
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)

    # 假设用户
    user = models.CharField(verbose_name="审批者", max_length=32)

    parent = models.ForeignKey(
        verbose_name="上一级（下一个）",
        to="AuditTask",
        null=True,
        blank=True,
        related_name="tasks",
        on_delete=models.CASCADE
    )
