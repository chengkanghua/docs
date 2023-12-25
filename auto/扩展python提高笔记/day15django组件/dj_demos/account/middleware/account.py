import importlib
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect


class AccountMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 处理白名单
        # /login/   /check/code/
        current_url = request.path_info
        if current_url in settings.ACCOUNT_WHITE_URL:
            print("在白名单")
            return None

        user_session = request.session.get(settings.ACCOUNT_SESSION_KEY)
        # 1. 用户未登录，返回登录界面（返回值）
        if not user_session:
            return redirect(settings.ACCOUNT_LOGIN_URL)
        # {'pk':xxx,"name":xx}
        pk = user_session['pk']

        module_path, cls_name = settings.ACCOUNT_LOGIN_MODEL_CLASS.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_path)
        cls = getattr(module, cls_name)
        user_object = cls.objects.filter(pk=pk).first()

        # 用户信息在数据库中获取不了到
        if not user_object:
            return redirect(settings.ACCOUNT_LOGIN_URL)

        # 2. 用户已登录，return None
        request.user_object = user_object
