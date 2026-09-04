from django.shortcuts import render, HttpResponse, redirect
from django import forms
from io import BytesIO
from account.utils.check_code import create_validate_code
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError
from account.utils.encrypt import md5
from django.conf import settings
import importlib


class LoginForm(forms.Form):
    """
    用户登录
    """

    login_type = forms.ChoiceField(
        label="用户类型",
        choices=((1, "普通用户"), (2, "管理员")),
    )
    username = forms.CharField(label='用户名')
    password = forms.CharField(
        label='密码',
        # min_length=8,
        # max_length=64,
        # error_messages={
        #     'min_length': "密码长度不能小于8个字符",
        #     'max_length': "密码长度不能大于64个字符"
        # },
        widget=forms.PasswordInput(render_value=True)
    )

    code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

        # 自定义工作：找到每个字段给他插件中加上样式
        for name, field in self.fields.items():
            # if name == "code":
            #     continue
            placeholder = "请输入{}".format(field.label)
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = placeholder

    def clean_code(self):
        # 进行验证码的校验

        # 用户输入的
        code = self.cleaned_data['code']
        # redis中存储的验证码
        conn = get_redis_connection()
        key = "IG_{}".format(self.request.session.session_key)
        redis_code = conn.get(key)  # 键需要用到 request.session.session_key
        if not redis_code:
            raise ValidationError("验证码已失效，请重新获取。")
        if code.lower() != redis_code.decode('utf-8').lower():
            raise ValidationError("验证码错误，请重新输入。")
        conn.delete(key)
        return code

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)


def login(request):
    """ 用户登录 """
    if not request.session.session_key:
        request.session.create()

    if request.method == "GET":
        # 创建Form对象
        form = LoginForm(request)
        # 项目根目录下 templates 中找 login.html
        # 根据app的注册顺序，去每个app的 templates 中找 login.html
        return render(request, "account/login.html", {'form': form})

    form = LoginForm(request, data=request.POST)

    # 验证码校验，redis读取
    # 用户名或密码校验，数据库
    if form.is_valid():
        # 获取用户名和密码数据库校验
        login_type = form.cleaned_data['login_type']  # 1普通用户；2管理员
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # print(login_type, username, password)
        # 去数据库校验即可，不直接去读某一个表。（在settings中让用户去配置，用户表的路径）。
        # 根据反射去找到 "web.models.UserInfo"
        module_path, cls_name = settings.ACCOUNT_LOGIN_MODEL_CLASS.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name)

        user_object = cls.objects.filter(username=username, password=password, login_type=login_type).first()
        if user_object:
            # 登录成功
            request.session[settings.ACCOUNT_SESSION_KEY] = {"pk": user_object.pk, 'name': username}
            request.session.set_expiry(1209600)
            return redirect(settings.ACCOUNT_LOGIN_SUCCESS_URL)
        form.add_error('password', "用户名或密码错误")

    return render(request, "account/login.html", {'form': form})


def check_code(request):
    """ 生成图片验证码 """
    stream = BytesIO()

    # 1. 创建一张图片 PIL模块 & 写随机的验证码
    img_object, code = create_validate_code()
    img_object.save(stream, 'PNG')

    # 2.将验证码写入redis中（以session_key为用户标识）
    # 6zucr361s6pp8lfbsjxqh1unpr41gvye:code
    # print(request.session.session_key)  # None
    # 2.1 启动redis
    # 2.2 django中配置redis
    # 2.3 连接redis去操作

    image_code_key = "{}_{}".format("IG", request.session.session_key)
    conn = get_redis_connection("default")
    conn.set(image_code_key, code, 60)

    # 3.给用户返回
    return HttpResponse(stream.getvalue())


def register(request):
    """ 用户注册 """
    return render(request, "account/register.html")


def logout(request):
    """ 用户注销 """
    pass
