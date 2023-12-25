from flask import Flask, request, session
from flask import globals

app = Flask(__name__)
app.secret_key = "asdfasdf "


@app.route("/")
def index():
    # 用来获取 URL中传递的参数值，例如：http://127.0.0.1:5000/?name=123&age=123
    print(request.args)
    session['k1'] = 123
    return "首页"


if __name__ == '__main__':
    app.run()
