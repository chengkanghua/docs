import requests
from bs4 import BeautifulSoup

# 1.请求并获取结构
res = requests.get("https://www.autohome.com.cn/news/")
text = res.content.decode('gbk')

# 2.获取我们想要的数据
#   - 正则表达式，费劲
#   - bs4，简单
soup = BeautifulSoup(text, features='html.parser')

# 2.1 获取新闻的区域 对象
area_object = soup.find(name='div', attrs={"id": "auto-channel-lazyload-article"})

# 2.2 在之前的基础上找所有的li标签，得到的是列表 [对象,对象,对象]
li_object_list = area_object.find_all(name='li')

# 2.3 循环所有的li_object_list对象
for obj in li_object_list:
    # 2.4 每个li中寻找h3标签
    # 标题
    h3_object = obj.find(name='h3')
    if not h3_object:
        continue
    title = h3_object.text  # <h3>吉利特别股东大会通过增持极氪股份议案</h3>

    # 简介
    p_object = obj.find(name='p')
    summary = p_object.text

    # 图片
    img_object = obj.find(name='img')
    src = img_object.attrs['src']

    # 链接
    a_object = obj.find(name='a')
    url = a_object.attrs['href']
    url_string = "https:{}".format(url)

    print(title)
    print(summary)
    print(src)
    print(url_string)
    print('-' * 30)
