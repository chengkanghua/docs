from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/show')
def show():
    # return "成功"
    # return jsonify({"status": True, 'message': "xxxx"})
    return render_template("show.html")


if __name__ == '__main__':
    app.run()
