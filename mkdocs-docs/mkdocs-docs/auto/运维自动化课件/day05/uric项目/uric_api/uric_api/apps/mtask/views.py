from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from host.models import Host
from uric_api.utils.key import PkeyManager
from django.conf import settings
from rest_framework.response import Response
from uric_api.utils.ssh import SSHParamiko


# Create your views here.
class CmdExecView(APIView):
    def post(self, request):
        host_ids = request.data.get('host_ids')
        cmd = request.data.get('cmd')
        print("host_ids", host_ids)
        if host_ids and cmd:
            exec_host_list = Host.objects.filter(id__in=host_ids)
            pkey, _ = PkeyManager.get(settings.DEFAULT_KEY_NAME)  # 获取ssh秘钥
            response_list = []
            for host in exec_host_list:
                ssh = SSHParamiko(host.ip_addr, host.port, host.username, pkey)
                ssh.get_connected_client()
                # ssh 远程执行指令
                res_code, res_data = ssh.execute_cmd(cmd)
                # res_code为0表示ok，不为0说明指令执行有问题
                response_list.append({
                    'host_info': {
                        'id': host.id,
                        'name': host.name,
                        'ip_addr': host.ip_addr,
                        'port': host.port,
                    },
                    'res_code': res_code,
                    'res_data': res_data,
                })
            return Response(response_list)

        else:
            return Response({'error': '没有该主机或者没有输入指令'}, status=400)


from rest_framework.generics import ListAPIView, CreateAPIView
from .models import CmdTemplate, CmdTemplateCategory
from .serializers import CmdTemplateModelSerialzer, CmdTemplateCategoryModelSerialzer
from rest_framework.permissions import IsAuthenticated


class TemplateView(ListAPIView, CreateAPIView):
    # 获取所有执行模板
    permission_classes = [IsAuthenticated]
    queryset = CmdTemplate.objects.all()
    serializer_class = CmdTemplateModelSerialzer


class TemplateCategoryView(ListAPIView, CreateAPIView):
    # 获取执行模板类别
    permission_classes = [IsAuthenticated]
    queryset = CmdTemplateCategory.objects.all()
    serializer_class = CmdTemplateCategoryModelSerialzer