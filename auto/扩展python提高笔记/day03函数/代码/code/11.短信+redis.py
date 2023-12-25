import random
import ssl
import redis

ssl._create_default_https_context = ssl._create_unverified_context
from qcloudsms_py import SmsMultiSender, SmsSingleSender
from qcloudsms_py.httpclient import HTTPError


def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = 1400498873  # 自己应用ID
    appkey = "8c9c327fb51d447183e8015c66d54e15"  # 自己应用Key
    sms_sign = "Python之路"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


def run():
    print("欢迎使用xxx系统")
    mobile_phone = input("请输入手机号：")
    # 1.生成一个随机验证码
    random_int = random.randint(1000, 9999)
    # 2.发送短信
    send_sms_single(mobile_phone, 548760, [random_int, ])


    # 3.验证码保存到redis
    conn = redis.Redis(host='127.0.0.1', port=6379, password='qwe123', encoding='utf-8')
    conn.set(mobile_phone, random_int, ex=60)  # 15131255089=1889   60

    print("短信验证码已发送成功")
    code = input("请输入验证码：")

    # 校验验证码是否正确/是否已使用。。。
    # 4.去redis中根据手机号读取短信验证码
    sms_code = conn.get(mobile_phone)
    if not sms_code:
        print("验证码失效")
        return

    # 5.读取验证码，字节类型
    sms_code = sms_code.decode('utf-8')
    if code != sms_code:
        print("验证码输入错误")
        return

    conn.delete(mobile_phone)  # 在redis中将手机号对应的验证码删除（？）。
    print("登录成功")


if __name__ == '__main__':
    run()
