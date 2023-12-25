#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit, QHBoxLayout

from PyQt5.QtCore import Qt

from utils.helper import ALERT, PROXY
from utils.logger import LOGGER


class AmazonDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field_dict = {}
        self.init_ui()

    def init_ui(self):
        """
        初始化对话框
        :return:
        """
        self.setWindowTitle("报警邮件配置")
        self.resize(300, 270)

        layout = QVBoxLayout()

        form_data_list = [
            {"title": "SMTP服务器:", "filed": "smtp"},
            {"title": "发件箱:", "filed": "from"},
            {"title": "密码:", "filed": "pwd"},
            {"title": "收件人（多个用逗号分隔）:", "filed": "to"},
        ]

        # 读取文件中的配置
        old_alert_dict = ALERT.read()

        for item in form_data_list:
            lbl = QLabel()
            lbl.setText(item['title'])
            layout.addWidget(lbl)
            txt = QLineEdit()
            filed = item['filed']
            if old_alert_dict and filed in old_alert_dict:
                txt.setText(old_alert_dict[filed])
            layout.addWidget(txt)
            self.field_dict[item['filed']] = txt

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(self.event_save_click)
        layout.addWidget(btn_save, 0, Qt.AlignRight)

        layout.addStretch(1)
        self.setLayout(layout)

    def event_save_click(self):

        data_dict = {}

        for key, filed in self.field_dict.items():
            value = filed.text().strip()
            if not value:
                QMessageBox.warning(self, "错误", "邮件报警项不能为空")
                return
            data_dict[key] = value
        ALERT.write(data_dict)
        self.close()


class LogDialog(QDialog):
    def __init__(self, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("日志记录")
        self.resize(500, 400)
        layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setText("")
        layout.addWidget(text_edit)
        self.setLayout(layout)

        # 读取日志展示出来
        content = LOGGER.get_log(self.asin)
        text_edit.setText(content)


class ProxyDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("配置代理IP")
        self.resize(500, 400)
        layout = QVBoxLayout()

        # 输入框
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("可用换行来设置多个代理IP，每个代理IP设置格式为：31.40.225.250:3128")
        all_proxy = PROXY.read()
        text_edit.setText(all_proxy)
        self.text_edit = text_edit
        layout.addWidget(text_edit)

        footer_config = QHBoxLayout()

        btn_save = QPushButton("重置")
        btn_save.clicked.connect(self.event_save_click)
        footer_config.addWidget(btn_save, 0, Qt.AlignRight)

        layout.addLayout(footer_config)

        self.setLayout(layout)

    def event_save_click(self):
        PROXY.write(self.text_edit.toPlainText())
        self.close()
