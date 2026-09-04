from django.db import models


class UserInfo(models.Model):
    login_type_choices = (
        (1, "普通用户"),
        (2, "管理员"),
    )
    login_type = models.IntegerField(verbose_name="用户类型", choices=login_type_choices)
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
