import copy
from datetime import timedelta
from flask import Flask, render_template, Markup, request, redirect, session

import pymysql
from utils import db

app = Flask(__name__)
app.secret_key = "asdfasdfj;alksjdfpoiausd;fkjhasdf"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=7)

MENU_LIST = [
    {
        'title': "课程管理",
        'icon': "fa-drivers-license",
        'class': "hide",
        'children': [
            {"title": "学科", "url": "/course"},
            {"title": "模块", "url": "/module"},
        ]
    },

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
            # /course/detail?cid=1     "/course"
            if request.path.startswith(child['url']):
                child['class'] = 'active'
                item['class'] = ""

    # 寻找HTML文件 + 渲染 + 数据
    return Markup(render_template("menu.html", menu_list=menu_list))


@app.before_request
def auth():
    if request.path.startswith("/static"):
        return

    if request.path == "/login":
        return

    current_user = session.get('user_name')
    if current_user:
        return

    return redirect('/login')


@app.route('/course')
def course():
    """ 学科管理 """

    data_list = db.fetch_all("select id,title,qq from course")
    # data_list = db.fetch_all("select id,title,qq from course where id>%s and id<%s", 3, 16)
    # data_list = db.fetch_all("select id,title,qq from course where id>%s and id<%s", *[3, 16])
    # data_list = db.fetch_all("select id,title,qq from course where id>%(n1)s and id<%(n2)s", n1=3, n2=16)
    # data_list = db.fetch_all("select id,title,qq from course where id>%(n1)s and id<%(n2)s", **{"n1":3, "n2":16})

    return render_template('course.html', data_list=data_list)


@app.route('/course/detail')
def course_detail():
    """ 学科详细 """
    # http://127.0.0.1:8888/course/detail?cid=1
    # 1.获取要查看的详细学科的ID
    cid = request.args.get("cid")  # 1;delete from  course;
    data_dict = db.fetch_one("select * from course where id=%s", cid)

    # 3.判断是否为空
    if not data_dict:
        return "请求数据不存在"

    # 4.页面展示出来
    return render_template('course_detail.html', x2=data_dict, x3=[11, 22, 33])


@app.route('/course/add', methods=["GET", "POST"])
def course_add():
    """ 创建学科 """
    if request.method == 'GET':
        return render_template('course_add.html')

    user_dict = request.form.to_dict()
    db.execute(
        "insert into course(title,summary,qq,qq_link)values(%(title)s,%(summary)s,%(qq)s,%(qq_link)s)",
        **user_dict
    )

    # 3.跳转到学科列表页面
    return redirect("/course")


@app.route('/course/delete')
def course_delete():
    """ 删除学科 """
    # 1.获取通过GET在URL中传入的参数
    cid = request.args.get('cid')

    # 2.在数据库删除
    db.execute("delete from course where id=%s", cid)

    # 3.返回到学科列表
    return redirect('/course')


@app.route('/course/edit', methods=["GET", "POST"])
def course_edit():
    """ 编辑学科 """
    if request.method == "GET":
        cid = request.args.get("cid")
        # 1.去数据库或者词条数据的详细信息
        data_dict = db.fetch_one("select * from course where id=%s", cid)
        # 2.给前端页面渲染
        # return render_template('course_edit.html', **{"data": data_dict})
        return render_template('course_edit.html', data=data_dict)

    # POST
    # user_dict = request.form.to_dict()
    # cid = request.args.get('cid')
    # user_dict['cid'] = cid

    user_dict = request.values.to_dict()

    db.execute(
        "update course set title=%(title)s,summary=%(summary)s,qq=%(qq)s,qq_link=%(qq_link)s where id=%(cid)s",
        **user_dict
    )

    return redirect('/course')


@app.route('/module')
def module():
    """ 模块列表 """

    # 1.获取所有模块
    # data_list = db.fetch_all("select * from module order by id asc")
    sql = """
        select 
            module.id,
            module.name,
            course.title,
            teacher.name  as tname
        from module
            left join course on module.course_id = course.id   
            left join teacher on module.teacher_id = teacher.id
    """
    data_list = db.fetch_all(sql)

    return render_template("module.html", data_list=data_list)


@app.route('/module/delete')
def module_delete():
    """ 删除模块 """
    # 1.获取通过GET在URL中传入的参数
    mid = request.args.get('mid')

    # 2.在数据库删除
    db.execute("delete from module where id=%s", mid)

    # 3.返回到学科列表
    return redirect('/module')


@app.route('/module/add', methods=["GET", "POST"])
def module_add():
    """ 添加模块 """
    if request.method == "GET":
        course_list = db.fetch_all("select id,title from course order by id desc")
        teacher_list = db.fetch_all("select id,name from teacher order by id asc")
        return render_template('module_add.html', course_list=course_list, teacher_list=teacher_list)

    data_dict = request.form.to_dict()
    db.execute(
        "insert into module(name,detail,course_id,teacher_id) values(%(name)s,%(detail)s,%(course_id)s,%(teacher_id)s)",
        **data_dict)
    return redirect('/module')


@app.route('/module/edit', methods=["GET", "POST"])
def module_edit():
    """ 编辑模块 """
    if request.method == "GET":
        mid = request.args.get("mid")

        current_dict = db.fetch_one("select name,detail,course_id,teacher_id from module where id=%s", mid)
        print(current_dict)

        course_list = db.fetch_all("select id,title from course order by id desc")
        teacher_list = db.fetch_all("select id,name from teacher order by id asc")
        return render_template('module_edit.html', course_list=course_list, teacher_list=teacher_list,
                               current_dict=current_dict)

    # mid = request.args.get("mid")
    # data_dict = request.form.to_dict()
    total_dict = request.values.to_dict()

    db.execute(
        "update module set name=%(name)s,detail=%(detail)s,course_id=%(course_id)s,teacher_id=%(teacher_id)s where id=%(mid)s",
        **total_dict)

    return redirect('/module')


@app.route('/login', methods=["GET", "POST"])
def login():
    """ 用户登录 """
    if request.method == "GET":
        return render_template('login.html')

    # 1.从请求中获取数据
    print(request.form)
    user = request.form.get('user')
    pwd = request.form.get('pwd')

    # 2.去数据库进行校验
    current_dict = db.fetch_one("select * from admin where username=%s and password=%s", user, pwd)
    # 2.1 登录失败
    if not current_dict:
        return render_template('login.html', error="用户名或密码错误")

    # 2.2 登录成功
    #   - 生成随机字符串
    #   - 给用户浏览器返回，写在cookie中
    session['user_name'] = current_dict['username']

    return redirect("/home")


@app.route('/home')
def home():
    """ 管理中心 """
    current_user = session.get('user_name')
    if not current_user:
        # 未登录
        return redirect('/login')
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
    app.run(port=9999, host="0.0.0.0")
