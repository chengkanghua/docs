# 1.  主从复制架构演变介绍

## 1.1 基本结构



```undefined
（1）一主一从
（2）一主多从
（3）多级主从
（4）双主
（5）循环复制
```

## 1.2 高级应用架构演变

### 1.2.1 高性能架构



```php
读写分离架构(读性能较高)
代码级别
MySQL proxy (Atlas,mysql router,proxySQL(percona),maxscale)、
amoeba(taobao)
xx-dbproxy等。
分布式架构(读写性能都提高):
分库分表——cobar--->TDDL(头都大了),DRDS
Mycat--->DBLE自主研发等。
NewSQL-->TiDB
```

### 1.2.2  高可用架构



```css
（3）单活:MMM架构——mysql-mmm（google）
（4）单活:MHA架构——mysql-master-ha（日本DeNa）,T-MHA
（5）多活:MGR ——5.7 新特性 MySQL Group replication(5.7.17) --->Innodb Cluster  
（6）多活:MariaDB Galera Cluster架构,(PXC)Percona XtraDB Cluster、MySQL Cluster(Oracle rac)架构
```

# 2. 高可用MHA       *****

## 2.1 架构工作原理



```undefined
主库宕机处理过程
1. 监控节点 (通过配置文件获取所有节点信息)
   系统,网络,SSH连接性
   主从状态,重点是主库

2. 选主
(1) 如果判断从库(position或者GTID),数据有差异,最接近于Master的slave,成为备选主
(2) 如果判断从库(position或者GTID),数据一致,按照配置文件顺序,选主.
(3) 如果设定有权重(candidate_master=1),按照权重强制指定备选主.
    1. 默认情况下如果一个slave落后master 100M的relay logs的话，即使有权重,也会失效.
    2. 如果check_repl_delay=0的化,即使落后很多日志,也强制选择其为备选主
3. 数据补偿
(1) 当SSH能连接,从库对比主库GTID 或者position号,立即将二进制日志保存至各个从节点并且应用(save_binary_logs )
(2) 当SSH不能连接, 对比从库之间的relaylog的差异(apply_diff_relay_logs) 
4. Failover
将备选主进行身份切换,对外提供服务
其余从库和新主库确认新的主从关系
5. 应用透明(VIP)
6. 故障切换通知(send_reprt)
7. 二次数据补偿(binlog_server)
8. 自愈自治(待开发...)
```

### 2.2 架构介绍:



```undefined
1主2从，master：db01   slave：db02   db03 ）：
MHA 高可用方案软件构成
Manager软件：选择一个从节点安装
Node软件：所有节点都要安装
```

## 2.3 MHA软件构成



```undefined
Manager工具包主要包括以下几个工具：
masterha_manger             启动MHA 
masterha_check_ssh      检查MHA的SSH配置状况 
masterha_check_repl         检查MySQL复制状况 
masterha_master_monitor     检测master是否宕机 
masterha_check_status       检测当前MHA运行状态 
masterha_master_switch  控制故障转移（自动或者手动）
masterha_conf_host      添加或删除配置的server信息

Node工具包主要包括以下几个工具：
这些工具通常由MHA Manager的脚本触发，无需人为操作
save_binary_logs            保存和复制master的二进制日志 
apply_diff_relay_logs       识别差异的中继日志事件并将其差异的事件应用于其他的
purge_relay_logs            清除中继日志（不会阻塞SQL线程）
```

## 2.4  MHA环境搭建

### 2.4.1 规划:



```undefined
主库: 51    node 
从库: 
52      node
53      node    manager
```

### 2.4.2 准备环境（略。1主2从GTID）

### 2.4.3 配置关键程序软连接



```kotlin
ln -s /data/mysql/bin/mysqlbinlog    /usr/bin/mysqlbinlog
ln -s /data/mysql/bin/mysql          /usr/bin/mysql
```

### 2.4.4  配置各节点互信



