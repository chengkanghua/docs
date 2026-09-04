from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True, verbose_name='手机号码')
    # upload_to 表示上传文件的存储子路由，需要在settings配置中，配置上传文件的支持
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True)

    class Meta:
        db_table = 'uric_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


# 下面的3个表现不用创建，留着以后使用
class Menu(models.Model):
    """
    一级菜单表
    """
    title = models.CharField(max_length=12)
    weight = models.IntegerField(default=0)
    icon = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'uric_menu'
        verbose_name = '一级菜单表'
        verbose_name_plural = verbose_name
        unique_together = ('title', 'weight')


class Permission(models.Model):
    url = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    menus = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    url_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'uric_permission'
        verbose_name = '权限表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    name = models.CharField(max_length=12)
    permissions = models.ManyToManyField(to='Permission')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'uric_role'
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
