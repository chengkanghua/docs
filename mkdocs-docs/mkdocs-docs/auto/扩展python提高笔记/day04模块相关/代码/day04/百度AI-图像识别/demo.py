import requests
import base64


def register_image(user_id, user_info, file_object, group_id="test"):
    # 1. 去百度AI获取 access token
    # client_id 为官网获取的AK，        client_secret 为官网获取的SK
    #  INgt7t4eNaXZ4AoeN2cQICzi    QgApMABK25gVxs8p1ck9Sh9MrSL8Y12R
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=INgt7t4eNaXZ4AoeN2cQICzi&client_secret=QgApMABK25gVxs8p1ck9Sh9MrSL8Y12R'
    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 2. 图片进行base64编码
    data = base64.b64encode(file_object.read())

    # 3. 上传图片
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": access_token
        },
        data={
            "image": data,
            "image_type": "BASE64",
            "group_id": group_id,
            "user_id": user_id,
            "user_info": user_info,
        }
    )
    result = res.json()
    print(result)
    # return result["result"]['face_token']


def search(file_object):
    # 1. 获取 access token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=INgt7t4eNaXZ4AoeN2cQICzi&client_secret=QgApMABK25gVxs8p1ck9Sh9MrSL8Y12R'
    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 2. 图片进行base64编码
    data = base64.b64encode(file_object.read())

    # 3. 检验图片
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/face/v3/search",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": access_token
        },
        data={
            "image": data,
            "image_type": "BASE64",
            "group_id_list": "test",
            "match_threshold": 80,
            "liveness_control": "NONE",
        }
    )
    # {'error_code': 223120, 'error_msg': 'liveness check fail', 'log_id': 8484101891584, 'timestamp': 1618122995, 'cached': 0, 'result': None}
    # {'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 9425255594947, 'timestamp': 1618123184, 'cached': 0, 'result': {'face_token': 'dce2981ea3ae849a4402dd422de25d98', 'user_list': [{'group_id': 'test', 'user_id': 'alex', 'user_info': '', 'score': 100}]}}
    # {"error_code":0,"error_msg":"SUCCESS","log_id":8975998965357,"timestamp":1593273355,"cached":0,"result":{"face_token":"daf9ead990ef00738ab842801e7d212c","user_list":[{"group_id":"test","user_id":"wupeiqi","user_info":"","score":97.43611907959}]}}
    ret = res.json()

    print(ret)
    return ret


if __name__ == '__main__':
    file_object = open('alex.png', mode='rb')
    # register_image("alex", "", file_object)
    search(file_object)
