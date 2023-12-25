"""
假设传送的参数如下：
{
    appid： wxd930ea5d5a258f4f
    mch_id： 10000100
    device_info： 1000
    body： test
    nonce_str： ibuaiVcKdpRxkhJA
}

第一步：对参数按照key=value的格式，并按照参数名 ASCII 字典序排序如下：
stringA="appid=wxd930ea5d5a258f4f&body=test&device_info=1000&mch_id=10000100&nonce_str=ibuaiVcKdpRxkhJA";

"""

import hashlib


def md5(origin):
    m = hashlib.md5()
    m.update(origin.encode('utf-8'))
    return m.hexdigest()


key = "192006250b4c09247ec02edce69f6a2d"
info = {
    "appid": "wxd930ea5d5a258f4f",
    "mch_id": "10000100",
    "device_info": "1000",
    "body": "test",
    "nonce_str": "ibuaiVcKdpRxkhJA",
}

# 示例1
"""
data = sorted(info.items(), key=lambda x: x[0])
temp_list = []
for item in data:
    ele = "{}={}".format(*item)
    temp_list.append(ele)
string = "&".join(temp_list)
string_sign_temp = string + "&key={}".format(key)
sign = md5(string_sign_temp).upper()
info['sign'] = sign

result_list = []
for k, v in info.items():
    ele = "<{0}>{1}</{0}>".format(k, v)
    result_list.append(ele)
result = "<xml>{}</xml>".format("".join(result_list))
print(result)
"""

# 示例2
"""
string = "&".join(["{}={}".format(*item) for item in sorted(info.items(), key=lambda x: x[0])])
string_sign_temp = string + "&key={}".format(key)
sign = md5(string_sign_temp).upper()
info['sign'] = sign
result = "<xml>{}</xml>".format("".join(["<{0}>{1}</{0}>".format(k, v) for k, v in info.items()]))
print(result)
"""
