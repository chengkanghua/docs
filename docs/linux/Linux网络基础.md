## 计算机网络

计算机网络学习的核心内容就是网络协议的学习。
网络协议是为计算机网络中进行数据交换而建立的规则、标准或者说是约定的集合。因为不同用户的数据终端可能采取的字符集是不同的，两者需要进行通信，必须要在一定的标准上进行。
一个很形象地比喻就是我们的语言，我们大天朝地广人多，地方性语言也非常丰富，而且方言之间差距巨大。A地区的方言可能B地区的人根本无法接受，所以我们要为全国人名进行沟通建立一个语言标准，这就是我们的普通话的作用。同样，放眼全球，我们与外国友人沟通的标准语言是英语，所以我们才要苦逼的学习英语。

---

计算机网络协议同我们的语言一样，多种多样。
而ARPA公司与1977年到1979年推出了一种名为ARPANET的网络协议受到了广泛的热捧，其中最主要的原因就是它推出了人尽皆知的TCP/IP标准网络协议。
目前TCP/IP协议已经成为Internet中的"通用语言"，下图为不同计算机群之间利用TCP/IP进行通信的示意图。
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856859526-6deb221c-0a0a-4995-9a31-e98e87344c13.png#align=left&display=inline&height=348&margin=%5Bobject%20Object%5D&originHeight=348&originWidth=1014&size=0&status=done&style=none&width=1014)

### 网络层次划分
为了使不同计算机厂家生产的计算机能够相互通信，以便在更大的范围内建立计算机网络，国际标准化组织（ISO）在1978年提出了"开放系统互联参考模型"
即著名的`OSI/RM模型（Open System Interconnection/Reference Model）。`
它将计算机网络体系结构的通信协议划分为七层，`自下而上`依次为：
物理层（Physics Layer）
数据链路层（Data Link Layer）
网络层（Network Layer）
传输层（Transport Layer）
会话层（Session Layer）
表示层（Presentation Layer）
应用层（Application Layer）。
其中第四层完成数据传送服务，上面三层面向用户。
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856861259-0cbd5f81-b41c-4a0d-9441-5e573482b345.png#align=left&display=inline&height=914&margin=%5Bobject%20Object%5D&originHeight=914&originWidth=1132&size=0&status=done&style=none&width=1132)

### 网络体系结构分层
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856861250-ef25c15d-0236-48c9-85ae-9c221cea706c.png#align=left&display=inline&height=536&margin=%5Bobject%20Object%5D&originHeight=536&originWidth=1322&size=0&status=done&style=none&width=1322)
### 应用层
**应用层(application-layer）的任务是通过应用进程间的交互来完成特定网络应用。**
应用层协议定义的是应用进程（进程：主机中正在运行的程序）间的通信和交互的规则。
对于不同的网络应用需要不同的应用层协议。在互联网中应用层协议很多，如**域名系统 DNS**，支持万维网应用的 **HTTP 协议**，支持电子邮件的 **SMTP 协议**等等。
我们把应用层交互的数据单元称为**报文**。
**域名系统(Domain Name System缩写 DNS**，Domain Name被译为域名)是因特网的一项核心服务，它作为可以将域名和IP地址相互映射的一个分布式数据库，能够使人更方便的访问互联网，而不用去记住能够被机器直接读取的IP数串。
DNS解析系统这好比我们手机上的电话簿，名字只是便于记忆，电话才是可以找到对方地址
```
小张  15210134321
小红  15293843845
```
**HTTP协议**
超文本传输协议（HTTP，HyperText Transfer Protocol)是互联网上应用最为广泛的一种网络协议。所有的 WWW（万维网） 文件都必须遵守这个标准。设计 HTTP 最初的目的是为了提供一种发布和接收 HTML 页面的方法。
我们能够上网，也就是因为有TCP/IP协议，且定义了互联网传输的HTTP协议，我们才能看到琳琅满目的商品网站
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856994831-65c08f56-5b92-4d24-9aa2-c6af2a89db2d.png#align=left&display=inline&height=623&margin=%5Bobject%20Object%5D&originHeight=1828&originWidth=3780&size=0&status=done&style=none&width=1288)

### 传输层
**运输层(transport layer)的主要任务就是负责向两台主机进程之间的通信提供通用的数据传输服务**。
第一个端到端，即主机到主机的层次。传输层负责将上层数据分段并提供端到端的、可靠的或不可靠的传输。
此外，传输层还要处理端到端的差错控制和流量控制问题。 传输层的任务是根据通信子网的特性，最佳的利用网络资源，为两个端系统的会话层之间，提供建立、维护和取消传输连接的功能，负责端到端的可靠数据传输。在这一层，信息传送的协议数据单元称为段或报文。 网络层只是根据网络地址将源结点发出的数据包传送到目的结点，而传输层则负责将数据可靠地传送到相应的端口。
传输层主要使用如下两种协议
**传输控制协议 TCP**（Transmisson Control Protocol）--提供**面向连接**的，**可靠的**数据传输服务。
**用户数据协议 UDP**（User Datagram Protocol）--提供**无连接**的，尽最大努力的数据传输服务（**不保证数据传输的可靠性**）。

```
UDP 是无连接的；
UDP 使用尽最大努力交付，即不保证可靠交付，因此主机不需要维持复杂的链接状态（这里面有许多参数）；
UDP 是面向报文的；
UDP 没有拥塞控制，因此网络出现拥塞不会使源主机的发送速率降低（对实时应用很有用，如 直播，实时视频会议等）；
UDP 支持一对一、一对多、多对一和多对多的交互通信；
UDP 的首部开销小，只有8个字节，比TCP的20个字节的首部要短。
```
```
TCP 是面向连接的。（就好像打电话一样，通话前需要先拨号建立连接，通话结束后要挂机释放连接）；
每一条 TCP 连接只能有两个端点，每一条TCP连接只能是点对点的（一对一）；
TCP 提供可靠交付的服务。通过TCP连接传送的数据，无差错、不丢失、不重复、并且按序到达；
TCP 提供全双工通信。TCP 允许通信双方的应用进程在任何时候都能发送数据。
TCP 连接的两端都设有发送缓存和接收缓存，用来临时存放双方通信的数据；
面向字节流。TCP 中的“流”（Stream）指的是流入进程或从进程流出的字节序列。“面向字节流”的含义是：虽然应用程序和 TCP 的交互是一次
```

