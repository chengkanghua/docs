import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# SQLAlchemy初始化
db = SQLAlchemy()

app = Flask(__name__)

jwt = JWTManager()

def init_app():
    """服务端初始化"""
    # 加载配置
    app.config.from_object(config)
    # 加载mysql数据库配置
    db.init_app(app)

    # jwt初始化
    jwt.init_app(app)

    # 自动创建数据表
    with app.app_context():
        db.create_all()

    return app