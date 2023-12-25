from flask import Flask, render_template,signals

app = Flask(__name__)

"""
本质：在flask内部维护了一个字典
before_request_funcs= {
    None:[b1,b2]
}

after_request_funcs = {
    None:[a1,a2]
}
在after_request_funcs执行时，会先拿到列表 [a1,a2]，将列表reverse，然后再执行。
"""


@app.before_request
def b1():
    print("b1")


@app.before_request
def b2():
    print("b2")


@app.after_request
def a1(res):
    print("A1")
    return res


@app.after_request
def a2(res):
    print("A2")
    return res


@app.route("/index")
def index():
    print("index函数")
    return render_template("index.html")


@app.route("/login")
def login():
    print("login函数")
    return "欢迎登录"


if __name__ == '__main__':
    app.run()