# Linux网络管理命令
## ifconfig
用于配置网卡ip地址信息等网络参数或显示网络接口状态，类似于windows的ipconfig命令。
可以用这个工具来临时性的配置网卡的IP地址、掩码、广播地址、网关等。
注意只能用root使用此命令，且系统如果没有此命令，需要单独安装
```
yum install net-tools -y
语　　法：
ifconfig [网络设备][down up -allmulti -arp -promisc][add<地址>][del<地址>][<hw<网络设备类型><硬件地址>][io_addr<I/O地址>][irq<IRQ地址>][media<网络媒介类型>][mem_start<内存地址>][metric<数目>][mtu<字节>][netmask<子网掩码>][tunnel<地址>][-broadcast<地址>][-pointopoint<地址>][IP地址]
```
参数
```
up 启动指定网络设备/网卡
down 关闭指定网络设备/网卡
-arp 设置指定网卡是否支持ARP协议
-promisc 设置是否支持网卡的promiscuous模式，如果选择此参数，网卡将接收网络中发给它所有的数据包
-allmulti 设置是否支持多播模式，如果选择此参数，网卡将接收网络中所有的多播数据包
-a 显示全部接口信息
-s 显示摘要信息（类似于 netstat -i）
add 给指定网卡配置IPv6地址
del 删除指定网卡的IPv6地址
<硬件地址> 配置网卡最大的传输单元
mtu<字节数> 设置网卡的最大传输单元 (bytes)
netmask<子网掩码> 设置网卡的子网掩码
tunel 建立隧道
dstaddr 设定一个远端地址，建立点对点通信
-broadcast<地址> 为指定网卡设置广播协议
-pointtopoint<地址> 为网卡设置点对点通讯协议
multicast 为网卡设置组播标志
为网卡设置IPv4地址
txqueuelen<长度> 为网卡设置传输列队的长度
```
## ifconfig案例
MAC地址，直译为媒体访问控制地址，也称为局域网地址，以太网地址或物理地址，它是一个用来确认网上设备位置的地址。在OSI模型中，第三层网上层负责IP地址，第二层数据链接层则负责MAC地址。
```
[root@local-gege ~]# ifconfig
ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.178.180  netmask 255.255.255.0  broadcast 192.168.178.255  #IPV4
        inet6 fe80::d2d8:6d71:84a:bacd  prefixlen 64  scopeid 0x20<link>  #IPV6
        ether 00:0c:29:1f:ea:9e  txqueuelen 1000  (Ethernet)                        #MAC地址
        RX packets 5290  bytes 451038 (440.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3829  bytes 363532 (355.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 15  bytes 1560 (1.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 15  bytes 1560 (1.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610857066248-8c71942c-ba27-4495-baa7-b08e7d13443d.png#align=left&display=inline&height=575&margin=%5Bobject%20Object%5D&originHeight=1014&originWidth=2372&size=0&status=done&style=none&width=1345)
### _启动/关闭指定网卡_
```
[root@local-gege ~]# ifconfig ens33 down  #注意不得在服务器上执行，关闭了网卡就断开连接了
[root@local-gege ~]# ifconfig ens33 up  #再次启动网卡
```
### _修改、设置网卡ip_
注意这个操作不要在服务器上操作，否则会断开连接，仅供学习
```
ifconfig ens33 192.168.178.100
```
### _给网卡设置别名、添加多个ip地址_
```
#添加并启动新ip
[root@local-gege ~]# ifconfig ens33:0 192.168.178.111 netmask 255.255.255.0 up
#第二种方式添加
[root@local-gege ~]# ifconfig ens33:0 192.168.178.115/24 up
```
### 修改MAC地址
```
[root@local-gege ~]# ifconfig ens33 hw ether 00:0c:29:13:10:CF
[root@local-gege ~]# ifconfig ens33 hw ether 00:0c:29:1f:ea:9e  #再改回去
```
### 修改网卡配置文件
以上命令重启网卡或是机器后，网卡信息会还原，想要永久修改网卡信息，还得修改配置文件
网卡路径
```
[root@local-gege ~]# ls /etc/sysconfig/network-scripts/ |grep ifcfg
ifcfg-ens33
ifcfg-lo
别名也可以设置配置文件
例如/etc/sysconfig/network-scripts/ifcfg-ens33:0
```
## ifup命令
用于激活指定的网络接口，ifup其实是读取配置文件/etc/sysconfig/network-scripts/ifcfg-ens33
_启停网卡_
```
ifup ens33 
ifdown ens33
ifconfig查看
```
## route命令
route程序对内核的IP选路表进行操作。它主要用于通过已用ifconfig(8)程序配置好的接口来指定的主机或网络设置静态路由。
路由概念：
计算机之间的数据传输必须经过网络，网络可以直接连接两台计算机，或者通过一个一个的节点构成。
路由器理解为互联网的中转站，网络中的数据包就是通过一个一个路由器转发到达目的地。
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610857066266-ae4b2ec7-dd1b-4051-9f4b-b0ba657eb0a2.png#align=left&display=inline&height=554&margin=%5Bobject%20Object%5D&originHeight=554&originWidth=1180&size=0&status=done&style=none&width=1180)
### 路由的分类
路由分为静态路由和动态路由。
Linux上配置的都是静态路由，是系统管理员使用route命令假如，也就是通过手动输入的方式添加路由规则。
动态路由是无需人为干预，是本机与不同机器之间经过路由的顺序，相互交换路由规则而来。
```
-v
    选用细节操作模式
