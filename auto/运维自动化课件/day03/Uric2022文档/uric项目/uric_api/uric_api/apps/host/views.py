from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated


class HostView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, reqeust):
        data = [
                   {
                       'id': 1,
                       'category_name': '数据库服务器',
                       'name': 'izbp13e05jqwodd605vm3gz',
                       'ip_addr': '47.58.131.12',
                       'port': 22,
                       'remark': ''
                   },
                   {
                       'id': 2,
                       'category_name': '数据库服务器',
                       'name': 'iZbp1a3jw4l12ho53ivhkkZ',
                       'ip_addr': '12.18.125.22',
                       'port': 22,
                       'remark': ''
                   },
                   {
                       'id': 3,
                       'category_name': '缓存服务器',
                       'name': 'iZbp1b1xqfqw257gs563k2iZ',
                       'ip_addr': '12.19.135.130',
                       'port': 22,
                       'remark': ''
                   },
                   {
                       'id': 4,
                       'category_name': '缓存服务器',
                       'name': 'iZbp1b1jw4l01ho53muhkkZ',
                       'ip_addr': '47.98.101.89',
                       'port': 22,
                       'remark': ''
                   }
               ],
        return Response(data)

    def delete(self, reqeust):
        return Response("DELETE响应")
