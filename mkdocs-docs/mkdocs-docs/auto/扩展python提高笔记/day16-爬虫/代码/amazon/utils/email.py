#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def send_email(config, content):
    to_email_list = config["to"].replace("，", ',').split(",")

    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = formataddr(["亚马逊商品检测系统", config['from']])
    msg['Subject'] = "亚马逊商品检测系统提醒"

    server = smtplib.SMTP_SSL(config['smtp'])
    server.login(config['from'], config['pwd'])
    server.sendmail(config['from'], to_email_list, msg.as_string())
    server.quit()
