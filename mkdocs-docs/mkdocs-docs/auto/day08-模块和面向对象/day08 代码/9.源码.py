from rest_framework.views import APIView


class UserAPI(APIView):
    def options(self, request, *args, **kwargs):
        pass