```ruby
db01：
rm -rf /root/.ssh 
ssh-keygen
cd /root/.ssh 
mv id_rsa.pub authorized_keys
scp  -r  /root/.ssh  10.0.0.52:/root 
scp  -r  /root/.ssh  10.0.0.53:/root 
各节点验证
db01:
ssh 10.0.0.51 date
ssh 10.0.0.52 date
ssh 10.0.0.53 date
db02:
ssh 10.0.0.51 date
ssh 10.0.0.52 date
ssh 10.0.0.53 date
db03:
ssh 10.0.0.51 date
ssh 10.0.0.52 date
ssh 10.0.0.53 date
```

### 2.4.5 安装软件

### 下载mha软件



```cpp
mha官网：https://code.google.com/archive/p/mysql-master-ha/
github下载地址：https://github.com/yoshinorim/mha4mysql-manager/wiki/Downloads
```

### 所有节点安装Node软件依赖包



```css
yum install perl-DBD-MySQL -y
rpm -ivh mha4mysql-node-0.56-0.el6.noarch.rpm
```

### 在db01主库中创建mha需要的用户



```css
 grant all privileges on *.* to mha@'10.0.0.%' identified by 'mha';
```

### Manager软件安装（db03）



```css
yum install -y perl-Config-Tiny epel-release perl-Log-Dispatch perl-Parallel-ForkManager perl-Time-HiRes
rpm -ivh mha4mysql-manager-0.56-0.el6.noarch.rpm
```

### 2.4.6 配置文件准备(db03)



```csharp
创建配置文件目录
 mkdir -p /etc/mha
创建日志目录
 mkdir -p /var/log/mha/app1
编辑mha配置文件
vim /etc/mha/app1.cnf
[server default]
manager_log=/var/log/mha/app1/manager        
manager_workdir=/var/log/mha/app1            
master_binlog_dir=/data/binlog       
user=mha                                   
password=mha                               
ping_interval=2
repl_password=123
repl_user=repl
ssh_user=root                               
[server1]                                   
hostname=10.0.0.51
port=3306                                  
[server2]            
hostname=10.0.0.52
port=3306
[server3]
hostname=10.0.0.53
port=3306
```

### 2.4.7 状态检查



```kotlin
### 互信检查
masterha_check_ssh  --conf=/etc/mha/app1.cnf 
Fri Apr 19 16:39:34 2019 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
Fri Apr 19 16:39:34 2019 - [info] Reading application default configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:39:34 2019 - [info] Reading server configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:39:34 2019 - [info] Starting SSH connection tests..
Fri Apr 19 16:39:35 2019 - [debug] 
Fri Apr 19 16:39:34 2019 - [debug]  Connecting via SSH from root@10.0.0.51(10.0.0.51:22) to root@10.0.0.52(10.0.0.52:22)..
Fri Apr 19 16:39:34 2019 - [debug]   ok.
Fri Apr 19 16:39:34 2019 - [debug]  Connecting via SSH from root@10.0.0.51(10.0.0.51:22) to root@10.0.0.53(10.0.0.53:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:36 2019 - [debug] 
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.52(10.0.0.52:22) to root@10.0.0.51(10.0.0.51:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.52(10.0.0.52:22) to root@10.0.0.53(10.0.0.53:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:37 2019 - [debug] 
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.53(10.0.0.53:22) to root@10.0.0.51(10.0.0.51:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.53(10.0.0.53:22) to root@10.0.0.52(10.0.0.52:22)..
Fri Apr 19 16:39:36 2019 - [debug]   ok.
Fri Apr 19 16:39:37 2019 - [info] All SSH connection tests passed successfully.
```

### 主从状态检查



