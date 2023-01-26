from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse

class M1(MiddlewareMixin):

    def process_request(self, request):
        print("IP:", request.META.get("REMOTE_ADDR"))
        print("m1 process_request")

        # return None代表通过
        if request.META.get("REMOTE_ADDR") != "127.0.0.1":
            return
        else:
            return HttpResponse("禁止本机访问")

    def process_response(self, request, response):
        print("m1 process_response")
        return response


class M2(MiddlewareMixin):

    def process_request(self, request):
        print("m2 process_request")

    def process_response(self, request, response):
        print("m2 process_response")
        print("response:", response.content)
        response.content = b"Hello " + response.content
        return response
