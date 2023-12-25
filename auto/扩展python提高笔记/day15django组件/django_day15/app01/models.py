from django.db import models


class UserInfo(models.Model):
    title = models.CharField(verbose_name="标题", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    # xx = models.IntegerField(verbose_name="xx")
    # 要删除xx列