```kotlin
[root@db03 ~]# masterha_check_ssh  --conf=/etc/mha/app1.cnf 
Fri Apr 19 16:39:34 2019 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
Fri Apr 19 16:39:34 2019 - [info] Reading application default configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:39:34 2019 - [info] Reading server configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:39:34 2019 - [info] Starting SSH connection tests..
Fri Apr 19 16:39:35 2019 - [debug] 
Fri Apr 19 16:39:34 2019 - [debug]  Connecting via SSH from root@10.0.0.51(10.0.0.51:22) to root@10.0.0.52(10.0.0.52:22)..
Fri Apr 19 16:39:34 2019 - [debug]   ok.
Fri Apr 19 16:39:34 2019 - [debug]  Connecting via SSH from root@10.0.0.51(10.0.0.51:22) to root@10.0.0.53(10.0.0.53:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:36 2019 - [debug] 
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.52(10.0.0.52:22) to root@10.0.0.51(10.0.0.51:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.52(10.0.0.52:22) to root@10.0.0.53(10.0.0.53:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:37 2019 - [debug] 
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.53(10.0.0.53:22) to root@10.0.0.51(10.0.0.51:22)..
Fri Apr 19 16:39:35 2019 - [debug]   ok.
Fri Apr 19 16:39:35 2019 - [debug]  Connecting via SSH from root@10.0.0.53(10.0.0.53:22) to root@10.0.0.52(10.0.0.52:22)..
Fri Apr 19 16:39:36 2019 - [debug]   ok.
Fri Apr 19 16:39:37 2019 - [info] All SSH connection tests passed successfully.
[root@db03 ~]# masterha_check_repl  --conf=/etc/mha/app1.cnf 
Fri Apr 19 16:40:50 2019 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
Fri Apr 19 16:40:50 2019 - [info] Reading application default configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:40:50 2019 - [info] Reading server configuration from /etc/mha/app1.cnf..
Fri Apr 19 16:40:50 2019 - [info] MHA::MasterMonitor version 0.56.
Fri Apr 19 16:40:51 2019 - [info] GTID failover mode = 1
Fri Apr 19 16:40:51 2019 - [info] Dead Servers:
Fri Apr 19 16:40:51 2019 - [info] Alive Servers:
Fri Apr 19 16:40:51 2019 - [info]   10.0.0.51(10.0.0.51:3306)
Fri Apr 19 16:40:51 2019 - [info]   10.0.0.52(10.0.0.52:3306)
Fri Apr 19 16:40:51 2019 - [info]   10.0.0.53(10.0.0.53:3306)
Fri Apr 19 16:40:51 2019 - [info] Alive Slaves:
Fri Apr 19 16:40:51 2019 - [info]   10.0.0.52(10.0.0.52:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Fri Apr 19 16:40:51 2019 - [info]     GTID ON
Fri Apr 19 16:40:51 2019 - [info]     Replicating from 10.0.0.51(10.0.0.51:3306)
Fri Apr 19 16:40:51 2019 - [info]   10.0.0.53(10.0.0.53:3306)  Version=5.7.20-log (oldest major version between slaves) log-bin:enabled
Fri Apr 19 16:40:51 2019 - [info]     GTID ON
Fri Apr 19 16:40:51 2019 - [info]     Replicating from 10.0.0.51(10.0.0.51:3306)
Fri Apr 19 16:40:51 2019 - [info] Current Alive Master: 10.0.0.51(10.0.0.51:3306)
Fri Apr 19 16:40:51 2019 - [info] Checking slave configurations..
Fri Apr 19 16:40:51 2019 - [info]  read_only=1 is not set on slave 10.0.0.52(10.0.0.52:3306).
Fri Apr 19 16:40:51 2019 - [info]  read_only=1 is not set on slave 10.0.0.53(10.0.0.53:3306).
Fri Apr 19 16:40:51 2019 - [info] Checking replication filtering settings..
Fri Apr 19 16:40:51 2019 - [info]  binlog_do_db= , binlog_ignore_db= 
Fri Apr 19 16:40:51 2019 - [info]  Replication filtering check ok.
Fri Apr 19 16:40:51 2019 - [info] GTID (with auto-pos) is supported. Skipping all SSH and Node package checking.
Fri Apr 19 16:40:51 2019 - [info] Checking SSH publickey authentication settings on the current master..
Fri Apr 19 16:40:51 2019 - [info] HealthCheck: SSH to 10.0.0.51 is reachable.
Fri Apr 19 16:40:51 2019 - [info] 
10.0.0.51(10.0.0.51:3306) (current master)
 +--10.0.0.52(10.0.0.52:3306)
 +--10.0.0.53(10.0.0.53:3306)

Fri Apr 19 16:40:51 2019 - [info] Checking replication health on 10.0.0.52..
Fri Apr 19 16:40:51 2019 - [info]  ok.
Fri Apr 19 16:40:51 2019 - [info] Checking replication health on 10.0.0.53..
Fri Apr 19 16:40:51 2019 - [info]  ok.
Fri Apr 19 16:40:51 2019 - [warning] master_ip_failover_script is not defined.
Fri Apr 19 16:40:51 2019 - [warning] shutdown_script is not defined.
Fri Apr 19 16:40:51 2019 - [info] Got exit code 0 (Not master dead).
MySQL Replication Health is OK.
```

