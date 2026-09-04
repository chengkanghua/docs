import requests
import json

WECHAT_CONFIG = {
    'app_id': 'xxxxxx',
    'appsecret': 'xxxx',
}


def get_access_token():
    """
    获取微信全局接口的凭证(默认有效期俩个小时)
    如果不每天请求次数过多, 通过设置缓存即可
    """
    result = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": WECHAT_CONFIG['app_id'],
            "secret": WECHAT_CONFIG['appsecret'],
        }
    ).json()
    return result.get('access_token')


def send_template_msg(token):
    """
    发送模版消息
    """
    res = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/template/send",
        params={
            'access_token': access_token
        },
        json={
            # "touser": "oko631YbM3Mq-0tewUUVH1rOAAJY",  # 对方 IDoko631YbM3Mq-0tewUUVH1rOAAJY
            "touser": "oko631XUgXCcG_rfbx94mxeB7sjs",  # 对方 IDoko631YbM3Mq-0tewUUVH1rOAAJY
            "template_id": '2KANbVNo_5tKCF0jJsZ1_Z446XLr7iGfalNto3bPVIw',
            "data": {
                "first": {
                    "value": "python开发",
                    "color": "#173177"
                },
                "keyword1": {
                    "value": "沙雕alex",
                    "color": "#173177"
                },
                "keyword2": {
                    "value": "13838383838",
                    "color": "#173177"
                },
            }
        }
    )
    result = res.json()
    print(result)
    return result


if __name__ == '__main__':
    # 1.获取token（向微信发送请求，是否允许我给对方发消息）   ->  redis
    access_token = get_access_token()
    # 2.发送消息
    send_template_msg(access_token)
