#!/usr/bin/env python
# -*- coding:utf-8 -*-


from utils.thread import SchedulerTaskThread, StopTaskThread


class Scheduler(object):
    def __init__(self):
        self.thread_list = []
        self.window = None
        self.terminate = False

    def start(self, window, fn_start, fn_stop, fn_counter, fn_error_counter, fn_error, fn_success):
        self.terminate = False
        self.window = window

        # 为每一行创建一个线程去执行
        for index in range(window.table_widget.rowCount()):
            asin = window.table_widget.item(index, 0).text().strip()
            status = window.table_widget.item(index, 6).text().strip()
            if window.STATUS_MAPPING[1] == status:
                self.start_one(index, asin, window, fn_start, fn_stop, fn_counter, fn_error_counter, fn_error,
                               fn_success)

    def start_one(self, index, asin, window, fn_start, fn_stop, fn_counter, fn_error_counter, fn_error, fn_success):

        # 又定义了一个线程（价格监测）
        thread = SchedulerTaskThread(index, self, asin, window)

        thread.start_signal.connect(fn_start)
        thread.stop_signal.connect(fn_stop)
        thread.counter_signal.connect(fn_counter)
        thread.error_counter_signal.connect(fn_error_counter)
        thread.error_signal.connect(fn_error)
        thread.success_signal.connect(fn_success)

        thread.start()


        self.thread_list.append(thread)

    def stop(self):
        self.terminate = True
        t = StopTaskThread(self, self.window)
        t.update.connect(self.window.update_status_message)
        t.start()

    def destroy_thread(self, thread):
        self.thread_list.remove(thread)


SCHEDULER = Scheduler()
