import os
import sys
import django
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "day14_task.settings")
django.setup()  # 伪造让django启动

from app01 import models

"""
 var nodeDataArray = [
    {key: "start", text: '开始', figure: 'Ellipse', color: "lightgreen"},
    {key: "download", parent: 'start', text: '下载代码', color: "lightgreen", link_text: '执行中...'},
    {key: "compile", parent: 'download', text: '本地编译', color: "lightgreen"},
    {key: "zip", parent: 'compile', text: '打包', color: "red", link_color: 'red'},
    {key: "c1", text: '服务器1', parent: "zip"},
    {key: "c11", text: '服务重启', parent: "c1",color: "lightgrey"},
    {key: "c2", text: '服务器2', parent: "zip"},
    {key: "c21", text: '服务重启', parent: "c2"},
    {key: "c3", text: '服务器3', parent: "zip"},
    {key: "c31", text: '服务重启', parent: "c3"},
];
"""
node_data_array = []

data_list = models.AuditTask.objects.filter(task_id=1).order_by("-id")
mapping = {item.parent_id: item.id for item in data_list}
for item in data_list:
    # parent, 数据库中值得下一个人（上一级）。
    # parent，上一个人
    # color: "lightgreen" / "lightgrey" / "red"
    color = models.AuditTask.status_mapping[item.status]
    info = {'key': item.id, 'text': item.user, 'parent': mapping.get(item.id), 'color': color}
    node_data_array.append(info)

print(json.dumps(node_data_array, indent=2, ensure_ascii=False))
