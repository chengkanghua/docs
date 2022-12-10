# 1. 延时从库

## 1.1介绍



```undefined
是我们认为配置的一种特殊从库.人为配置从库和主库延时N小时.
```

## 1.2 为什么要有延时从



```undefined
数据库故障?
物理损坏
主从复制非常擅长解决物理损坏.
逻辑损坏
普通主从复制没办法解决逻辑损坏
```

## 1.3 配置延时从库



```cpp
SQL线程延时:数据已经写入relaylog中了,SQL线程"慢点"运行
一般企业建议3-6小时,具体看公司运维人员对于故障的反应时间

mysql>stop slave;
mysql>CHANGE MASTER TO MASTER_DELAY = 300;
mysql>start slave;
mysql> show slave status \G
SQL_Delay: 300
SQL_Remaining_Delay: NULL
```

## 1.4 延时从库应用

### 1.4.1 故障恢复思路



```undefined
1主1从,从库延时5分钟,主库误删除1个库
1. 5分钟之内 侦测到误删除操作
2. 停从库SQL线程
3. 截取relaylog
起点 :停止SQL线程时,relay最后应用位置
终点:误删除之前的position(GTID)
4. 恢复截取的日志到从库
5. 从库身份解除,替代主库工作
```

### 1.4.2 故障模拟及恢复



```css
1.主库数据操作
db01 [(none)]>create database relay charset utf8;
db01 [(none)]>use relay
db01 [relay]>create table t1 (id int);
db01 [relay]>insert into t1 values(1);
db01 [relay]>drop database relay;
```



```undefined
2. 停止从库SQL线程
stop slave sql_thread;
```



```kotlin
3. 找relaylog的截取起点和终点
起点:
Relay_Log_File: db01-relay-bin.000002
Relay_Log_Pos: 482
终点:
show relaylog events in 'db01-relay-bin.000002'
| db01-relay-bin.000002 | 1046 | Xid            |         7 |        2489 | COMMIT /* xid=144 */                  |
| db01-relay-bin.000002 | 1077 | Anonymous_Gtid |         7 |        2554 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'  |
mysqlbinlog --start-position=482 --stop-position=1077  /data/3308/data/db01-relay-bin.000002>/tmp/relay.sql
```

1. 从库恢复relaylog



```bash
source /tmp/relay.sql
```

5.从库身份解除



```css
db01 [relay]>stop slave;
db01 [relay]>reset slave all
```

# 2. 半同步            ***



```undefined
解决主从数据一致性问题
```

## 2.1 半同步复制工作原理的变化



```dart
1. 主库执行新的事务,commit时,更新 show master  status\G ,触发一个信号给
2. binlog dump 接收到主库的 show master status\G信息,通知从库日志更新了
3. 从库IO线程请求新的二进制日志事件
4. 主库会通过dump线程传送新的日志事件,给从库IO线程
5. 从库IO线程接收到binlog日志,当日志写入到磁盘上的relaylog文件时,给主库ACK_receiver线程
6. ACK_receiver线程触发一个事件,告诉主库commit可以成功了
7. 如果ACK达到了我们预设值的超时时间,半同步复制会切换为原始的异步复制.
```

## 2.2 配置半同步复制



```dart
加载插件
主:
INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';
从:
INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';
查看是否加载成功:
show plugins;
启动:
主:
SET GLOBAL rpl_semi_sync_master_enabled = 1;
从:
SET GLOBAL rpl_semi_sync_slave_enabled = 1;
重启从库上的IO线程
STOP SLAVE IO_THREAD;
START SLAVE IO_THREAD;
查看是否在运行
主:
show status like 'Rpl_semi_sync_master_status';
从:
show status like 'Rpl_semi_sync_slave_status';
```

# 3 . 过滤复制

## 3.1 说明

主库：



```dart
show master status;
Binlog_Do_DB
Binlog_Ignore_DB 
```

从库：



```dart
show slave status\G
Replicate_Do_DB: 
Replicate_Ignore_DB: 
```

3.2 实现过程



```csharp
mysqldump -S /data/3307/mysql.sock -A --master-data=2 --single-transaction  -R --triggers >/backup/full.sql

vim  /backup/full.sql
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000002', MASTER_LOG_POS=154;

[root@db01 ~]# mysql -S /data/3309/mysql.sock 
source /backup/full.sql

CHANGE MASTER TO
MASTER_HOST='10.0.0.51',
MASTER_USER='repl',
MASTER_PASSWORD='123',
MASTER_PORT=3307,
MASTER_LOG_FILE='mysql-bin.000002',
MASTER_LOG_POS=154,
MASTER_CONNECT_RETRY=10;
start  slave;
[root@db01 ~]# vim /data/3309/my.cnf 
replicate_do_db=ppt
replicate_do_db=word
[root@db01 ~]# systemctl restart mysqld3309

主库：
Master [(none)]>create database word;
Query OK, 1 row affected (0.00 sec)
Master [(none)]>create database ppt;
Query OK, 1 row affected (0.00 sec)
Master [(none)]>create database excel;
Query OK, 1 row affected (0.01 sec)
```

