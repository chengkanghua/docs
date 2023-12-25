import time
import psutil
from datetime import datetime

if __name__ == '__main__':
    # # 物理CPU个数
    # print(psutil.cpu_count(logical=False))
    # # CPU内核个数[逻辑CPU个数]
    # print(psutil.cpu_count())

    # # 获取CPU的利用率
    # print(psutil.cpu_percent(percpu=True, interval=0.1))  # 每一个CPU的利用率
    # print(psutil.cpu_percent(percpu=False, interval=1))  # 所有CPU的平均利用率

    # # CPU的负载
    # # windows系统下是通过子线程进行模拟的，因此前5秒返回的结果是(0.0,0.0, 0.0)
    # for _ in range(3):
    #     print(psutil.getloadavg())
    #     time.sleep(5)

    # # 内存
    # memory = psutil.virtual_memory()
    # print(memory)
    # # 总内存
    # print(memory.total)
    # # 可用内存，linux系统下，available = free + buffers + cached
    # print(memory.available)
    # # 空闲内存
    # print(memory.free)
    # if psutil.POSIX:
    #     # 内存缓冲
    #     print(memory.buffers)
    #     print(memory.cached)
    #     print(memory.free + memory.buffers + memory.cached)

    # # 交换内存
    # swap = psutil.swap_memory()
    # print(swap)
    # print(swap.total)
    # print(swap.free)
    # print(swap.used)

    # 硬盘
    # # 分区信息
    # partitions = psutil.disk_partitions()
    # for partition in partitions:
    #     print(partition, partition.device, partition.fstype)

    # 分区磁盘的使用统计信息
    # print( psutil.disk_usage("/") )


    # # 网络IO统计
    # network = psutil.net_io_counters()
    # print(network)
    # print(network.bytes_sent)
    # print(network.bytes_recv)
    # print(network.packets_sent)
    # print(network.packets_recv)
    #
    # for item in psutil.net_if_addrs().items():
    #     print(item)

    # # 系统启动时间
    # uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    #
    # # 系统当前时间
    # now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # print(uptime, now_time)

    # # 连接当前系统的用户
    # users = psutil.users()
    # for user in users:
    #     started = datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")
    #     print(user.name, user.host, user.terminal, started, user.pid)

    # # 系统进程列表
    # for proc in psutil.process_iter(['pid', 'create_time', 'name', 'status', 'memory_percent', 'username', 'cmdline']):
    #     print(proc.info)

    # 本地执行终端命令[开启一个独立的进程，单独运行命令]
    my_process = psutil.Popen(["python", "-c", 'print("hello world")'])
    # 用户程序的信息获取
    print("用户进程的名称：{}".format(my_process.name()))
    print("用户进程的启动用户：{}".format(my_process.username()))
    print("用户进程的输出信息：{}".format(my_process.communicate()))
