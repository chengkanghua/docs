import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox, QTableWidget,
    QTableWidgetItem, QLabel
)

from utils.database import DB


class MainWindow(QWidget):
    STATUS_MAPPING = {
        0: "初始化中",
        1: "待执行",
        2: "正在执行",
        3: "完成并提醒",
        10: "异常并停止",
        11: "初始化失败",
    }

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """ 将窗体和窗体中的元素给生成 """

        self.setWindowTitle('亚马逊检测平台')
        self.resize(1228, 550)

        # 窗体居中显示
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 1. 垂直方向布局（元素垂直存放）
        layout = QVBoxLayout()

        # 1.1 顶部布局，里面有2个按钮
        layout.addLayout(self.init_header())

        # 1.2 输入框
        layout.addLayout(self.init_form())

        # 1.3 表格
        layout.addLayout(self.init_table())

        # 1.4 底部
        layout.addLayout(self.init_footer())

        # layout.addStretch(1)
        self.setLayout(layout)
        self.show()

    def init_header(self):
        header = QHBoxLayout()

        btn_start = QPushButton("开始")
        btn_start.clicked.connect(self.event_start_click)

        header.addWidget(btn_start)

        btn_stop = QPushButton("结束")
        btn_stop.clicked.connect(self.event_stop_click)
        header.addWidget(btn_stop)

        header.addStretch(1)
        return header

    def init_form(self):
        form = QHBoxLayout()

        self.txt_asin = txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入商品ASIN且多个用逗号分隔，如：B0815JJQQ8=18,B0815JJQQ9=19,B0818JJQQ8=88")

        form.addWidget(txt_asin)
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)

        form.addWidget(btn_add)
        return form

    def init_table(self):
        table = QHBoxLayout()

        # 创建表格对象
        self.table_widget = table_widget = QTableWidget(0, 8)

        # 生成表头数据
        table_header_list = [
            {"field": "asin", "text": "ASIN", 'width': 120},
            {"field": "title", "text": "标题", 'width': 150},
            {"field": "url", "text": "URL", 'width': 400},
            {"field": "price", "text": "底价", 'width': 100},
            {"field": "success", "text": "成功次数", 'width': 100},
            {"field": "error", "text": "503次数", 'width': 100},
            {"field": "status", "text": "状态", 'width': 100},
            {"field": "frequency", "text": "频率（N秒/次）", 'width': 100},
        ]

        for index, info in enumerate(table_header_list):
            # 设置表格宽度
            table_widget.setColumnWidth(index, info['width'])
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(index, item)

        # 创建表内容，在创建某些对象添加到表格中。 去文件中获取历史的商品信息
        db_data_list = DB.CACHE_LIST

        current_row_count = table_widget.rowCount()
        for item in db_data_list:
            # 原来的基础上再增加一行（空白）
            table_widget.insertRow(current_row_count)
            self.create_row(table_widget, item, current_row_count)
            current_row_count += 1

        table.addWidget(table_widget)
        return table

    def init_footer(self):
        footer = QHBoxLayout()

        self.label_status = label_status = QLabel("未检测", self)
        footer.addWidget(label_status)

        footer_config = QHBoxLayout()
        footer_config.addStretch(1)

        btn_reinit = QPushButton("重新初始化")
        footer_config.addWidget(btn_reinit, 0, Qt.AlignRight)
        # btn_reinit.clicked.connect(self.event_reinit_click)

        btn_recheck = QPushButton("重新检测")
        footer_config.addWidget(btn_recheck, 0, Qt.AlignRight)
        # btn_recheck.clicked.connect(self.event_recheck_click)

        btn_reset_count = QPushButton("次数清零")
        footer_config.addWidget(btn_reset_count, 0, Qt.AlignRight)
        # btn_reset_count.clicked.connect(self.event_reset_count_click)

        btn_delete = QPushButton("删除检测项")
        footer_config.addWidget(btn_delete, 0, Qt.AlignRight)
        # btn_delete.clicked.connect(self.event_delete_click)

        btn_alert = QPushButton("SMTP报警配置")
        footer_config.addWidget(btn_alert, 0, Qt.AlignRight)
        # btn_alert.clicked.connect(self.event_alert_click)

        btn_proxy = QPushButton("代理IP")
        footer_config.addWidget(btn_proxy, 0, Qt.AlignRight)
        # btn_proxy.clicked.connect(self.event_proxy_click)

        footer.addLayout(footer_config)
        return footer

    def create_row(self, table_widget, item, current_row_count):
        for column, ele in enumerate(item):
            # 规定，是否不可以被修改
            text = self.STATUS_MAPPING[item[column]] if column == 6 else item[column]
            cell = QTableWidgetItem(str(text))
            if column in [0, 4, 5, 6]:
                # 不能被修改
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table_widget.setItem(current_row_count, column, cell)

    def event_start_click(self):
        QMessageBox.warning(self, "错误", "点击开始")

    def event_stop_click(self):
        QMessageBox.warning(self, "错误", "点击结束")

    def event_add_click(self):
        """ 获取在输入框中输入的数据，然后再去处理 """
        text = self.txt_asin.text()
        if not text:
            QMessageBox.warning(self, "错误", "商品ASIN输入错误 ！")
            return

        text = text.replace("，", ",")
        asin_price_list = text.split(",")

        # 获取当前表格总共有多少行
        current_row_index = self.table_widget.rowCount()

        for item in asin_price_list:
            data_pair = item.split("=")
            if len(data_pair) != 2:
                continue
            try:
                asin, price = data_pair
                asin = asin.strip()
                price = float(price.strip())
            except Exception as e:
                QMessageBox.warning(self, "错误", "商品ASIN输入错误 ！")
                return

            # ASIN已存在，自动忽略不再添加
            if DB.get_by_asin(asin):
                continue

            # 表格添加 & 数据库插入（asin，价格，状态，次数）
            new_row_data_list = [asin, "", "", price, 0, 0, 0, 5]
            DB.add(new_row_data_list)

            self.table_widget.insertRow(current_row_index)
            self.create_row(self.table_widget, new_row_data_list, current_row_index)

            # 在创建一个线程去获取商品标题、
            from utils.thread import NewTaskThread
            thread = NewTaskThread(asin, self)
            thread.updated.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()

            current_row_index += 1

    def init_task_success_callback(self, asin, title, url):

        # 去文件中找
        db_index = DB.get_index_by_asin(asin)
        if db_index == None:
            return

        row_object = self.table_widget.item(db_index, 0)
        row_asin = row_object.text().strip()
        if row_asin != asin:
            return

        # 更新数据库中的：标题、URL、状态
        DB.update_title_url_status(asin, title, url, 1)

        # 更新表格中的：标题、URL、状态
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(db_index, 1, cell_title)

        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(db_index, 2, cell_url)

        cell_status = QTableWidgetItem(self.STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(db_index, 6, cell_status)

        # 如果已启动，则开始检测
        # if self.switch == SWITCH.RUNNING:
        #     SCHEDULER.start_one(
        #         db_index,
        #         asin,
        #         self,
        #         self.task_start_callback,
        #         self.task_stop_callback,
        #         self.task_counter_callback,
        #         self.task_error_counter_callback,
        #         self.task_error_callback,
        #         self.task_success_callback
        #     )
        self.txt_asin.clear()

    def init_task_error_callback(self, asin, title, detail):
        db_index = DB.get_index_by_asin(asin)
        if db_index == None:
            return
        row_object = self.table_widget.item(db_index, 0)
        if not row_object:
            return
        row_asin = row_object.text().strip()
        if row_asin != asin:
            return
        # 更新数据库状态：初始化失败 & 写入错误日志
        DB.update_status(asin, 11)

        LOGGER.log(asin, title, detail)

        # 更新表格状态：初始化失败
        cell_status = QTableWidgetItem(self.STATUS_MAPPING[11])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(db_index, 6, cell_status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
