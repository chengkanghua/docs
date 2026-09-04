import re


# 验证 email
def email(text):
    return re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$', text)


# 验证cellphone
def cellphone(text):
    return re.match('^1[3-9]\d{9}', text)


# 验证输入字符串的
def while_input(text, validator=None):
    while True:
        data = input(text).strip()
        if data.upper() == 'Q':
            return
        if not data:
            continue
        if not validator:
            return data
        if not validator(data):
            print('格式出错, 请重试')
            continue
        return data
