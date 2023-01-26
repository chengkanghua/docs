from flask import request
from sqlalchemy import or_
from flask_jwt_extended import jwt_required, create_access_token

from . import app
from .models import User,db


@app.route("/user/register", methods=["POST"])
def register():
    """
    用户信息注册
    :return:
    """
    try:
        data = request.json
        # 创建用户数据
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {"msg": "注册成功！", "data": {"id":user.id, "name": user.name}}, 200
    except Exception as e:
        return {"msg": "注册失败！", "data": {}}, 400


@app.route("/user/login", methods=["POST"])
def login():
    """
    用户登录
    :return:
    """
    user = User.query.filter(
        or_(
            User.mobile == request.json.get("username"),
            User.name == request.json.get("username"),
            User.email == request.json.get("username")
        )
    ).first()  # 实例化模型

    if not user:
        return {"msg": "登录失败！用户不存在！", "data": {}}, 400

    if not user.check_password(request.json.get("password")):
        return {"msg": "登录失败！密码错误！", "data": {}}, 400

    # 生成token，并返回给客户端
    access_token = create_access_token(identity={"id": user.id, "username": user.name})
    return {"msg": "登录成功", "data": {"token": access_token}}, 200


@app.route("/user", methods=["GET"])
@jwt_required()   # 当前这个装饰器的作用就是 校验用户是否登录
def user_center():
    return {"errmsg": "访问成功"}