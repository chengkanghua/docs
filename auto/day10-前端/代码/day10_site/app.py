from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/index')
def index():
    # 1.去数据库获取数据
    db_list = [
        {"id": 1, "title": "python全栈"},
        {"id": 2, "title": "自动化开发"},
    ]
    title = "数据列表222"
    # 2.利用Flask里面的模板引擎
    #   - 读取HTML文件作为模板：单独数据的替换+循环
    #   - 替换
    return render_template('index.html', x1=title, x2=db_list)


@app.route('/table')
def table():
    return render_template('table.html')


@app.route('/demo')
def demo():
    return render_template('demo.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/sub')
def sub():
    return render_template('sub.html')


@app.route('/cc', methods=["GET", "POST"])
def cc():
    # 接收用户提交过来的数据 GET
    # print(request.args)

    # 去请求体中获取数据POST
    print(request.form)
    print(request.files)
    return "OK"


@app.route('/css')
def css():
    return render_template('css.html')


@app.route('/boot')
def boot():
    return render_template('boot.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run()
