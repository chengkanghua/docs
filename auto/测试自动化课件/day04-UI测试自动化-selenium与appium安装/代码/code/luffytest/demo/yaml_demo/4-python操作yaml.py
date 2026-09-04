import yaml
"""读取yaml文件的数据"""
# with open("./data.yaml", "r",encoding="utf-8") as f:
#     content = f.read()
#     data = yaml.load(content, Loader=yaml.FullLoader)
#     print(data)
#     print(data["name"])


"""把数据写入yaml文件"""
from datetime import datetime


with open("data2.yaml", "w", encoding="utf-8") as f:
    # yaml.dump(data, f, Dumper=yaml.SafeDumper) # 没有多字节内容的情况下
    data = {
        "name": "xiaoming",
        "age": 17,
        "datetime": datetime.now(),
        "point": 1.245464E10,
        "goods_list": [
            {"name": "xiaoming","age": 17, "sex": True},
            {"name": "xiaoming","age": 17, "sex": True},
            {"name": "xiaoming","age": 17, "sex": True},
            {"name": "xiaoming","age": 17, "sex": True},
        ],
        "author_list": ["小明", "小白", "小红"],
        "user_info": {"username":"小明", "password": "123456"}
    }
    yaml.dump(data, f, Dumper=yaml.SafeDumper, allow_unicode=True)  # 有多字节内容的情况下，中文就是多字节内容