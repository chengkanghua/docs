from django.db import models
from host.models import Host
from uric_api.utils.models import BaseModel


class MonitorParams(BaseModel):
    """监控参数类型"""
    class Meta:
        db_table = "monitor_params"
        verbose_name = "监控参数类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MonitorHost(models.Model):
    """监控的主机列表"""
    NOTIFICATION_TYPE = (
        (0, "邮件通知"),
        (1, "短信通知"),
        (2, "微信通知"),
        (3, "钉钉通知"),
    )
    host = models.ForeignKey(Host, on_delete=models.DO_NOTHING, verbose_name='主机')
    times = models.CharField(max_length=255, verbose_name="时间间隔")
    param = models.ForeignKey(MonitorParams, default=None, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="监控参数")
    value = models.FloatField(default=0, null=True, blank=True, verbose_name="预警阈值")
    notification_type = models.SmallIntegerField(choices=NOTIFICATION_TYPE, default=0, verbose_name="通知类型")
    notification_info = models.CharField(default=None, null=True, blank=True, max_length=500, verbose_name="通知人")

    class Meta:
        db_table = "monitor_host"
        verbose_name = "监控主机列表"
        verbose_name_plural = verbose_name
