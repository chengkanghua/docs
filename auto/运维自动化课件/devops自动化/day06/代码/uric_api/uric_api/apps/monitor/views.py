from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import MonitorHost, MonitorParams
from .serializers import MonitorParamsModelSerializer, MonitorHostModelSerlaizer
from host.models import Host
from uric_api.utils.key import PkeyManager
from django.conf import settings
from uric_api.utils.ssh import SSHParamiko

# Create your views here.
class MonitorParamViewSet(ModelViewSet):
    """监控参数类型"""
    queryset = MonitorParams.objects.all()
    serializer_class = MonitorParamsModelSerializer


class NotificationTypeAPIView(APIView):
    """获取监控的通知类型"""
    def get(self, request):
        return Response(MonitorHost.NOTIFICATION_TYPE)

class MonitorHostViewSet(ModelViewSet):
    """监控主机列表"""
    queryset = MonitorHost.objects.all()
    serializer_class = MonitorHostModelSerlaizer

    def create(self, request, *arg, **kwargs):
        # 根据上传的主机ID，使用parmiko基于ssh协议上传监控监本
        host_id = request.data.get("host")
        host = Host.objects.filter(id=host_id).first()
        pkey, _ = PkeyManager.get(settings.DEFAULT_KEY_NAME)  # 获取ssh秘钥
        ssh = SSHParamiko(host.ip_addr, host.port, host.username, pkey)
        ssh.get_connected_client()
        # 基于ssh上传文件
        fl = open(settings.MONITOR_SCRIPT, "rb")
        ssh.upload_file(fl, settings.REMOTE_MONITOR_SCRIPT_PATH.replace("~", ssh.execute_cmd("cd ~ && pwd")[1][:-1]))
        return super().create(request, *arg, **kwargs)
