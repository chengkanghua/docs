# !/usr/bin/env python
import time, json, os
from datetime import datetime
try:
    import psutil
except:
    os.system("pip install psutil")
    import psutil
try:
    import requests

except:
    os.system("pip install requests")
    import requests

from psutil._common import bytes2human as size

data = {}
# 获取系统启动时间
data["uptime"] = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
# 系统当前本地时间
data['time'] = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

# 获取当前连接到系统的用户
data["users_count"] = len(psutil.users())
data["users"] = [{"name": user.name, "pid": user.pid, "terminal": user.terminal, "host": user.host, "started": datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S")} for user in psutil.users()]


# 物理cpu个数
data["cpu_count"] = psutil.cpu_count(logical=False)
# cpu内核个数
data["cpu_logical_count"] = psutil.cpu_count()
# cpu的使用率
data["cpu_every_percent"] = psutil.cpu_percent(interval=1, percpu=True)  # 每个CPU最近1秒内的使用率
data["cpu_avg_percent"] = psutil.cpu_percent(interval=1, percpu=False)   # 系统所有CPU最近1秒内的平均使用率
# cpu的平均负载
data["cpu_loadavg"] = [str(item) for item in psutil.getloadavg()]

# 查看物理内存信息
data["memory"] = {}
memory = psutil.virtual_memory()
# 总内存
data["memory"]["total"] = size(memory.total)
# 空闲内存
data["memory"]["free"] = size(memory.free)
# 可用内存
data["memory"]["available"] = size(memory.available)
# 系统已用内存的百分比(不包含缓存与缓存)，percent=(total - available) / total * 100
data["memory"]["percent1"] = size(memory.percent)
# 系统已用内存的百分比（包含缓存与缓存）
data["memory"]["percent2"] = (memory.total - memory.free) / memory.total

# 查看交换内存信息
data["swap_memory"] = {}
swap = psutil.swap_memory()
data["swap_memory"]["free"] = size(swap.free)
data["swap_memory"]["total"] = size(swap.total)
data["swap_memory"]["swap_percent"] = (swap.total - swap.free) / swap.total

# 获取网卡信息，可以得到得到网卡属性，连接数，当前数据等信息
data["net"] = {}
net = psutil.net_io_counters()
data["net"]["bytes_recv"] = size(net.bytes_recv)
data["net"]["bytes_sent"] = size(net.bytes_sent)
data["net"]["packets_sent"] = size(net.packets_sent)
data["net"]["packets_recv"] = size(net.packets_recv)

# 获取磁盘数据信息
data["disk"] = []
io = psutil.disk_partitions()
for i in io:
    try:
        o = psutil.disk_usage(i.device)
        data["disk"].append({
          "device": i.device,
          "total": size(o.total),
          "used": size(o.used),
          "free": size(o.free),
        })
    except PermissionError:
        continue


# 查看系统全部进程
data["process_list"] = []
for proc in psutil.process_iter(['pid', 'create_time', 'name', 'status', 'memory_percent', 'username', 'cmdline']):
    data["process_list"].append(proc.info)

print(json.dumps(data))

# send request to django

