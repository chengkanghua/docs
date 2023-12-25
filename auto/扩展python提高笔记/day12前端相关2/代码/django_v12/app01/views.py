from django.shortcuts import render
from django.http import JsonResponse


def api(request):
    """ 接收vue前端发送的请求，然后返回结果即可。 """
    print("接收到请求了")

    res = {
        'status': True,
        'values': ["alex", "李杰", "土鳖","土包子"]
    }
    data = JsonResponse(res, json_dumps_params={"ensure_ascii": False})
    data['Access-Control-Allow-Origin'] = "*"
    return data
