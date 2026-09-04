import datetime
import time
import traceback
import random
import bs4
from urllib.parse import quote
from PyQt5.QtCore import QThread, pyqtSignal

from utils.helper import ALERT, PROXY
from utils.email import send_email
from utils.database import DB
from utils.logger import LOGGER

HOST = "https://www.amazon.com/"
HOST_ASIN_TPL = "{}{}".format(HOST, "gp/product/")
HOST_TASK_LIST_TPL = "{}{}".format(HOST, "gp/offer-listing")

FILTERS = quote('{"all":true,"new":true}')
TPL = "https://www.amazon.com/gp/aod/ajax/ref=aod_f_new?qty=1&asin={}&pc=dp&pageno=1&filters={}"


class NewTaskThread(QThread):
    """ 点击添加新商品检测信息 """

    # 信号，触发信号后更新窗体中的内容
    updated = pyqtSignal(str, str, str)
    error = pyqtSignal(str, str, str)

    def __init__(self, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.asin = asin

    def run(self):
        try:
            # 根据 B08166SLDF 去拼接URL
            url = "{}{}/".format(HOST_ASIN_TPL, self.asin)
            # 向地址发送请求 & bs4 进行解析（requests）
            success, text, proxy_ip = PROXY.request(url)
            if not success:
                raise Exception(text)
            soup = bs4.BeautifulSoup(text, 'lxml')
            title = soup.find(id="title").text.strip()
            url = "{}/{}/ref=dp_olp_all_mbc?ie=UTF8&condition=new".format(HOST_TASK_LIST_TPL, self.asin)

            # 获取到title和url，将这个信息填写到 表格上 & 写入文件中。
            self.updated.emit(self.asin, title, url)
        except Exception as e:
            title = "监控项 {} 添加失败。".format(self.asin)
            self.error.emit(self.asin, title, str(e))


class SchedulerTaskThread(QThread):
    start_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(int)
    counter_signal = pyqtSignal(int, str, int)
    error_counter_signal = pyqtSignal(int, str, int)
    error_signal = pyqtSignal(int, str, str, str)
    success_signal = pyqtSignal(int, str)

    def __init__(self, index, scheduler, asin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = scheduler
        self.asin = asin
        self.index = index

    def check_top_price(self, soup_object, limit_price):
        # 处理顶部商户
        tag_top_price = soup_object.select_one("#pinned-offer-top-id #aod-price-0 .a-offscreen")
        tag_top_sold_by = soup_object.select_one("#aod-pinned-offer-additional-content #aod-offer-soldBy .a-color-base")
        if tag_top_price and tag_top_price:
            top_sold_by = tag_top_sold_by.text.strip()
            condition_set = {"amazon", "amazon.com"}
            if top_sold_by.lower() not in condition_set:
                return
            top_price = float(tag_top_price.text.strip("$").replace(',', ""))
            if top_price > limit_price:
                return
            return top_price

    def check_body_price(self, soup_object, limit_price):
        condition_set = {"amazon", "amazon.com"}
        root = soup_object.find(attrs={'id': "aod-offer-list"})
        row_list = root.find_all(attrs={'id': "aod-offer"})
        for tag in row_list:
            sold_by_a = tag.find(attrs={'id': "aod-offer-soldBy"}).find('a')
            sold_by_span = tag.find(attrs={'id': "aod-offer-soldBy"}).find('span', {'class': 'a-color-base'})
            if sold_by_a:
                sold_by = sold_by_a.text.strip()
            elif sold_by_span:
                sold_by = sold_by_span.text.strip()
            else:
                sold_by = None
            price_tag = tag.find(attrs={'class': "a-offscreen"})
            price = float(price_tag.text.strip("$").replace(',', ""))
            if not sold_by:
                continue
            if sold_by.lower() not in condition_set:
                continue

            if price > limit_price:
                return
            return price

    def run(self):
        self.start_signal.emit(self.index)
        while True:
            try:
                if self.scheduler.terminate:
                    self.scheduler.destroy_thread(self)
                    self.stop_signal.emit(self.index)
                    return

                db_row_list = DB.get_by_index(self.index)
                # url = db_row_list[2]
                url = TPL.format(self.asin, FILTERS)

                limit_price = float(db_row_list[3])
                frequency = int(db_row_list[7])
                count = int(db_row_list[4])
                error_count = int(db_row_list[5])

                # 发送网络请求
                success, text, proxy_ip = PROXY.request(url)
                if not success:
                    error_count = error_count + 1
                    self.error_counter_signal.emit(self.index, self.asin, error_count)
                    content = "代理IP:{} 请求失败。\n".format(str(proxy_ip) or "本机")
                    LOGGER.log(self.asin, content, text)
                    continue

                count = count + 1
                self.counter_signal.emit(self.index, self.asin, count)

                soup = bs4.BeautifulSoup(text, 'lxml')

                top_price = self.check_top_price(soup, limit_price)

                if top_price:
                    # 发送邮件提醒 & 销毁线程 & 成功
                    self.send_alert_email(db_row_list, top_price)
                    self.scheduler.destroy_thread(self)
                    self.success_signal.emit(self.index, self.asin)
                    return

                body_price = self.check_body_price(soup, limit_price)

                if body_price:
                    # 发送邮件提醒 & 销毁线程 & 成功
                    self.send_alert_email(db_row_list, body_price)
                    self.scheduler.destroy_thread(self)
                    self.success_signal.emit(self.index, self.asin)
                    return
                time.sleep(random.randint(frequency if frequency - 3 < 0 else frequency - 3, frequency + 3))

            except Exception as e:
                title = "{}检测异常。".format(self.asin)
                stack = traceback.format_exc()
                self.scheduler.destroy_thread(self)
                self.error_signal.emit(self.index, self.asin, title, stack)
                return

    def send_alert_email(self, task_row, price):
        """ 发送邮件提醒 """

        config = ALERT.read()
        template = """

            <div style="width:750px;">
                <h2 style="text-align:center;">亚马逊商品检测报告</h2>
                <table border="1" style="width:100%;">
                    <thead>
                        <tr><th>标题</th><th>对应值</th></tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding:5px 10px;text-align:right;">商品名称</td>
                            <td style="padding:5px 10px;text-align:left;">{0}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;text-align:right;">ASIN</td>
                            <td style="padding:5px 10px;text-align:left;">{1}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;text-align:right;">当前售价</td>
                            <td style="padding:5px 10px;text-align:left;">{2}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;text-align:right;">限定低价</td>
                            <td style="padding:5px 10px;text-align:left;">{3}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;text-align:right;">商品地址</td>
                            <td style="padding:5px 10px;text-align:left;"><a href="{4}ref=dp_olp_all_mbc?ie=UTF8&condition=new">{4}ref=dp_olp_all_mbc?ie=UTF8&condition=new</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """
        content = template.format(task_row[1], task_row[0], price, task_row[3], task_row[2])
        send_email(config, content)


class StopTaskThread(QThread):
    update = pyqtSignal(str)

    def __init__(self, scheduler, window):
        super().__init__(window)
        self.scheduler = scheduler
        self.window = window

    def run(self):
        total_count = len(self.scheduler.thread_list)
        self.scheduler.terminate = True
        while True:
            running_count = len(self.scheduler.thread_list)
            self.update.emit("正在终止（{}/{}）".format(total_count - running_count, total_count))
            if running_count == 0:
                break
            time.sleep(1)
        self.update.emit("已终止")
