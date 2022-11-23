import re

'''正则 匹配'''

# 手机号匹配
def cellphone(text):
    return re.match("^1[3-9]\d{9}$", text)

# email匹配
def email(text):
    return re.match("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$", text)

# 用户文本的匹配
def while_input(text, validator=None):
    while True:
        data = input(text).strip()
        if not data:
            print("输入不能为空，请重新输入。")
            continue
        if not validator:
            return data
        if not validator(data):  # email(data)  mobile(data)
            print("格式错误，请重新输入。")
            continue
        return data
