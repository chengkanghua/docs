from rest_framework import serializers
from .models import MonitorParams, MonitorHost

class MonitorParamsModelSerializer(serializers.ModelSerializer):
    """监控参数类型的序列化器"""
    class Meta:
        model = MonitorParams
        fields = ["id", "name", "description"]


class MonitorHostModelSerlaizer(serializers.ModelSerializer):
    """监控主机的序列化器"""
    host_name = serializers.CharField(source="host.name", read_only=True)
    host_ip_addr = serializers.CharField(source="host.ip_addr", read_only=True)
    host_port = serializers.IntegerField(source="host.port", read_only=True)
    param_name = serializers.CharField(source="param.name", read_only=True)
    param_description = serializers.CharField(source="param.description", read_only=True)

    class Meta:
        model = MonitorHost
        fields = ["id", "host", "host_name", "host_ip_addr", "host_port", "times", "param", "param_name", "param_description", "value", "notification_type", "get_notification_type_display", "notification_info"]
