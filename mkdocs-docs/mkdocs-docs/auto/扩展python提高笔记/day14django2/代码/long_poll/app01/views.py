import queue
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

USER_QUEUE = {}


def home(request):
    uid = request.GET.get('uid')   #uid最开始是浏览器地址栏传递过来的 127.0.0.1/home/?uid=alex
    USER_QUEUE[uid] = queue.Queue()
    return render(request, 'home.html', {"uid": uid})


def send_msg(request):
    text = request.GET.get('text')
    for uid, q in USER_QUEUE.items():
        q.put(text)
    return HttpResponse("ok")


def get_msg(request):
    # 去自己的队列获取数据，把你的uid告诉我
    uid = request.GET.get('uid')
    q = USER_QUEUE[uid]  # 获取自己的队列

    result = {'status': True, 'data': None}
    try:
        data = q.get(timeout=10)
        result["data"] = data
    except queue.Empty as e:
        result['status'] = False

    return JsonResponse(result)
