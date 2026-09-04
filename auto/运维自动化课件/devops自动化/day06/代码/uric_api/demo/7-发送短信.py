import json
import random
from ronglian_sms_sdk import SmsSDK

# 配置文件 settings.py
accId = '8a216da863f8e6c20164139687e80c1b'
accToken = '6dd01b2b60104b3dbc88b2b74158bac6'
appId = '8a216da863f8e6c20164139688400c21'
templateId = 1

# 工具函数 utils/
def send_message(mobile, datas, tid=None):
    sdk = SmsSDK(accId, accToken, appId)
    tid = templateId if tid is None else tid
    resp = sdk.sendMessage(tid, mobile, datas)
    response = json.loads(resp)
    return response


if __name__ == '__main__':
    code = f"{random.randint(100000,999999):06d}"
    resp = send_message('13928835901', (code, 5))
    print(resp)