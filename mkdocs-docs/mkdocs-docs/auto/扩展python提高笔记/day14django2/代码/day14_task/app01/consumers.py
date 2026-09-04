from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from app01 import models
import json


class AuditConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 1.用户认证

        # 2. 获取任务
        task_id = self.scope['url_route']['kwargs'].get("tid")

        # 3. 允许创建连接
        self.accept()

        # 4. 数据库中获取任务的所有审批信息并发送给客户端。
        node_data_array = []
        data_list = models.AuditTask.objects.filter(task_id=task_id).order_by("-id")
        mapping = {item.parent_id: item.id for item in data_list}
        for item in data_list:
            # parent, 数据库中值得下一个人（上一级）。
            # parent，上一个人
            # color: "lightgreen" / "lightgrey" / "red"
            color = models.AuditTask.status_mapping[item.status]
            info = {'key': item.id, 'text': item.user, 'color': color}
            pid = mapping.get(item.id)
            if pid:
                info['parent'] = pid
            node_data_array.append(info)

        context = {
            'msg_type': 1,
            'node_data_array': node_data_array
        }

        self.send(json.dumps(context, ensure_ascii=False))

    def websocket_receive(self, message):
        # 接收到用户请求
        task_id = self.scope['url_route']['kwargs'].get("tid")

        # 1. 获取当前登录用户信息

        # 2. 根据发送的信息来进行判定合法性

        # 3. 根据 同意 or 不同意
        text = message['text']  # {'user': '用户', 'type': '同意or不同意'}
        text_dict = json.loads(text)
        user = text_dict['user']
        content = text_dict['type']

        if content == "同意":
            # 3.1 当前流程的状态更新
            audit_object = models.AuditTask.objects.filter(task_id=task_id, user=user).first()
            audit_object.status = 3
            audit_object.save()

            # 3.2 当前节点前端应该变绿
            info = {
                'color': models.AuditTask.status_mapping[audit_object.status],
                'key': audit_object.id,
                'msg_type': 2,
            }
            self.send(json.dumps(info))

            # 3.3 下个状态
            if audit_object.parent:
                audit_object.parent.status = 2
                audit_object.parent.save()

                # 3.4 下个状态的状态编程亮绿色
                info = {
                    'color': models.AuditTask.status_mapping[audit_object.parent.status],
                    'key': audit_object.parent.id,
                    'msg_type': 2,
                }
                self.send(json.dumps(info))

        else:
            # 3.1 当前流程的状态更新
            audit_object = models.AuditTask.objects.filter(task_id=task_id, user=user).first()
            audit_object.status = 4
            audit_object.save()

            # 3.2 当前节点前端应该变绿
            info = {
                'color': models.AuditTask.status_mapping[audit_object.status],
                'key': audit_object.id,
                'msg_type': 2,
            }
            self.send(json.dumps(info))

    def websocket_disconnect(self, message):
        print("断开连接了")
        raise StopConsumer()
