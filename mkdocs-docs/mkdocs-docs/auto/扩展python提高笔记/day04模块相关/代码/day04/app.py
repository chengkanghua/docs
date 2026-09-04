from flask import Flask,render_template

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('video.html')


if __name__ == '__main__':
    app.run()