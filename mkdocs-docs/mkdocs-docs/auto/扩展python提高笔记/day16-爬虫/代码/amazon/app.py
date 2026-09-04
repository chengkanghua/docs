import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QDesktopWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLineEdit, QTableWidget,
    QTableWidgetItem, QMenu, QLabel
)

from utils.dialog import LogDialog, ProxyDialog, AmazonDialog
from utils.database import DB
from utils.logger import LOGGER
from utils.helper import ALERT
from utils.thread import NewTaskThread
from utils.scheduler import SCHEDULER


class SWITCH:
    """
    开关，在进行开始和停止任务时用于标记状态
    """
    RUNNING = 1
    STOPPING = 2
    STOP = 3


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

        self.switch = SWITCH.STOP

    def init_ui(self):
        # 窗体标题和尺寸
        self.setWindowTitle('亚马逊检测平台')
        self.resize(1228, 550)

        # 窗体居中显示
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 垂直方向布局（元素垂直存放）
        layout = QVBoxLayout()
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_form())
        layout.addLayout(self.init_table())
        layout.addLayout(self.init_footer())

        # layout.addStretch(1)
        self.setLayout(layout)
        self.show()

    def init_header(self):
        # 水平排列
        header = QHBoxLayout()

        btn_start = QPushButton("开始")
        btn_start.clicked.connect(self.event_start_click)

        header.addWidget(btn_start)

        self.btn_stop = btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_stop_click)
        header.addWidget(btn_stop)

        # 设置元素的伸缩量，当做弹簧，把元素压倒左边
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
        """ 读取文件并初始化表格展示 """
        table = QHBoxLayout()

        table_widget = QTableWidget(0, 8)

        table_header = [
            {"field": "asin", "text": "ASIN", 'width': 120},
            {"field": "title", "text": "标题", 'width': 150},
            {"field": "url", "text": "URL", 'width': 400},
            {"field": "price", "text": "底价", 'width': 100},
            {"field": "success", "text": "成功次数", 'width': 100},
            {"field": "error", "text": "503次数", 'width': 100},
            {"field": "status", "text": "状态", 'width': 100},
            {"field": "frequency", "text": "频率（N秒/次）", 'width': 100},
        ]

        for index, info in enumerate(table_header):
            # 设置表格宽度
            table_widget.setColumnWidth(index, info['width'])
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(index, item)

        # # 文件中读取数据
        db_data_list = DB.CACHE_LIST
        # 初始化表格内容
        current_row_count = table_widget.rowCount()
        for item in db_data_list:
            table_widget.insertRow(current_row_count)
            self.create_row(table_widget, item, current_row_count)
            current_row_count += 1

        # # 绑定事件，当表格被修改时候自动触发
        # table_widget.itemChanged.connect(self.event_table_update)


        # # 开启右键复制功能，在表格中点击右键时，自动触发 right_menu 函数
        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.right_menu)



        self.table_widget = table_widget
        table.addWidget(table_widget)
        return table

    def create_row(self, table_widget, item, new_row_index):
        for column in range(len(item)):
            text = self.STATUS_MAPPING[item[column]] if column == 6 else item[column]
            cell = QTableWidgetItem(str(text))
            if column in [0, 4, 5, 6]:
                # 设置双击不可编辑
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table_widget.setItem(new_row_index, column, cell)

    def right_menu(self, pos):

        # 只有选中一行时，才支持右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) == 0:
            return

        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        item_log_clear = menu.addAction("清除日志")

        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == item_copy:
            # 拷贝
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())

        elif action == item_log:
            index = selected_item_list[0].row()
            asin = self.table_widget.item(index, 0).text().strip()

            # 展示日志窗口
            dialog = LogDialog(asin)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()

        elif action == item_log_clear:
            # 清除日志，根据商品ID找到文件清空
            index = selected_item_list[0].row()
            asin = self.table_widget.item(index, 0).text().strip()
            LOGGER.clear_log(asin)

    def init_footer(self):
        footer = QHBoxLayout()

        self.label_status = label_status = QLabel("未检测", self)
        footer.addWidget(label_status)

        footer_config = QHBoxLayout()
        footer_config.addStretch(1)

        btn_reinit = QPushButton("重新初始化")
        footer_config.addWidget(btn_reinit, 0, Qt.AlignRight)
        btn_reinit.clicked.connect(self.event_reinit_click)

        btn_recheck = QPushButton("重新检测")
        footer_config.addWidget(btn_recheck, 0, Qt.AlignRight)
        btn_recheck.clicked.connect(self.event_recheck_click)

        btn_reset_count = QPushButton("次数清零")
        footer_config.addWidget(btn_reset_count, 0, Qt.AlignRight)
        btn_reset_count.clicked.connect(self.event_reset_count_click)

        btn_delete = QPushButton("删除检测项")
        footer_config.addWidget(btn_delete, 0, Qt.AlignRight)
        btn_delete.clicked.connect(self.event_delete_click)

        btn_alert = QPushButton("SMTP报警配置")
        footer_config.addWidget(btn_alert, 0, Qt.AlignRight)
        btn_alert.clicked.connect(self.event_alert_click)

        btn_proxy = QPushButton("代理IP")
        footer_config.addWidget(btn_proxy, 0, Qt.AlignRight)
        btn_proxy.clicked.connect(self.event_proxy_click)

        footer.addLayout(footer_config)
        return footer

    # 开始检测
    def event_start_click(self):
        """ 点击开始检测 """
        alert_config = ALERT.read()
        if not alert_config:
            QMessageBox.warning(self, "错误", "SMTP报警配置未配置")
            return

        if self.switch != SWITCH.STOP:
            QMessageBox.warning(self, "错误", "正在检测或终止中，请勿重复操作")
            return

        self.switch = SWITCH.RUNNING

        # 获取所有行的数据，为每一行创建一个线程去执行。
        SCHEDULER.start(
            self,
            self.task_start_callback,
            self.task_stop_callback,
            self.task_counter_callback,
            self.task_error_counter_callback,
            self.task_error_callback,
            self.task_success_callback
        )

        self.update_status_message("检测中")

    def task_start_callback(self, index):
        """ 仅当前行更新为检测中 & 数据库不更新防止强制关闭后再次展示 """
        cell_status = QTableWidgetItem(self.STATUS_MAPPING[2])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 6, cell_status)

    def task_stop_callback(self, index):
        """ 仅当前行更新为待执行 & 数据库不更新防止强制关闭后再次展示 """
        cell_status = QTableWidgetItem(self.STATUS_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 6, cell_status)

    def task_counter_callback(self, index, asin, value):
        """ 计数器+1 """
        DB.update_count_by_index(index, value)
        cell = QTableWidgetItem(str(value))
        cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 4, cell)

    def task_error_counter_callback(self, index, asin, value):
        """ 错误计数器+1 """
        DB.update_error_count_by_index(index, value)
        cell = QTableWidgetItem(str(value))
        cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 5, cell)

    def task_success_callback(self, index, asin):
        """ 执行检测成功 """
        DB.update_status_by_index(index, 3)
        cell_status = QTableWidgetItem(self.STATUS_MAPPING[3])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 6, cell_status)

    def task_error_callback(self, index, asin, title, stack):
        """ 执行检测失败 """

        DB.update_status_by_index(index, 10)
        LOGGER.log(asin, title, stack)

        cell_status = QTableWidgetItem(self.STATUS_MAPPING[10])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(index, 6, cell_status)

    # 停止检测
    def event_stop_click(self):
        """ 点击停止检测 """
        if self.switch != SWITCH.RUNNING:
            QMessageBox.warning(self, "错误", "已停止或正在终止，请勿重复操作")
            return
        self.switch = SWITCH.STOPPING
        # self.switch = SWITCH.STOP
        # self.update_status_message("已停止")

        SCHEDULER.stop()

    # 点击添加
    def event_add_click(self):
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

            # 线程去获取商品标题
            thread = NewTaskThread(asin, self)
            thread.updated.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()
            current_row_index += 1

    def init_task_success_callback(self, asin, title, url):
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

    # 点击 重新初始化
    def event_reinit_click(self):
        """ 重新初始化 """
        # 选中的所有行数据
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择重新需要重新检测的行")
            return

        for row_object in row_list:
            index = row_object.row()
            asin = self.table_widget.item(index, 0).text().strip()
            text = self.table_widget.item(index, 6).text()
            if text not in [self.STATUS_MAPPING[11], self.STATUS_MAPPING[0]]:
                continue

            # 当前状态变为初始化中（表格&数据库）
            DB.update_status(asin, 0)

            cell = QTableWidgetItem(self.STATUS_MAPPING[0])
            cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 6, cell)

            # 开启线程去执行
            thread = NewTaskThread(asin, self)
            thread.updated.connect(self.init_task_success_callback)
            thread.error.connect(self.init_task_error_callback)
            thread.start()

    # 点击 重新检测
    def event_recheck_click(self):
        if self.switch != SWITCH.RUNNING:
            QMessageBox.warning(self, "错误", "开始检测后，才能对指定行进行重新检测。")
            return
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择重新需要重新检测的行")
            return

        for row_object in row_list:
            index = row_object.row()
            asin = self.table_widget.item(index, 0).text().strip()
            # 表格中变为 执行中 并 开始执行
            status = self.table_widget.item(index, 6).text()
            if status in [self.STATUS_MAPPING[3], self.STATUS_MAPPING[10]]:
                # 数据库变为 待执行
                DB.update_status_by_index(index, 1)

                SCHEDULER.start_one(
                    index,
                    asin,
                    self,
                    self.task_start_callback,
                    self.task_stop_callback,
                    self.task_counter_callback,
                    self.task_error_counter_callback,
                    self.task_error_callback,
                    self.task_success_callback
                )

    # 点击 删除
    def event_delete_click(self):
        """ 点击删除选中的监控项 """
        if self.switch != SWITCH.STOP:
            QMessageBox.warning(self, "错误", "终止后才能进行删除")
            return

        selected_row_list = self.table_widget.selectionModel().selectedRows()
        if not selected_row_list:
            QMessageBox.warning(self, "错误", "请选择要删除的检测项")
            return
        asin_list = []
        selected_row_list.reverse()

        # 页面表格中删除
        for selected in selected_row_list:
            row = selected.row()
            asin = self.table_widget.item(row, 0).text().strip()
            asin_list.append(asin)
            self.table_widget.removeRow(row)

        # 数据库中删除 & 日志删除
        DB.remove_by_asin_list(asin_list)
        LOGGER.remove_by_asin_list(asin_list)

    # 点击 次数清零
    def event_reset_count_click(self):
        """ 数据库次数和表格次数更新为0 """
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择清零的行")
            return
        index_list = []
        for row_object in row_list:
            index = row_object.row()
            index_list.append(index)

            cell = QTableWidgetItem(str(0))
            cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 4, cell)

            cell = QTableWidgetItem(str(0))
            cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 5, cell)

        DB.clear_count_and_error_count(index_list)

    # 点击 报警配置
    def event_alert_click(self):
        """ 弹出对话框进行邮件提醒配置 """

        dialog = AmazonDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    # 点击 配置代理IP
    def event_proxy_click(self):
        dialog = ProxyDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def update_status_message(self, message):
        if message == "已终止":
            self.switch = SWITCH.STOP
        self.label_status.setText(message)
        self.label_status.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
