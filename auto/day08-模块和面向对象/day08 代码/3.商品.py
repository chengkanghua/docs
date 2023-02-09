import re
import requests
from bs4 import BeautifulSoup

res = requests.get(url="http://s.10010.com/hebei/mobilelist-0-0-0-0-0-0-0-0-177-0-0-p2/")

soup_object = BeautifulSoup(res.text, 'html.parser')

goods_object_list = soup_object.find_all(name='li', attrs={"class": "goodsLi"})

for goods in goods_object_list:
    # 商品ID
    # goods_id = goods.get("goodsid")
    goods_id = goods.attrs['goodsid']

    # 商品标题
    title = goods.find(name='p', attrs={"class": "mobileGoodsName"}).find(name='a').text

    # 需求1：补充代码实现提取价格中的数字，例如：￥59，则想办法只获取数字部分。
    price_string = goods.find(name="label", attrs={'class': "priceD"}).text

    # 需求2：提取评论数量，例如：已有5人评价，想办法只获取数字部分。
    comment_string = goods.find(name="p", attrs={'class': "evalNum"}).text

    # 需求3：将已处理好的商品ID、价格、评论数量、商品标题写入到Excel文件中。
    print(goods_id, price_string, comment_string, title)