### 2.4.8  开启MHA(db03)：



```ruby
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover  < /dev/null> /var/log/mha/app1/manager.log 2>&1 &
```

### 2.4.9  查看MHA状态



```ruby
[root@db03 ~]# masterha_check_status --conf=/etc/mha/app1.cnf
app1 (pid:4719) is running(0:PING_OK), master:10.0.0.51
[root@db03 ~]# mysql -umha -pmha -h 10.0.0.51 -e "show variables like 'server_id'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| server_id     | 51    |
+---------------+-------+
[root@db03 ~]# mysql -umha -pmha -h 10.0.0.52 -e "show variables like 'server_id'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| server_id     | 52    |
+---------------+-------+
[root@db03 ~]# mysql -umha -pmha -h 10.0.0.53 -e "show variables like 'server_id'"
mysql: [Warning] Using a password on the command line interface can be insecure.
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| server_id     | 53    |
+---------------+-------+
```

### 2.4.10 故障模拟及处理



```bash
### 停主库db01:    
/etc/init.d/mysqld stop

观察manager  日志 tail -f /var/log/mha/app1/manager
末尾必须显示successfully，才算正常切换成功。                            
```

### 修复主库



```csharp
[root@db01 ~]# /etc/init.d/mysqld start
```

### 恢复主从结构



```bash
CHANGE MASTER TO 
MASTER_HOST='10.0.0.52',
MASTER_PORT=3306, 
MASTER_AUTO_POSITION=1, 
MASTER_USER='repl', 
MASTER_PASSWORD='123';
start slave ;
```

### 修改配置文件



```csharp
[server1]
hostname=10.0.0.51
port=3306
```

### 启动MHA



```ruby
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover  < /dev/null> /var/log/mha/app1/manager.log 2>&1 &
```

### 2.4.11  Manager额外参数介绍



```bash
说明：
主库宕机谁来接管？
1. 所有从节点日志都是一致的，默认会以配置文件的顺序去选择一个新主。
2. 从节点日志不一致，自动选择最接近于主库的从库
3. 如果对于某节点设定了权重（candidate_master=1），权重节点会优先选择。
但是此节点日志量落后主库100M日志的话，也不会被选择。可以配合check_repl_delay=0，关闭日志量的检查，强制选择候选节点。

(1)  ping_interval=1
#设置监控主库，发送ping包的时间间隔，尝试三次没有回应的时候自动进行failover
(2) candidate_master=1
#设置为候选master，如果设置该参数以后，发生主从切换以后将会将此从库提升为主库，即使这个主库不是集群中事件最新的slave
(3)check_repl_delay=0
#默认情况下如果一个slave落后master 100M的relay logs的话，
MHA将不会选择该slave作为一个新的master，因为对于这个slave的恢复需要花费很长时间，通过设置check_repl_delay=0,MHA触发切换在选择一个新的master的时候将会忽略复制延时，这个参数对于设置了candidate_master=1的主机非常有用，因为这个候选主在切换的过程中一定是新的master
```

### 2.4.12 MHA 的vip功能

### 参数



```bash
master_ip_failover_script=/usr/local/bin/master_ip_failover
注意：/usr/local/bin/master_ip_failover，必须事先准备好
```

### 修改脚本内容



```bash
vi  /usr/local/bin/master_ip_failover
my $vip = '10.0.0.55/24';
my $key = '1';
my $ssh_start_vip = "/sbin/ifconfig eth0:$key $vip";
my $ssh_stop_vip = "/sbin/ifconfig eth0:$key down";
```

