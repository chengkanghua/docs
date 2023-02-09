from django.db import models

# Create your models here.
class BaseModel(models.Model):
    """公共模型"""
    name = models.CharField(max_length=500,default="", null=True, blank=True, verbose_name='名称/标题')
    is_show = models.BooleanField(default=True, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    description = models.TextField(null=True, blank=True, default="", verbose_name="描述信息")

    class Meta:
        # 数据库迁移时，设置了bstract = True的model类不会生成数据库表
        abstract = True

    def __str__(self):
        return self.name