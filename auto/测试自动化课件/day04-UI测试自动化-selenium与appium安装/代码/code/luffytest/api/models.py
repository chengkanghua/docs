from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(db.Model):
    """公共模型"""
    __abstract__ = True  # 抽象模型
    id = db.Column(db.Integer, primary_key=True, comment="主键ID")
    name = db.Column(db.String(255), default="", comment="名称/标题")
    is_deleted = db.Column(db.Boolean, default=False, comment="逻辑删除")
    orders = db.Column(db.Integer, default=0, comment="排序")
    status = db.Column(db.Boolean, default=True, comment="状态(是否显示,是否激活)")
    created_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    updated_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class User(BaseModel):
    """用户基本信息表"""
    __tablename__ = "py_user"
    name = db.Column(db.String(255), index=True, comment="用户账户")
    nickname = db.Column(db.String(255), comment="用户昵称")
    _password = db.Column(db.String(255), comment="登录密码")
    intro = db.Column(db.String(500), default="", comment="个性签名")
    avatar = db.Column(db.String(255), default="", comment="头像url地址")
    sex = db.Column(db.SmallInteger, default=0, comment="性别")  # 0表示未设置,保密, 1表示男,2表示女
    email = db.Column(db.String(32), index=True, default="", nullable=False, comment="邮箱地址")
    mobile = db.Column(db.String(32), index=True, nullable=False, comment="手机号码")

    @property
    def password(self):  # user.password
        """获取密码的加密串"""
        return self._password

    @password.setter
    def password(self, rawpwd):  # user.password = '123456'
        """密码加密"""
        self._password = generate_password_hash(rawpwd)

    def check_password(self, rawpwd):
        """验证密码"""
        return check_password_hash(self.password, rawpwd)