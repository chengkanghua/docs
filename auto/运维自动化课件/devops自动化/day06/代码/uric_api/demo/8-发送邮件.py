import os, django
from django.core import mail

if __name__ == '__main__':
    # django初始化
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uric_api.settings.dev')
    django.setup()

    # mail.send_mail(
    #     subject="测试标题",
    #     message="邮件文本内容[不包含html内容]",
    #     from_email="发件人的邮箱地址",
    #     recipient_list="收件人的邮箱列表",
    #     html_message="邮件HTML内容")

    # 其中，message与html_message是互斥的，只能指定其中一个参数
    mail.send_mail(
        subject="测试标题",
        message="邮件文本内容[不包含html内容]",
        from_email="13928835901@163.com",
        recipient_list=["13928835901@163.com"])
