import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.autohome.com.cn/news/")
text = res.content.decode('gbk')
soup = BeautifulSoup(text, features='html.parser')

area_object = soup.find(name='ul', attrs={"id": "tagInfo"})

li_object_list = area_object.find_all(name='li')
for obj in li_object_list:
    div_object = obj.find(name='div',attrs={'class':"editorname"})
    # print(div_object.text)
    a_object = div_object.find(name='a')
    print(a_object.text)
