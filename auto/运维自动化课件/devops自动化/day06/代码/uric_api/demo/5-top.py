# !/usr/bin/env python
import time
import psutil
from datetime import datetime
from psutil._common import bytes2human as size

# 获取系统启动时间
print(f"{'-'*32} 系统时间 {'-'*32}")
uptime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
# 系统当前本地时间
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(f"系统启动时间: {uptime}\t系统本地时间：{now_time}")

# 获取系统用户
users_count = len(psutil.users())
users_list = ",".join([u.name for u in psutil.users()])
print(f"当前有{users_count}个用户：{users_list}")

print(f"{'-'*32} CPU信息 {'-'*32}")
# 物理cpu个数
cpu_count = psutil.cpu_count(logical=False)
# cpu内核个数
logical_cpu_count = psutil.cpu_count()
# cpu的使用率
cpu_percent = psutil.cpu_percent(1)
# cpu的平均负载
cpu_loadavg = " ".join([str(item) for item in psutil.getloadavg()])
print(f"CPU个数: {cpu_count}\t内核个数：{logical_cpu_count}\tcup使用率: {cpu_percent}%\tCPU负载参数：{cpu_loadavg}")

print(f"{'-'*32} 内存信息 {'-'*32}")
# 查看物理内存信息
memory = psutil.virtual_memory()
free = size(memory.free)
total = size(memory.total)
memory_percent = (memory.total - memory.free) / memory.total
print(f"总物理内存：{total}\t剩余物理内存：{free:10s}物理内存使用率：{int(memory_percent * 100)}%")
# 查看交换内存信息
swap = psutil.swap_memory()
free = size(swap.free)
total = size(swap.total)
swap_percent = (swap.total - swap.free) / swap.total
print(f"总交换内存：{total}\t剩余交换内存：{free:10s}交换内存使用率：{int(swap_percent * 100)}%")


print(f"{'-'*32} 网卡信息 {'-'*32}")
# 获取网卡信息，可以得到得到网卡属性，连接数，当前数据等信息
net = psutil.net_io_counters()
bytes_sent = size(net.bytes_recv)
bytes_rcvd = size(net.bytes_sent)
print(f"网卡接收数据：{bytes_rcvd}\t网卡发送数据：{bytes_sent}")

# 获取磁盘数据信息
print(f"{'-'*32} 磁盘信息 {'-'*32}")
io = psutil.disk_partitions()
for i in io:
    try:
        o = psutil.disk_usage(i.device)
        print(f"设备：{i.device:12s}总容量：{size(o.total):6s}已用容量：{size(o.used):6s}可用容量：{size(o.free)}")
    except PermissionError:
        continue

print(f"{'-'*32} 进程信息 {'-'*32}")
# 查看系统全部进程
for pnum in psutil.pids():
    p = psutil.Process(pnum)
    print(f"进程名：{p.name():20.20s}内存利用率：{p.memory_percent():.2f}\t进程状态：{p.status():10s}创建时间：{datetime.fromtimestamp(p.create_time()):%Y-%m-%d %H:%M:%S}")