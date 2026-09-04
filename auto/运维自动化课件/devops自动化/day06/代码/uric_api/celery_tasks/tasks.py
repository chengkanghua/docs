from .main import app

# 经过@app.task装饰过，就会被celery识别为任务，否则就是普通的函数
@app.task
def task1():
    print("任务1函数正在执行....")

@app.task
def task2(a, b, c):
    print(f"任务2函数正在执行，参数：{[a, b, c]}....")

@app.task
def task3():
    print(f"任务3函数正在执行....")
    return True

@app.task
def task4(a, b, c):
    print(f"任务4函数正在执行....")
    return a, b, c


import json
from host.models import Host
from django.conf import settings
from uric_api.utils.key import PkeyManager
@app.task(name='schedule_task')
def schedule_task(cmd, hosts_ids):
    """计划任务"""
    hosts_objs = Host.objects.filter(id__in=hosts_ids)
    result_data = []
    private_key, public_key = PkeyManager.get(settings.DEFAULT_KEY_NAME)
    for host_obj in hosts_objs:
        cli = host_obj.get_ssh(private_key)
        code, result = cli.exec_command(cmd)
        result_data.append({
            'host_id': host_obj.id,
            'host': host_obj.ip_addr,
            'status': code,
            'result': result
        })
        print('>>>>', code, result)

    return json.dumps(result_data)