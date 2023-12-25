from flask import Flask

app = Flask(__name__)


#  对应关系：
#       /index    ->     index函数
#       /login    ->     login函数


@app.route("/index")  # @decorator
def index():
    # 处理所有的请求...
    return "欢迎使用xxx系统"


@app.route("/login")  # @decorator
def login():
    # 处理所有的请求...
    return "欢迎登陆"


if __name__ == '__main__':
    app.run()