-A family
    用指定的地址族(如`inet'，`inet6')。
-n
    以数字形式代替解释主机名形式来显示地址。此项对试图检测对域名服务器进行路由发生故障的原因非常有用。
-e
    用netstat(8)的格式来显示选路表。-ee将产生包括选路表所有参数在内的大量信息。
-net
    路由目标为网络。
-host
    路由目标为主机。
-F
    显示内核的FIB选路表。其格式可以用-e 和 -ee选项改变。
-C
    显示内核的路由缓存。
del
    删除一条路由。
add
    添加一条路由。
target
    指定目标网络或主机。可以用点分十进制形式的IP地址或主机/网络名。
netmask Nm
    为添加的路由指定网络掩码。
gw Gw
    为发往目标网络/主机的任何分组指定网关。注意：指定的网关首先必须是可达的。也就是说必须为该网关预先指定一条静态路由。如果你为本地接口之一指定这个网关地址的话，那么此网关地址将用于决定此接口上的分组将如何进行路由。这是BSD风格所兼容的。
metric M
    把选路表中的路由值字段(由选路进程使用)设为M。
mss M
    把基于此路由之上的连接的TCP最大报文段长度设为M字节。这通常只用于优化选路设置。默认值为536。
window W
    把基于此路由之上的连接的TCP窗口长度设为W字节。这通常只用于AX.25网络和不能处理背对背形式的帧的设备。
irtt I
    把基于此路由之上的TCP连接的初始往返时间设为I毫秒(1-12000)。这通常也只用于AX.25网络。如果省略此选项，则使用RFC1122的缺省值300ms。
reject
    设置一条阻塞路由以使一条路由查找失败。这用于在使用缺省路由前先屏蔽掉一些网络。但这并不起到防火墙的作用。
mod, dyn, reinstate
    设置一条动态的或更改过的路由。这些标志通常只由选路进程来设置。这只用于诊断目的，
dev If
    强制使路由与指定的设备关联，因为否则内核会自己来试图检测相应的设备(通常检查已存在的路由和加入路由的设备的规格)。在多数正常的网络上无需使用。
    如果dev If是命令行上最后一个指定的选项，那么可以省略关键字dev，因为它是缺省值。否则路由修改对象(metric - netmask- gw - dev)无关紧要。
```
### route案例
```
# route将IP地址进行DNS解析成主机名
[root@local-gege network-scripts]# route 
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         bogon           0.0.0.0         UG    102    0        0 ens33
192.168.178.0   0.0.0.0         255.255.255.0   U     102    0        0 ens33
#route 添加-n参数，不解析dns
[root@local-gege network-scripts]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.178.2   0.0.0.0         UG    102    0        0 ens33
192.168.178.0   0.0.0.0         255.255.255.0   U     102    0        0 ens33
```
解释

- Destination：表示网络号，network的意思
- Gateway：网关地址，网络是通过该IP连接出去的，如果显示0.0.0.0代表该路由是直接本机传送出去的，如果有ip表示本条路由必须经过该IP才能连接出去。
- Genmask：子网掩码地址，也就是netmask，IP+NETMASK组成一个完整的网络
- Flags：路由标记信息，标记当前网络节点的状态
   - U Up表示此路由当前为启动状态。
   - H Host，表示此网关为一主机
   - G Gateway，表示此网关为一路由器。
   - R Reinstate Route，使用动态路由重新初始化的路由。
   - D Dynamically,此路由是动态性地写入。
   - M Modified，此路由是由路由守护程序或导向器动态修改。
   - ! 表示此路由当前为关闭状态，用于禁止不安全的网络
- Metric：需要经过几个网络节点才能到达路由的目标地址
- Ref：参考到此路由规则的数目
- Iface：路由对应的网络设备接口
```
192.168.178.0   0.0.0.0         255.255.255.0   U     102    0        0 ens33
表示主机所在网段是192.168.178.0
若数据传送目标在同一网段，可以直接通过ens33转发数据包
0.0.0.0         192.168.178.2   0.0.0.0         UG    102    0        0 ens33
是系统默认网关，表示去任何地方的请求，都转发给192.168.178.2网关去处理
```
### 添加和删除默认网关
默认网关就是数据包不匹配任何设定的路由规则最后流经的地址关口。
网关网关，网络的关口，就好比家里的门，外出就得经过访问，数据也是一样。
```
#此时我的机器，路由信息
[root@local-gege network-scripts]# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         bogon           0.0.0.0         UG    102    0        0 ens33
192.168.178.0   0.0.0.0         255.255.255.0   U     102    0        0 ens33
```
### 删除网关
```
[root@local-gege network-scripts]# route del default
[root@local-gege ~]# route
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.178.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33
```
### 添加网关
```
[root@local-gege ~]# route add default gw 192.168.178.2
[root@local-gege ~]# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.178.2   0.0.0.0         UG    0      0        0 ens33
192.168.178.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33
以上方式等同于
route add -net 0.0.0.0 gw 192.168.178.2
```
## arp命令
arp是地址解析协议（ARP、Address Resolution Protocol），主要功能是根据IP地址获取物理地址（MAC地址）
```
[描述]
    用来管理系统的arp缓存，常用的命令包括：
    arp: 显示所有的表项。
    arp  -d  address: 删除一个arp表项。
    arp  -s address hw_addr: 设置一个arp表项。
常用参数：
    -a 使用bsd形式输出。（没有固定的列）
    -n 使用数字形式显示ip地址，而不是默认的主机名形式。
    -D 不是指定硬件地址而是指定一个网络接口的名称，表项将使用相应接口的MAC地址。一般用来设置ARP代理。
    -H type, --hw-type type: 指定检查特定类型的表项，默认type为ether，还有其他类型。
    -i If, --device If: 指定设置哪个网络接口上面的arp表项。
    -f filename: 作用同'-s',不过它通过文件来指定IP地址和MAC地址的绑定。文件中每行分别是主机和MAC，中间以空格分割。如果没有指定文件名称，则使用/etc/ethers文件。
```
案例
```
显示arp缓存区的所有条目
[root@local-gege ~]# arp
Address                  HWtype  HWaddress           Flags Mask            Iface
bogon                    ether   00:50:56:eb:26:44   C                     ens33
bogon                    ether   00:50:56:c0:00:08   C                     ens33
Address：主机地址或是主机名
HWtype：硬件类型
HWaddress：硬件地址
Flags Mask：记录标志，C表示是arp缓存中的条目，M表示静态arp条目
Iface：网络接口
[root@local-gege ~]# arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.178.2            ether   00:50:56:eb:26:44   C                     ens33
192.168.178.1            ether   00:50:56:c0:00:08   C                     ens33
```
## ip命令
ip是iproute软件包里面的一个强大的网络配置工具，用于显示或管理Linux系统的路由、网络设备、策略路由等。
```
ip命令的用法如下：
ip [OPTIONS] OBJECT [COMMAND [ARGUMENTS]]
其中，OPTIONS是一些修改ip行为或者改变其输出的选项。所有的选项都是以-字符开头，分为长、短两种形式。目前，ip支持如下选项：
-V,-Version 打印ip的版本并退出。
-s,-stats,-statistics 输出更为详尽的信息。如果这个选项出现两次或者多次，输出的信息将更为详尽。
-f,-family 这个选项后面接协议种类，包括：inet、inet6或者link，强调使用的协议种类。如果没有足够的信息告诉ip使用的协议种类，ip就会使用默认值inet或者any。link比较特殊，它表示不涉及任何网络协议。
-4 是-family inet的简写。
-6 是-family inet6的简写。
-0 是-family link的简写。
-o,-oneline 对每行记录都使用单行输出，回行用字符代替。如果你需要使用wc、grep等工具处理ip的输出，会用到这个选项。
-r,-resolve 查询域名解析系统，用获得的主机名代替主机IP地址。
```
OBJECT对象
```
OBJECT是你要管理或者获取信息的对象。目前ip认识的对象包括：
link 网络设备
address 一个设备的协议（IP或者IPV6）地址
neighbour ARP或者NDISC缓冲区条目
route 路由表条目
rule 路由策略数据库中的规则
maddress 多播地址
mroute 多播路由缓冲区条目
tunnel IP上的通道
另外，所有的对象名都可以简写，例如：address可以简写为addr，甚至是a。
```
COMMAND
```
COMMAND设置针对指定对象执行的操作，它和对象的类型有关。一般情况下，ip支持对象的增加(add)、删除(delete)和展示(show或者list)。有些对象不支持所有这些操作，或者有其它的一些命令。对于所有的对象，用户可以使用help命令获得帮助。这个命令会列出这个对象支持的命令和参数的语法。如果没有指定对象的操作命令，ip会使用默认的命令。一般情况下，默认命令是list，如果对象不能列出，就会执行help命令。
```
ARGUMENTS
```
ARGUMENTS是命令的一些参数，它们倚赖于对象和命令。ip支持两种类型的参数：flag和parameter。flag由一个关键词组成；parameter由一个关键词加一个数值组成。为了方便，每个命令都有一个可以忽略的默认参数。例如，参数dev是ip link命令的默认参数，因此ip link ls eth0等于ip link ls dev eth0。我们将在后面的章节详细介绍每个命令的使用，命令的默认参数将使用default标出。
link支持：set、show
address支持：add、del、flush、show
```
### ip使用案例
显示ens33网卡信息
```
[root@local-gege ~]# ip link show dev ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:35:ee:89 brd ff:ff:ff:ff:ff:ff
```
-s参数显示详细信息
```
[root@local-gege ~]# ip -s  link show dev ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:35:ee:89 brd ff:ff:ff:ff:ff:ff
    RX: bytes  packets  errors  dropped overrun mcast    #显示每个网络设备上数据包的统计信息
    116094     1298     0       0       0       0
    TX: bytes  packets  errors  dropped carrier collsns
    102744     938      0       0       0       0
[root@local-gege ~]# ip -s -s link show dev ens33 #使用两个-s显示结果更详细w
```
### 关闭/激活网络设备
```
[root@local-gege ~]# ip link set ens33 down
[root@local-gege ~]# ip link set ens33 up
```
### 修改网卡MAC地址
```
[root@local-gege ~]# ip link set ens33 address 0:0c:29:13:10:11
[root@local-gege ~]# ip link show dev ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 00:0c:29:13:10:11 brd ff:ff:ff:ff:ff:ff
```
### 查看网卡信息
```
[root@local-gege ~]# ip address show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:13:10:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.178.180/24 brd 192.168.178.255 scope global noprefixroute ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::d2d8:6d71:84a:bacd/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
也可以用缩减命令 
[root@local-gege ~]# ip a
```
### 添加或删除IP地址
添加ip
```
[root@local-gege ~]# ip a add 192.168.178.111/24 dev ens33
[root@local-gege ~]#
[root@local-gege ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:13:10:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.178.180/24 brd 192.168.178.255 scope global noprefixroute ens33
       valid_lft forever preferred_lft forever
    inet 192.168.178.111/24 scope global secondary ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::d2d8:6d71:84a:bacd/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
[root@local-gege ~]# ip link set ens33 up
[root@local-gege ~]# ping 192.168.178.111
PING 192.168.178.111 (192.168.178.111) 56(84) bytes of data.
64 bytes from 192.168.178.111: icmp_seq=1 ttl=64 time=0.012 ms
```
删除ip
```
[root@local-gege ~]# ip a del 192.168.178.180/24 dev ens33  #此时ip已经被删掉，远程终端会断开
可以用另一个ip连接
yumac:~ yuchao$ ssh root@192.168.178.111
```
### ip命令添加别名
```
[root@local-gege ~]# ip a add 192.168.178.120/24 dev ens33 label ens33:1
#通过ifconfig命令检查
[root@local-gege ~]# ifconfig
```
### ip检查路由表
```
[root@local-gege ~]# ip route
default via 192.168.178.2 dev ens33 proto static metric 100
192.168.178.0/24 dev ens33 proto kernel scope link src 192.168.178.111
```
### ip检查arp缓存（显示网络邻居信息）
```
[root@local-gege ~]# ip neighbour
192.168.178.2 dev ens33 lladdr 00:50:56:eb:26:44 REACHABLE
192.168.178.1 dev ens33 lladdr 00:50:56:c0:00:08 DELAY
```
## netstat命令
netstat - 显示网络连接，路由表，接口状态，伪装连接，网络链路信息和组播成员组。
_描述_
```
语法参数
Netstat 程序显示Linux网络子系统的信息。 输出信息的类型是由第一个参数控制的，就像这样： [[ ]]
(none)
无选项时, netstat 显示打开的套接字. 如果不指定任何地址族，那么打印出所有已配置地址族的有效套接字。 [[ ]]
--route , -r
显示内核路由表。 [[ ]]
--groups , -g
显示IPv4 和 IPv6的IGMP组播组成员关系信息。 [[ ]]
--interface=iface , -i
显示所有网络接口列表或者是指定的 iface 。 [[ ]]
--masquerade , -M
显示一份所有经伪装的会话列表。 [[ ]]
--statistics , -s
显示每种协议的统计信息。 [[ ]]
```
_选项 OPTIONS_
```
--verbose , -v
详细模式运行。特别是打印一些关于未配置地址族的有用信息。 [[ ]]
--numeric , -n
显示数字形式地址而不是去解析主机、端口或用户名。 [[ ]]
--numeric-hosts
显示数字形式的主机但是不影响端口或用户名的解析。 [[ ]]
--numeric-ports
显示数字端口号，但是不影响主机或用户名的解析。 [[ ]]
--numeric-users
显示数字的用户ID，但是不影响主机和端口名的解析。 [[ ]]
--protocol=family , -A
指定要显示哪些连接的地址族(也许在底层协议中可以更好地描述)。 family 以逗号分隔的地址族列表，比如 inet , unix , ipx , ax25 , netrom , 和 ddp 。 这样和使用 --inet , --unix ( -x ), --ipx , --ax25 , --netrom, 和 --ddp 选项效果相同。 地址族 inet 包括raw, udp 和tcp 协议套接字。 [[ ]]
-c, --continuous
将使 netstat 不断地每秒输出所选的信息。 [[ ]]
-e, --extend
显示附加信息。使用这个选项两次来获得所有细节。 [[ ]]
-o, --timers
包含与网络定时器有关的信息。 [[ ]]
-p, --programs
显示套接字所属进程的PID和名称。 [[ ]]
-l, --listening
只显示正在侦听的套接字(这是默认的选项) [[ ]]
-a, --all
显示所有正在或不在侦听的套接字。加上 --interfaces 选项将显示没有标记的接口。 [[ ]]
-F
显示FIB中的路由信息。(这是默认的选项) [[ ]]
-C
显示路由缓冲中的路由信息。 [[ ]]
delay
netstat将循环输出统计信息，每隔 delay 秒。 [[ ]]
```
### 案例
```
[root@local-gege ~]# netstat -an
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
tcp        0     84 192.168.178.180:22      192.168.178.1:59434     ESTABLISHED
tcp        0      0 192.168.178.111:22      192.168.178.1:59794     ESTABLISHED
tcp6       0      0 :::22                   :::*                    LISTEN
tcp6       0      0 ::1:25                  :::*                    LISTEN
udp        0      0 127.0.0.1:323           0.0.0.0:*
udp6       0      0 ::1:323                 :::*
raw6       0      0 :::58                   :::*                    7
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ACC ]     STREAM     LISTENING     23567    private/tlsmgr
unix  2      [ ACC ]     STREAM     LISTENING     23570    private/rewrite
unix  2      [ ACC ]     STREAM     LISTENING     23573    private/bounce
unix  2      [ ACC ]     STREAM     LISTENING     23576    private/defer
```
_输出解释_
活动的Internet网络连接 (TCP, UDP, raw)
```
Proto
套接字使用的协议。 [[ ]]
Recv-Q
连接此套接字的用户程序未拷贝的字节数。 [[ ]]
Send-Q
远程主机未确认的字节数。 [[ ]]
Local Address
套接字的本地地址(本地主机名)和端口号。除非给定-n --numeric ( -n ) 选项，否则套接字地址按标准主机名(FQDN)进行解析，而端口号则转换到相应的服务名。 [[ ]]
Foreign Address
套接字的远程地址(远程主机名)和端口号。 Analogous to "Local Address." [[ ]]
State
套接字的状态。因为在RAW协议中没有状态，而且UDP也不用状态信息，所以此行留空。通常它为以下几个值之一：
ESTABLISHED
套接字有一个有效连接。
SYN_SENT
套接字尝试建立一个连接。
SYN_RECV
从网络上收到一个连接请求。
FIN_WAIT1
套接字已关闭，连接正在断开。
FIN_WAIT2
连接已关闭，套接字等待远程方中止。
TIME_WAIT
在关闭之后，套接字等待处理仍然在网络中的分组
CLOSED
套接字未用。
CLOSE_WAIT
远程方已关闭，等待套接字关闭。
LAST_ACK
远程方中止，套接字已关闭。等待确认。
LISTEN
套接字监听进来的连接。如果不设置 --listening (-l) 或者 --all (-a) 选项，将不显示出来这些连接。
CLOSING
套接字都已关闭，而还未把所有数据发出。
UNKNOWN
套接字状态未知。
```
_State_
```
此字段包含以下关键字之一：
FREE
套接字未分配。
LISTENING
套接字正在监听一个连接请求。除非设置 --listening (-l) 或者 --all (-a) 选项，否则不显示。
CONNECTING
套接字正要建立连接。
CONNECTED
套接字已连接。
DISCONNECTING
套接字已断开。
(empty)
套接字未连。
```
### netstat案例
常用组合参数
```
[root@local-gege ~]# netstat -tunlp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1272/sshd
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1400/master
tcp6       0      0 :::22                   :::*                    LISTEN      1272/sshd
tcp6       0      0 ::1:25                  :::*                    LISTEN      1400/master
udp        0      0 127.0.0.1:323           0.0.0.0:*                           985/chronyd
udp6       0      0 ::1:323                 :::*                                985/chronyd
```
参数解释

- -l：显示所有Listen监听中的网络连接
- -n：显示IP地址，不进行DNS解析成主机名、域名
- -t：显示所有tcp连接
- -u：显示所有udp连接
- -p：显示进程号与进程名
### 显示当前系统的路由表
效果等同于route -n
```
[root@local-gege ~]# netstat -rn
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
0.0.0.0         192.168.178.2   0.0.0.0         UG        0 0          0 ens33
192.168.178.0   0.0.0.0         255.255.255.0   U         0 0          0 ens33
```
### 显示网络的接口情况
```
[root@local-gege ~]# netstat -i
Kernel Interface table
Iface             MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
ens33            1500     2976      0      0 0          1950      0      0      0 BMRU
ens33:1          1500      - no statistics available -                        BMRU
lo              65536       13      0      0 0            13      0      0      0 LRU
```

- Iface：网络设备的接口名
- MTU：最大传输单元，单位是字节
- RX-OK/TX-OK：正确接收，发送了多少数据包
- RX-ERR/TX-ERR：接收、发送数据包时丢弃了多少数据包
- RX-OVR/TX-OVR：由于错误遗失了多少数据包
- Flg：接口标记
   - L：是回环地址
   - B：设置了广播地址
   - M：接收所有数据包
   - R：接口正在运行
   - U：接口正处于活动状态
   - O：表示在该接口上禁止arp
   - P：表示一个点到点的连接

正常丢包、错误包的数值如果不为0，说明网络存在问题，性能会下降
### netstat实战
检测nginx是否监听
```
[root@front01-web ~]# netstat -tunlp|grep nginx
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      32140/nginx: master
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      32140/nginx: master
```
统计服务器各状态的网络连接个数，利用awk的数组功能
```
[root@web ~]# netstat -n |awk '/^tcp/{++chaoge[$NF]} END {for(i in chaoge)print i,chaoge[i]}'
LAST_ACK 2
CLOSE_WAIT 151
ESTABLISHED 47
FIN_WAIT2 2
TIME_WAIT 59
```
## ss命令
ss命令是在centos7之后目的在于替代netstat的工具，用来查看网络状态信息，包括TCP、UDP、连接、端口等。优点在于能够显示更多详细的网络状态信息
如果系统没有ss命令，则需要安装下
```
[root@local-gege ~]# yum install iproute -y
```
ss命令参数
```
-a  显示所有网络连接
-l  显示LISTEN状态的连接(连接打开)
-m 显示内存信息(用于tcp_diag)
-o  显示Tcp 定时器x
-p  显示进程信息
-s  连接统计
-n  显示ip地址，不进行dns解析
-d  只显示 DCCP信息 (等同于 -A dccp)
-u  只显示udp信息 (等同于 -A udp)
-w 只显示 RAW信息 (等同于 -A raw)
-t 只显示tcp信息 (等同于 -A tcp)
-x 只显示Unix通讯信息 (等同于 -A unix)
-4 只显示 IPV4信息
-6 只显示 IPV6信息
--help 显示帮助信息
--version 显示版本信息
```
案例
```
#显示所有的socket连接
[root@local-gege ~]# ss -an
#格式化输出
[root@local-gege ~]# ss -an|column -t
```
_显示正在监听的TCP和UDP连接_
```
[root@local-gege ~]# ss -tunlp |column -t
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610857066239-2fb1b847-3790-49a6-bb97-009fb2fc273f.png#align=left&display=inline&height=290&margin=%5Bobject%20Object%5D&originHeight=290&originWidth=1574&size=0&status=done&style=none&width=1574)
_显示socket统计_
可以用于统计服务器链接数的宏观数据统计
```
[root@local-gege ~]# ss -s
Total: 570 (kernel 1071)
TCP:   5 (estab 1, closed 0, orphaned 0, synrecv 0, timewait 0/0), ports 0
Transport Total     IP        IPv6
*      1071      -         -
RAW      1         0         1
UDP      2         1         1
TCP      5         3         2
INET      8         4         4
FRAG      0         0         0
```
## ping命令
ping命令用于检测主机之间网络的连通性，执行ping命令使用ICMP传输协议，发出要求回应的信息。
参数
```
-c
    count 在发送(和接收)了正好数量为 count 的回显应答分组后停止操作。在发送了 count 个分组后没有收到任何分组的特别情况是发送导致了终止(选程主机或网关不可达)。
-d      
    在所用的套接字上使用SO_DEBUG 选项。
-f      
    以高速方式来作ping 。以分组返回的速度来输出其它分组或每秒输出百次。当收到每个回显应答并打印一个退格符时，对每个回显请求都打印一个句点``.。这可以快速显示出丢弃了多少个分组，只有超级用户可以用这个选项。这（操作）对网络要求非常苛刻，应该慎重使用。
-i
    wait 在发送每个分组时等待 wait 个秒数。缺省值为每个分组等待一秒。此选项与-f选项不能同时使用。
-l
    preload 如果指定 preload ，那么 ping 程序在开始正常运行模式前尽可能快地发送分组。同样只有超级用户可以用这个选项。
-n      
    只以数字形式输出信息。这样就不尝试去查找主机名了。
-p
    pattern 可以指定最多16个填充字节用于保持分组长度为16的整数倍。在网络上诊断与数据相关问题时此选项很有用。例如``-p ff将使发出的分组都用全1填充数据区。
-q      
    静态输出。在程序启动和结束时只显示摘要行。
-R      
    记录路由。在回显请求分组中包含记录路由选项并在相应的分组返回时显示路由缓冲区。注意IP首部的容量只能存放9条这样的路由。很多主机忽略或禁用此选项。
-r      
    在所连接的网络上旁路正常的选路表，直接向主机发送分组。如果主机未处于直接相连的网络上，那么返回一个错误。此选项可用来通过无路由接口对一台主机进行检测(例如当接口已被routed 程序丢弃后)。
-s
    packetsize 指定要发送数据的字节量。缺省值为 56 ，这正好在添加了 8 字节的 ICMP 首部后组装成 64 字节的 ICMP 数据报。
    详细模式输出。打印接收到的回显应答以外的ICMP分组。
-t
    设置存活数值TTL的大小-v      
-w
    waitsecs 在 waitsecs 秒后停止 ping 程序的执行。当试图检测不可达主机时此选项很有用。
```
### ping案例
_测试到目标及其的网络连通性_
```
[root@local-gege ~]# ping chengkanghua.top
PING chengkanghua.top (123.206.16.61) 56(84) bytes of data.
64 bytes from 123.206.16.61 (123.206.16.61): icmp_seq=1 ttl=128 time=57.8 ms
64 bytes from 123.206.16.61 (123.206.16.61): icmp_seq=2 ttl=128 time=54.3 ms
#ping命令跟着域名或是ip地址，会一直刷新ping的结果
#ping发送了56字节的数据
#从目标及其收到的数据是64字节，icmp_seq是收到的序列包，ttl是数据包的生存期，time是延迟
#直到ctrl + c 终止ping
--- chengkanghua.top ping statistics ---   #ping命令的统计结果
2 packets transmitted, 2 received, 0% packet loss, time 1001ms  #发了2个包，收到2个包
rtt min/avg/max/mdev = 54.387/56.100/57.813/1.713 ms            #最小/平均/最大/平均差
```
扩展知识
```
ping命令的输出信息中含有TTL值，Time To Life（生存期），指的是ICMP报文在网络中的存活时间。不同的操作系统发出的ICMP报文生存期不同，有32、64、128、255等。
```
_ping不通的情况_
```
1.pign不存在的网址，
[root@chaogelinux ~]# ping ss.qwe
ping: ss.qwe: 未知的名称或服务
2.ping的时候出现”Destination Host Unreachable“
```
_ping命令组合_
```
[root@local-gege ~]# ping -c 3 -i 3 -s 1024 -t 255 www.chengkanghua.top
PING www.chengkanghua.top (123.206.16.61) 1024(1052) bytes of data.
1032 bytes from 123.206.16.61 (123.206.16.61): icmp_seq=1 ttl=128 time=63.2 ms
1032 bytes from 123.206.16.61 (123.206.16.61): icmp_seq=2 ttl=128 time=63.0 ms
1032 bytes from 123.206.16.61 (123.206.16.61): icmp_seq=3 ttl=128 time=63.7 ms
--- www.chengkanghua.top ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 6011ms
rtt min/avg/max/mdev = 63.029/63.345/63.740/0.414 ms
#参数解释
-c 3 发送3次ICMP包
-i 3 每隔3秒发包
-s 1024 发送1024字节的数据包
-t 255 设置数据包存活值255
```
## telnet命令
telnet命令以前用于登录远程主机然后进行管理，但是telnet采用明文传输报文，安全性很低，因此几乎以及弃用telnet，采用更安全的SSH服务了。
大多数网络设备，还是使用telnet登录，且telnet主要用于判断服务器是否打开了远程端口。
_telnet使用_
```
1.首先可能需要安装
[root@local-gege ~]# yum install telnet -y
2.检测ssh端口是否开放
[root@local-gege ~]# telnet 123.206.16.61 22
Trying 123.206.16.61...
Connected to 123.206.16.61.
Escape character is '^]'.
SSH-2.0-OpenSSH_7.4
^]
telnet> q
Connection closed.
进入telnet后，ctrl+c也无法退出，根据输入，按下ctrl+]，然后进入telnet命令行，输入quit结束
```
_2.端口未打开_
```
[root@local-gege ~]# telnet 123.206.16.61 3306
Trying 123.206.16.61...
连接不上，表示端口服务未开启，或是端口禁止访问等问题
```
## ssh命令
ssh命令是openssh套件中的客户端连接工具，可以使用ssh加密协议远程登录服务器，实现对服务器的远程管理，在windows中使用Xshell、SecureCRT等远程工具，Linux或是MacOS使用ssh命令连接。
```
参数
-p port
    指定远程主机的端口. 可以在配置文件中对每个主机单独设定这个参数.
-t
    强制分配伪终端. 可以在远程机器上执行任何全屏幕(screen-based)程序, 所以非常有用, 例如菜单服务。即使没有本地终端，多个-t选项也会强制分配终端
-v 调试模式，打印关于运行情况的调试信息. 在调试连接, 认证和配置问题时非常有用
```
案例
```
远程登录服务器
yumac:~ yuchao$ ssh root@192.168.178.180
```
_指定端口，用户登录服务器_
```
yumac:~ yuchao$ ssh chaoge@192.168.178.180 -p 22
chaoge@192.168.178.180's password:
```
_远程执行服务器的命令_
```
yumac:~ yuchao$ ssh root@192.168.178.180 "free -m"
root@192.168.178.180's password:
              total        used        free      shared  buff/cache   available
Mem:           3862         144        3367          11         349        3443
Swap:          2047           0        2047
```
## wget命令
**wget命令**用来从指定的URL下载文件。wget非常稳定，它在带宽很窄的情况下和不稳定网络中有很强的适应性，如果是由于网络的原因下载失败，wget会不断的尝试，直到整个文件下载完毕。如果是服务器打断下载过程，它会再次联到服务器上从停止的地方继续下载。这对从那些限定了链接时间的服务器上下载大文件非常有用。
wget特点

- 支持断点下载
- 支持FTP和HTTP下载
- 支持代理服务器
```
用法： wget [选项]... [URL]...
长选项所必须的参数在使用短选项时也是必须的。
启动：
  -V,  --version           显示 Wget 的版本信息并退出。
  -h,  --help              打印此帮助。
  -b,  --background        启动后转入后台。
  -e,  --execute=COMMAND   运行一个“.wgetrc”风格的命令。
日志和输入文件：
  -o,  --output-file=FILE    将日志信息写入 FILE。
  -a,  --append-output=FILE  将信息添加至 FILE。
  -d,  --debug               打印大量调试信息。
  -q,  --quiet               安静模式 (无信息输出)。
  -v,  --verbose             详尽的输出 (此为默认值)。
  -nv, --no-verbose          关闭详尽输出，但不进入安静模式。
  -i,  --input-file=FILE     下载本地或外部 FILE 中的 URLs。
  -F,  --force-html          把输入文件当成 HTML 文件。
  -B,  --base=URL            解析与 URL 相关的
                             HTML 输入文件 (由 -i -F 选项指定)。
       --config=FILE         Specify config file to use.
下载：
  -t,  --tries=NUMBER            设置重试次数为 NUMBER (0 代表无限制)。
       --retry-connrefused       即使拒绝连接也是重试。
  -O,  --output-document=FILE    将文档写入 FILE。
  -nc, --no-clobber              skip downloads that would download to
                                 existing files (overwriting them).
  -c,  --continue                断点续传下载文件。
       --progress=TYPE           选择进度条类型。
  -N,  --timestamping            只获取比本地文件新的文件。
  --no-use-server-timestamps     不用服务器上的时间戳来设置本地文件。
  -S,  --server-response         打印服务器响应。
       --spider                  不下载任何文件。
  -T,  --timeout=SECONDS         将所有超时设为 SECONDS 秒。
       --dns-timeout=SECS        设置 DNS 查寻超时为 SECS 秒。
       --connect-timeout=SECS    设置连接超时为 SECS 秒。
       --read-timeout=SECS       设置读取超时为 SECS 秒。
  -w,  --wait=SECONDS            等待间隔为 SECONDS 秒。
       --waitretry=SECONDS       在获取文件的重试期间等待 1..SECONDS 秒。
       --random-wait             获取多个文件时，每次随机等待间隔
                                 0.5*WAIT...1.5*WAIT 秒。
       --no-proxy                禁止使用代理。
  -Q,  --quota=NUMBER            设置获取配额为 NUMBER 字节。
       --bind-address=ADDRESS    绑定至本地主机上的 ADDRESS (主机名或是 IP)。
       --limit-rate=RATE         限制下载速率为 RATE。
       --no-dns-cache            关闭 DNS 查寻缓存。
       --restrict-file-names=OS  限定文件名中的字符为 OS 允许的字符。
       --ignore-case             匹配文件/目录时忽略大小写。
  -4,  --inet4-only              仅连接至 IPv4 地址。
  -6,  --inet6-only              仅连接至 IPv6 地址。
       --prefer-family=FAMILY    首先连接至指定协议的地址
                                 FAMILY 为 IPv6，IPv4 或是 none。
       --user=USER               将 ftp 和 http 的用户名均设置为 USER。
       --password=PASS           将 ftp 和 http 的密码均设置为 PASS。
       --ask-password            提示输入密码。
       --no-iri                  关闭 IRI 支持。
       --local-encoding=ENC      IRI (国际化资源标识符) 使用 ENC 作为本地编码。
       --remote-encoding=ENC     使用 ENC 作为默认远程编码。
       --unlink                  remove file before clobber.
目录：
  -nd, --no-directories           不创建目录。
  -x,  --force-directories        强制创建目录。
  -nH, --no-host-directories      不要创建主目录。
       --protocol-directories     在目录中使用协议名称。
  -P,  --directory-prefix=PREFIX  以 PREFIX/... 保存文件
       --cut-dirs=NUMBER          忽略远程目录中 NUMBER 个目录层。
HTTP 选项：
       --http-user=USER        设置 http 用户名为 USER。
       --http-password=PASS    设置 http 密码为 PASS。
       --no-cache              不在服务器上缓存数据。
       --default-page=NAME     改变默认页
                               (默认页通常是“index.html”)。
  -E,  --adjust-extension      以合适的扩展名保存 HTML/CSS 文档。
       --ignore-length         忽略头部的‘Content-Length’区域。
       --header=STRING         在头部插入 STRING。
       --max-redirect          每页所允许的最大重定向。
       --proxy-user=USER       使用 USER 作为代理用户名。
       --proxy-password=PASS   使用 PASS 作为代理密码。
       --referer=URL           在 HTTP 请求头包含‘Referer: URL’。
       --save-headers          将 HTTP 头保存至文件。
  -U,  --user-agent=AGENT      标识为 AGENT 而不是 Wget/VERSION。
       --no-http-keep-alive    禁用 HTTP keep-alive (永久连接)。
       --no-cookies            不使用 cookies。
       --load-cookies=FILE     会话开始前从 FILE 中载入 cookies。
       --save-cookies=FILE     会话结束后保存 cookies 至 FILE。
       --keep-session-cookies  载入并保存会话 (非永久) cookies。
       --post-data=STRING      使用 POST 方式；把 STRING 作为数据发送。
       --post-file=FILE        使用 POST 方式；发送 FILE 内容。
       --content-disposition   当选中本地文件名时
                               允许 Content-Disposition 头部 (尚在实验)。
       --auth-no-challenge     发送不含服务器询问的首次等待
                               的基本 HTTP 验证信息。
HTTPS (SSL/TLS) 选项：
       --secure-protocol=PR     选择安全协议，可以是 auto、SSLv2、
                                SSLv3 或是 TLSv1 中的一个。
       --no-check-certificate   不要验证服务器的证书。
       --certificate=FILE       客户端证书文件。
       --certificate-type=TYPE  客户端证书类型，PEM 或 DER。
       --private-key=FILE       私钥文件。
       --private-key-type=TYPE  私钥文件类型，PEM 或 DER。
       --ca-certificate=FILE    带有一组 CA 认证的文件。
       --ca-directory=DIR       保存 CA 认证的哈希列表的目录。
       --random-file=FILE       带有生成 SSL PRNG 的随机数据的文件。
       --egd-file=FILE          用于命名带有随机数据的 EGD 套接字的文件。
FTP 选项：
       --ftp-user=USER         设置 ftp 用户名为 USER。
       --ftp-password=PASS     设置 ftp 密码为 PASS。
       --no-remove-listing     不要删除‘.listing’文件。
       --no-glob               不在 FTP 文件名中使用通配符展开。
       --no-passive-ftp        禁用“passive”传输模式。
       --retr-symlinks         递归目录时，获取链接的文件 (而非目录)。
递归下载：
  -r,  --recursive          指定递归下载。
  -l,  --level=NUMBER       最大递归深度 (inf 或 0 代表无限制，即全部下载)。
       --delete-after       下载完成后删除本地文件。
  -k,  --convert-links      让下载得到的 HTML 或 CSS 中的链接指向本地文件。
  -K,  --backup-converted   在转换文件 X 前先将它备份为 X.orig。
  -m,  --mirror             -N -r -l inf --no-remove-listing 的缩写形式。
  -p,  --page-requisites    下载所有用于显示 HTML 页面的图片之类的元素。
       --strict-comments    用严格方式 (SGML) 处理 HTML 注释。
递归接受/拒绝：
  -A,  --accept=LIST               逗号分隔的可接受的扩展名列表。
  -R,  --reject=LIST               逗号分隔的要拒绝的扩展名列表。
  -D,  --domains=LIST              逗号分隔的可接受的域列表。
       --exclude-domains=LIST      逗号分隔的要拒绝的域列表。
       --follow-ftp                跟踪 HTML 文档中的 FTP 链接。
       --follow-tags=LIST          逗号分隔的跟踪的 HTML 标识列表。
       --ignore-tags=LIST          逗号分隔的忽略的 HTML 标识列表。
  -H,  --span-hosts                递归时转向外部主机。
  -L,  --relative                  只跟踪有关系的链接。
  -I,  --include-directories=LIST  允许目录的列表。
  --trust-server-names             use the name specified by the redirection
                                   url last component.
  -X,  --exclude-directories=LIST  排除目录的列表。
  -np, --no-parent                 不追溯至父目录。
```
_下载单个的文件_
```
[root@local-gege ~]# wget http://chengkanghua.top/
--2019-12-10 14:50:27--  http://chengkanghua.top/
正在解析主机 chengkanghua.top (chengkanghua.top)... 123.206.16.61
正在连接 chengkanghua.top (chengkanghua.top)|123.206.16.61|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：141 [text/html]
正在保存至: “index.html”
100%[=================================================================>] 141         --.-K/s 用时 0s
2019-12-10 14:50:27 (11.1 MB/s) - 已保存 “index.html” [141/141])
[root@local-gege ~]# cat index.html
<meta charset=utf8>
<h1> 各位小伙伴，看懂了源代码编译安装了吗？我们再来一个骇客帝国编译安装，如何?</h1>
```
_下载文件，指定文件名保存到本地_
```
[root@local-gege ~]# wget -O /tmp/test.html www.chengkanghua.top
--2019-12-10 14:55:08--  http://www.chengkanghua.top/
正在解析主机 www.chengkanghua.top (www.chengkanghua.top)... 123.206.16.61
正在连接 www.chengkanghua.top (www.chengkanghua.top)|123.206.16.61|:80... 已连接。
已发出 HTTP 请求，正在等待回应... 200 OK
长度：141 [text/html]
正在保存至: “/tmp/test.html”
100%[=================================================================>] 141         --.-K/s 用时 0s
2019-12-10 14:55:08 (14.1 MB/s) - 已保存 “/tmp/test.html” [141/141])
```
_限速下载，限制每秒1k_
```
[root@local-gege ~]# wget --limit-rate=1k https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/lrzsz-0.12.20-36.el7.x86_64.rpm
```
_断点续传_
```
1.使用-c参数断点续传下载文件，可以直接强制中断
wget -c  --limit-rate=1k https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/lrzsz-0.12.20-36.el7.x86_64.rpm
2.断开之后可以继续执行命令
[root@local-gege tmp]# wget -c  --limit-rate=1k https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/lrzsz-0.12.20-36.el7.x86_64.rpm
--2019-12-10 15:46:16--  https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/lrzsz-0.12.20-36.el7.x86_64.rpm
正在解析主机 mirrors.aliyun.com (mirrors.aliyun.com)... 111.32.172.248, 111.32.172.244, 111.32.172.238, ...
正在连接 mirrors.aliyun.com (mirrors.aliyun.com)|111.32.172.248|:443... 已连接。
已发出 HTTP 请求，正在等待回应... 206 Partial Content
长度：79376 (78K)，剩余 61245 (60K) [application/x-redhat-package-manager]
正在保存至: “lrzsz-0.12.20-36.el7.x86_64.rpm”
23% [+++++++++++++++                                                   ] 18,746      1024B/s 
3.看到HTTP状态码 206 partial content 代表客户端请求一个未完成的资源，继续下载
```
_后台下载_
```
[root@local-gege tmp]# wget -b  --limit-rate=1k https://mirrors.aliyun.com/centos/7/os/x86_64/Packages/lrzsz-0.12.20-36.el7.x86_64.rpm
继续在后台运行，pid 为 6475。
将把输出写入至 “wget-log”。
可以实时监测日志内容
tail -f wget-log
```
_伪装代理下载_
有些网站会根据客户端身份进行判断，不是浏览器禁止下载，或者返回不同的页面，可以使用--user-agent参数伪装身份
```
1.下载电脑版资料
[root@local-gege tmp]# wget -O /tmp/luffy.html www.luffy.com
2.下载移动端版页面
[root@local-gege tmp]# wget --user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1" www.luffy.com
```
_检测网站url是否正常_
```
#检测$0的返回值，是0正常，非零表示网站有问题了
[root@local-gege tmp]# wget -q -T 3 --tries=1 --spider www.chengkanghua.top
[root@local-gege tmp]# echo $?
0
[root@local-gege tmp]# wget -q -T 3 --tries=1 --spider www.chengkanghua.top1
[root@local-gege tmp]# echo $?
4
```
## nslookup命令
nslookup 命令：用于查找域名服务器的程序，nslookup有两种模式：交互和非交互
此命令需要安装
```
[root@local-gege tmp]# yum install bind-utils -y
```
_交互模式_

```bash
ubuntu@VM-4-16-ubuntu:~$ cat /etc/resolv.conf
nameserver 127.0.0.53
options edns0
ubuntu@VM-4-16-ubuntu:~$ nslookup
> www.baidu.com    # 输入想解析的域名
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
www.baidu.com	canonical name = www.a.shifen.com.
Name:	www.a.shifen.com
Address: 112.80.248.75
Name:	www.a.shifen.com
Address: 112.80.248.76
```


_修改指定的dns服务器地址_

```
> server 223.5.5.5
Default server: 223.5.5.5
Address: 223.5.5.5#53
> www.chengkanghua.top
Server:        223.5.5.5
Address:    223.5.5.5#53
Non-authoritative answer:
Name:    www.chengkanghua.top
Address: 123.206.16.61
```
_非交互式_
```
[root@local-gege tmp]# nslookup www.chengkanghua.top
Server:        119.29.29.29
Address:    119.29.29.29#53
Non-authoritative answer:
Name:    www.chengkanghua.top
Address: 123.206.16.61
```
## nmap命令
nmap是一款开放源码的网络探测工具，全称Network Mapper
目的在于快速扫描大型网络，nmap可以发现网络上有哪些主机，主机提供了什么服务，并且探测操作系统类型等信息。
```
需要安装此命令
yum install nmap -y
```
语法参数
```
Nmap命令的格式为：
Nmap [ 扫描类型 ... ] [ 通用选项 ] { 扫描目标说明 }
下面对Nmap命令的参数按分类进行说明：
1. 扫描类型
-sV 探测服务版本信息
-sT    TCP connect()扫描，这是最基本的TCP扫描方式。这种扫描很容易被检测到，在目标主机的日志中会记录大批的连接请求以及错误信息。
-sS    TCP同步扫描(TCP SYN)，因为不必全部打开一个TCP连接，所以这项技术通常称为半开扫描(half-open)。这项技术最大的好处是，很少有系统能够把这记入系统日志。不过，你需要root权限来定制SYN数据包。
-sF,-sX,-sN    秘密FIN数据包扫描、圣诞树(Xmas Tree)、空(Null)扫描模式。这些扫描方式的理论依据是：关闭的端口需要对你的探测包回应RST包，而打开的端口必需忽略有问题的包(参考RFC 793第64页)。
-sP    ping扫描，用ping方式检查网络上哪些主机正在运行。当主机阻塞ICMP echo请求包是ping扫描是无效的。nmap在任何情况下都会进行ping扫描，只有目标主机处于运行状态，才会进行后续的扫描。
-sU    如果你想知道在某台主机上提供哪些UDP(用户数据报协议,RFC768)服务，可以使用此选项。
-sA    ACK扫描，这项高级的扫描方法通常可以用来穿过防火墙。
-sW    滑动窗口扫描，非常类似于ACK的扫描。
-sR    RPC扫描，和其它不同的端口扫描方法结合使用。
-b    FTP反弹攻击(bounce attack)，连接到防火墙后面的一台FTP服务器做代理，接着进行端口扫描。
2. 通用选项
-P0    在扫描之前，不ping主机。
-PT    扫描之前，使用TCP ping确定哪些主机正在运行。
-PS    对于root用户，这个选项让nmap使用SYN包而不是ACK包来对目标主机进行扫描。
-PI    设置这个选项，让nmap使用真正的ping(ICMP echo请求)来扫描目标主机是否正在运行。
-PB    这是默认的ping扫描选项。它使用ACK(-PT)和ICMP(-PI)两种扫描类型并行扫描。如果防火墙能够过滤其中一种包，使用这种方法，你就能够穿过防火墙。
-O    这个选项激活对TCP/IP指纹特征(fingerprinting)的扫描，获得远程主机的标志，也就是操作系统类型。
-I    打开nmap的反向标志扫描功能。
-f    使用碎片IP数据包发送SYN、FIN、XMAS、NULL。包增加包过滤、入侵检测系统的难度，使其无法知道你的企图。
-v    冗余模式。强烈推荐使用这个选项，它会给出扫描过程中的详细信息。
-S <IP>    在一些情况下，nmap可能无法确定你的源地址(nmap会告诉你)。在这种情况使用这个选项给出你的IP地址。
-g port    设置扫描的源端口。一些天真的防火墙和包过滤器的规则集允许源端口为DNS(53)或者FTP-DATA(20)的包通过和实现连接。显然，如果攻击者把源端口修改为20或者53，就可以摧毁防火墙的防护。
-oN    把扫描结果重定向到一个可读的文件logfilename中。
-oS    扫描结果输出到标准输出。
--host_timeout    设置扫描一台主机的时间，以毫秒为单位。默认的情况下，没有超时限制。
--max_rtt_timeout    设置对每次探测的等待时间，以毫秒为单位。如果超过这个时间限制就重传或者超时。默认值是大约9000毫秒。
--min_rtt_timeout    设置nmap对每次探测至少等待你指定的时间，以毫秒为单位。
-M count    置进行TCP connect()扫描时，最多使用多少个套接字进行并行的扫描。
3. 扫描目标
目标地址    可以为IP地址，CIRD地址等。如192.168.1.2，222.247.54.5/24
-iL filename    从filename文件中读取扫描的目标。
-iR    让nmap自己随机挑选主机进行扫描。
-p    端口 这个选项让你选择要进行扫描的端口号的范围。如：-p 20-30,139,60000。
-exclude    排除指定主机。
-excludefile    排除指定文件中的主机。
```
_案例_
**1.查看主机开放的端口，默认扫描1~1000的端口**
```
[root@local-gege tmp]# nmap 127.0.0.1
Starting Nmap 6.40 ( http://nmap.org ) at 2019-12-10 16:29 CST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000040s latency).
Not shown: 998 closed ports    #有998个端口关闭
PORT   STATE SERVICE
22/tcp open  ssh
25/tcp open  smtp
Nmap done: 1 IP address (1 host up) scanned in 0.07 seconds
```
_2.扫描指定端口范围_
```
[root@local-gege tmp]# nmap -p 1024-65535 127.0.0.1
Starting Nmap 6.40 ( http://nmap.org ) at 2019-12-10 16:48 CST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000040s latency).
All 64512 scanned ports on localhost (127.0.0.1) are closed
Nmap done: 1 IP address (1 host up) scanned in 1.21 seconds
```
_扫描局域网内的ip，端口开放情况_
```
nmap 192.168.178.0/24  #扫描局域网段的机器端口打开情况
```
_探测目标主机的服务和操作系统版本_
对于网络安全性较高的机器，最好能够屏蔽服务版本信息，防止黑客利用版本漏洞攻击
```
[root@chaogelinux ~]# nmap -O -sV  127.0.0.1    #-O显示系统版本,-sV探测服务版本信息
Starting Nmap 6.40 ( http://nmap.org ) at 2019-12-11 09:19 CST
Nmap scan report for VM_32_137_centos (127.0.0.1)
Host is up (0.000066s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.4 (protocol 2.0)
25/tcp open  smtp    Postfix smtpd
80/tcp open  http    nginx 1.12.0
Device type: general purpose
Running: Linux 3.X
OS CPE: cpe:/o:linux:linux_kernel:3
OS details: Linux 3.7 - 3.9
Network Distance: 0 hops
Service Info: Host:  chaogelinux.localdomain
OS and Service detection performed. Please report any incorrect results at http://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.77 seconds
```



