from django.utils.deprecation import MiddlewareMixin
import time

import logging


class LogMiddleWare(MiddlewareMixin):
    start = 0

    def process_request(self, request):
        self.start = time.time()

    def process_response(self, request, response):
        cost_timer = time.time() - self.start

        print("cost_timer", cost_timer)

        if cost_timer > 0.5:
            # 警告日志
            logger = logging.getLogger("django")
            logger.warning(f"请求路径: {request.path} 耗时{cost_timer}秒")


        return response
