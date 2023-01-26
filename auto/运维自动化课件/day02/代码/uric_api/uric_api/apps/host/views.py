from rest_framework.views import APIView

from rest_framework.response import Response


class HostView(APIView):

    def get(self, reqeust):
        data = [{"name": "主机1", "port": 22}, {"name": "主机2", "port": 22}]
        print(data)
        return Response(data)

    def delete(self, reqeust):
        return Response("DELETE!")
