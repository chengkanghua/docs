from flask import Flask, render_template

# 创建了一个Flask类的对象（在app对象中封装了很多值）
app = Flask(__name__)


@app.route("/index")
def index():
    print("index函数")
    return render_template("index.html")


if __name__ == '__main__':
    app.__call__
    app.run()
