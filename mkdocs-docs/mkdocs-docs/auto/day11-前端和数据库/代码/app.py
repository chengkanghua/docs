import copy
from flask import Flask, render_template, Markup, request

app = Flask(__name__)

MENU_LIST = [
    {
        'title': "用户中心",
        'icon': "fa-cubes",
        'class': "hide",
        'children': [
            {"title": "管理中心", "url": "/home"},
            {"title": "用户中心", "url": "/user"},
        ]
    },
    {
        'title': "VIP中心",
        'icon': "fa-drivers-license",
        'class': "hide",
        'children': [
            {"title": "VIP管理", "url": "/vip"},
            {"title": "订单管理", "url": "/order"},
        ]
    },
]


@app.template_global()
def menu_html():
    """ 页面访问时，自动执行这个函数"""
    menu_list = copy.deepcopy(MENU_LIST)
    for item in menu_list:
        for child in item['children']:
            if child['url'] == request.path:
                child['class'] = 'active'
                item['class'] = ""

    # 寻找HTML文件 + 渲染 + 数据
    return Markup(render_template("menu.html", menu_list=menu_list))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    """ 管理中心 """

    # import pymysql
    #
    # # 连接MySQL，自动执行 use userdb; -- 进入数据库
    # conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db='userdb')
    # cursor = conn.cursor()
    #
    # # 查询
    # cursor.execute("select * from 表名 where id>10")
    # data = cursor.fetchall()
    # print(data)  # [(),(),()]
    #
    # # 关闭连接
    # cursor.close()
    # conn.close()


    return render_template('home.html')


@app.route('/user')
def user():
    """ 用户管理 """
    return render_template('user.html')


@app.route('/vip')
def vip():
    return render_template('vip.html')


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


if __name__ == '__main__':
    app.run()