# 4. GTID复制

## 4.1  GTID引入

## 4.2 GTID介绍



```objectivec
GTID(Global Transaction ID)是对于一个已提交事务的唯一编号，并且是一个全局(主从复制)唯一的编号。
它的官方定义如下：
GTID = source_id ：transaction_id
7E11FA47-31CA-19E1-9E56-C43AA21293967:29
什么是sever_uuid，和Server-id 区别？
核心特性: 全局唯一,具备幂等性
```

# 4.3 GTID核心参数

重要参数：



```bash
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1

gtid-mode=on                        --启用gtid类型，否则就是普通的复制架构
enforce-gtid-consistency=true               --强制GTID的一致性
log-slave-updates=1                 --slave更新是否记入日志
```

## 4.4  GTID复制配置过程：

### 4.4.1 清理环境



```kotlin
pkill mysqld
 \rm -rf /data/mysql/data/*
 \rm -rf /data/binlog/*
```

### 4.4.2 准备配置文件



```kotlin
主库db01：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql/
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=51
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db01 [\\d]>
EOF

slave1(db02)：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=52
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db02 [\\d]>
EOF

slave2(db03)：
cat > /etc/my.cnf <<EOF
[mysqld]
basedir=/data/mysql
datadir=/data/mysql/data
socket=/tmp/mysql.sock
server_id=53
port=3306
secure-file-priv=/tmp
autocommit=0
log_bin=/data/binlog/mysql-bin
binlog_format=row
gtid-mode=on
enforce-gtid-consistency=true
log-slave-updates=1
[mysql]
prompt=db03 [\\d]>
EOF
```

### 4.4.3 初始化数据



```kotlin
mysqld --initialize-insecure --user=mysql --basedir=/data/mysql  --datadir=/data/mysql/data 
```

### 4.4.4 启动数据库



```kotlin
/etc/init.d/mysqld start
```

### 4.4.5 构建主从：



```csharp
master:51
slave:52,53

51:
grant replication slave  on *.* to repl@'10.0.0.%' identified by '123';

52\53:
change master to 
master_host='10.0.0.51',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;

start slave;
```

## 4.5 GTID 从库误写入操作处理



```rust
查看监控信息:
Last_SQL_Error: Error 'Can't create database 'oldboy'; database exists' on query. Default database: 'oldboy'. Query: 'create database oldboy'

Retrieved_Gtid_Set: 71bfa52e-4aae-11e9-ab8c-000c293b577e:1-3
Executed_Gtid_Set:  71bfa52e-4aae-11e9-ab8c-000c293b577e:1-2,
7ca4a2b7-4aae-11e9-859d-000c298720f6:1

注入空事物的方法：

stop slave;
set gtid_next='99279e1e-61b7-11e9-a9fc-000c2928f5dd:3';
begin;commit;
set gtid_next='AUTOMATIC';
    
这里的xxxxx:N 也就是你的slave sql thread报错的GTID，或者说是你想要跳过的GTID。
最好的解决方案：重新构建主从环境
```

## 4.6  GTID 复制和普通复制的区别



```dart
CHANGE MASTER TO
MASTER_HOST='10.0.0.51',
MASTER_USER='repl',
MASTER_PASSWORD='123',
MASTER_PORT=3307,
MASTER_LOG_FILE='mysql-bin.000001',
MASTER_LOG_POS=444,
MASTER_CONNECT_RETRY=10;

change master to 
master_host='10.0.0.51',
master_user='repl',
master_password='123' ,
MASTER_AUTO_POSITION=1;
start slave;

（0）在主从复制环境中，主库发生过的事务，在全局都是由唯一GTID记录的，更方便Failover
（1）额外功能参数（3个）
（2）change master to 的时候不再需要binlog 文件名和position号,MASTER_AUTO_POSITION=1;
（3）在复制过程中，从库不再依赖master.info文件，而是直接读取最后一个relaylog的 GTID号
（4） mysqldump备份时，默认会将备份中包含的事务操作，以以下方式
    SET @@GLOBAL.GTID_PURGED='8c49d7ec-7e78-11e8-9638-000c29ca725d:1';
    告诉从库，我的备份中已经有以上事务，你就不用运行了，直接从下一个GTID开始请求binlog就行。
```