### 更改manager配置文件：



```ruby
vi /etc/mha/app1.cnf
添加：
master_ip_failover_script=/usr/local/bin/master_ip_failover
注意：
[root@db03 ~]# dos2unix /usr/local/bin/master_ip_failover 
dos2unix: converting file /usr/local/bin/master_ip_failover to Unix format ...
[root@db03 ~]# chmod +x /usr/local/bin/master_ip_failover 
```

### 主库上，手工生成第一个vip地址



```undefined
手工在主库上绑定vip，注意一定要和配置文件中的ethN一致，我的是eth0:1(1是key指定的值)
ifconfig eth0:1 10.0.0.55/24
```

### 重启mha



```jsx
masterha_stop --conf=/etc/mha/app1.cnf
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover < /dev/null > /var/log/mha/app1/manager.log 2>&1 &
```

### 2.4.13 邮件提醒



```jsx
1. 参数：
report_script=/usr/local/bin/send
2. 准备邮件脚本
send_report
(1)准备发邮件的脚本(上传 email_2019-最新.zip中的脚本，到/usr/local/bin/中)
(2)将准备好的脚本添加到mha配置文件中,让其调用

3. 修改manager配置文件，调用邮件脚本
vi /etc/mha/app1.cnf
report_script=/usr/local/bin/send

（3）停止MHA
masterha_stop --conf=/etc/mha/app1.cnf
（4）开启MHA    
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover < /dev/null > /var/log/mha/app1/manager.log 2>&1 &
        
(5) 关闭主库,看警告邮件  
故障修复：
1. 恢复故障节点
（1）实例宕掉
/etc/init.d/mysqld start 
（2）主机损坏，有可能数据也损坏了
备份并恢复故障节点。
2.恢复主从环境
看日志文件：
CHANGE MASTER TO MASTER_HOST='10.0.0.52', MASTER_PORT=3306, MASTER_AUTO_POSITION=1, MASTER_USER='repl', MASTER_PASSWORD='123';
start slave ;
3.恢复manager
3.1 修好的故障节点配置信息，加入到配置文件
[server1]
hostname=10.0.0.51
port=3306
3.2 启动manager   
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover < /dev/null > /var/log/mha/app1/manager.log 2>&1 &
```

### 2.4.14 binlog server（db03）

### 参数：



```csharp
binlogserver配置：
找一台额外的机器，必须要有5.6以上的版本，支持gtid并开启，我们直接用的第二个slave（db03）
vim /etc/mha/app1.cnf 
[binlog1]
no_master=1
hostname=10.0.0.53
master_binlog_dir=/data/mysql/binlog
```

### 创建必要目录



```kotlin
mkdir -p /data/mysql/binlog
chown -R mysql.mysql /data/*
修改完成后，将主库binlog拉过来（从000001开始拉，之后的binlog会自动按顺序过来）
```

### 拉取主库binlog日志



```bash
cd /data/mysql/binlog     -----》必须进入到自己创建好的目录
mysqlbinlog  -R --host=10.0.0.52 --user=mha --password=mha --raw  --stop-never mysql-bin.000001 &
注意：
拉取日志的起点,需要按照目前从库的已经获取到的二进制日志点为起点
```

### 重启MHA



```jsx
masterha_stop --conf=/etc/mha/app1.cnf
nohup masterha_manager --conf=/etc/mha/app1.cnf --remove_dead_master_conf --ignore_last_failover < /dev/null > /var/log/mha/app1/manager.log 2>&1 &
```

### 故障处理



```undefined
主库宕机，binlogserver 自动停掉，manager 也会自动停止。
处理思路：
1、重新获取新主库的binlog到binlogserver中
2、重新配置文件binlog server信息
3、最后再启动MHA
```

# 3.管理员在高可用架构维护的职责



```css
1. 搭建：MHA+VIP+SendReport+BinlogServer
2. 监控及故障处理
3.  高可用架构的优化
 核心是：尽可能降低主从的延时，让MHA花在数据补偿上的时间尽量减少。
5.7 版本，开启GTID模式，开启从库SQL并发复制。 
```

