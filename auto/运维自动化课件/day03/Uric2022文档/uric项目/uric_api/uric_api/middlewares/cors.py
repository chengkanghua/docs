from django.utils.deprecation import MiddlewareMixin


class CorsMiddleWare(MiddlewareMixin):

    def process_response(self, request, response):
        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Allow-Methods'] = 'PUT,PATCH,DELETE'

        response["Access-Control-Allow-Origin"] = "*"

        return response
