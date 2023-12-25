from django.db import models

# Create your models here.
from uric_api.utils.models import BaseModel
from conf_center.models import Environment
from django.db import models

# Create your models here.
from uric_api.utils.models import BaseModel, models
from users.models import User


class HostCategory(BaseModel):
    """主机类别"""

    class Meta:
        db_table = "host_category"
        verbose_name = "主机类别"
        verbose_name_plural = verbose_name  # 取消提示文字中关于英文复数+s的情况


class Host(BaseModel):
    # 真正在数据库中的字段实际上叫 category_id，而category则代表了关联的哪个分类模型对象
    category = models.ForeignKey('HostCategory', on_delete=models.DO_NOTHING, verbose_name='主机类别', related_name='hc', null=True, blank=True)
    ip_addr = models.CharField(blank=True, null=True, max_length=500, verbose_name='连接地址')
    port = models.IntegerField(verbose_name='端口')
    username = models.CharField(max_length=50, verbose_name='登录用户')
    users = models.ManyToManyField(User)
    environment = models.ForeignKey(Environment, on_delete=models.DO_NOTHING, default=1, verbose_name='从属环境')

    class Meta:
        db_table = "host"
        verbose_name = "主机信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + ':' + self.ip_addr


# 全局密钥和共钥，所有用户都使用这个一对
class PkeyModel(BaseModel):
    name = models.CharField(max_length=32, unique=True)  # 名称
    private = models.TextField(verbose_name="私钥")
    public = models.TextField(verbose_name="公钥")

    def __repr__(self):
        return f'<Pkey {self.name}>'
