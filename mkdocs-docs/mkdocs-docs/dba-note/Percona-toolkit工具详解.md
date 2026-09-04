# 1. pt工具安装



```css
[root@master ~]# yum install -y  percona-toolkit-3.1.0-2.el7.x86_64.rpm
```

# 2. 常用工具使用介绍

## 2.1 pt-archiver 归档表



```bash
# 重要参数
--limit 100       每次取100行数据用pt-archive处理    
--txn-size  100   设置100行为一个事务提交一次，    
--where 'id<3000'  设置操作条件    
--progress 5000     每处理5000行输出一次处理信息    
--statistics       输出执行过程及最后的操作统计。（只要不加上--quiet，默认情况下pt- archive都会输出执行过程的）    
--charset=UTF8     指定字符集为UTF8—这个最后加上不然可能出现乱码。    
--bulk-delete      批量删除source上的旧数据(例如每次1000行的批量删除操作)
使用案例：
1.归档到数据库

pt-archiver --source h=10.0.0.11,D=world,t=city,u=root,p=123 --dest h=10.0.0.11,D=world,t=city2,u=root,p=123 --where 'id<1000' --no-check-charset --no-delete --limit=100 --commit-each --progress 200 --statistics

2.只清理数据

pt-archiver --source h=127.0.0.1,D=world,t=city2,u=root,p=123 --where 'id<100' --purge --limit=1 --no-check-charset

3.只把数据导出到外部文件，但是不删除源表里的数据
pt-archiver --source h=10.0.0.11,D=world,t=city,u=root,p=123 --where '1=1' --no-check-charset --no-delete --file="/tmp/archiver.dat" 
```

2.2 pt-osc



```bash
pt-osc工作流程：
1、检查更改表是否有主键或唯一索引，是否有触发器
2、检查修改表的表结构，创建一个临时表，在新表上执行ALTER TABLE语句
3、在源表上创建三个触发器分别对于INSERT UPDATE DELETE操作
4、从源表拷贝数据到临时表，在拷贝过程中，对源表的更新操作会写入到新建表中
5、将临时表和源表rename（需要元数据修改锁，需要短时间锁表）
6、删除源表和触发器，完成表结构的修改。

##=====================================================##
pt-osc工具限制
1、源表必须有主键或唯一索引，如果没有工具将停止工作
2、如果线上的复制环境过滤器操作过于复杂，工具将无法工作
3、如果开启复制延迟检查，但主从延迟时，工具将暂停数据拷贝工作
4、如果开启主服务器负载检查，但主服务器负载较高时，工具将暂停操作
5、当表使用外键时，如果未使用--alter-foreign-keys-method参数，工具将无法执行
6、只支持Innodb存储引擎表，且要求服务器上有该表1倍以上的空闲空间。

pt-osc之alter语句限制
1、不需要包含alter table关键字，可以包含多个修改操作，使用逗号分开，如"drop clolumn c1, add column c2 int"
2、不支持rename语句来对表进行重命名操作
3、不支持对索引进行重命名操作
4、如果删除外键，需要对外键名加下划线，如删除外键fk_uid, 修改语句为"DROP FOREIGN KEY _fk_uid"

pt-osc之命令模板
## --execute表示执行
## --dry-run表示只进行模拟测试
## 表名只能使用参数t来设置，没有长参数
pt-online-schema-change \
--host="127.0.0.1" \
--port=3358 \
--user="root" \
--password="root@root" \
--charset="utf8" \
--max-lag=10 \
--check-salve-lag='xxx.xxx.xxx.xxx' \
--recursion-method="hosts" \
--check-interval=2 \
--database="testdb1" \
 t="tb001" \
--alter="add column c4 int" \
--execute

例子：
pt-online-schema-change --user=root --password=123 --host=10.0.0.11 --alter "add column age int default 0" D=test,t=t1 --print --execute
```

## 2.3 pt-table-checksum



```bash
创建数据库
Create database pt CHARACTER SET utf8;
创建用户checksum并授权
GRANT ALL ON *.* TO 'checksum'@'10.0.0.%' IDENTIFIED BY 'checksum';
flush privileges;

--[no]check-replication-filters：是否检查复制的过滤器，默认是yes，建议启用不检查模式。
--databases | -d：指定需要被检查的数据库，多个库之间可以用逗号分隔。
--[no]check-binlog-format：是否检查binlog文件的格式，默认值yes。建议开启不检查。因为在默认的row格式下会出错。
--replicate`：把checksum的信息写入到指定表中。
--replicate-check-only：只显示不同步信息

pt-table-checksum --nocheck-replication-filters --no-check-binlog-format --replicate=pt.checksums --create-replicate-table --databases=test --tables=t1 h=10.0.0.11,u=checksum,p=checksum,P=3306

#!/bin/bash
date >> /root/db/checksum.log
pt-table-checksum --nocheck-binlog-format --nocheck-plan
--nocheck-replication-filters --replicate=pt.checksums --set-vars
innodb_lock_wait_timeout=120 --databases UAR_STATISTIC -u'checksum' -p'checksum'
-h'10.0.0.11' >> /root/db/checksum.log
date >> /root/db/checksum.log
```

## 2.4 pt-table-sync



```dart
主要参数介绍
--replicate ：指定通过pt-table-checksum得到的表.
--databases : 指定执行同步的数据库。
--tables ：指定执行同步的表，多个用逗号隔开。
--sync-to-master ：指定一个DSN，即从的IP，他会通过show processlist或show slave status 去自动的找主。
h= ：服务器地址，命令里有2个ip，第一次出现的是Master的地址，第2次是Slave的地址。
u= ：帐号。
p= ：密码。
--print ：打印，但不执行命令。
--execute ：执行命令。
pt-table-sync --replicate=pt.checksums h=10.0.0.11,u=root,p=123,P=3306 --print
```

## 2.5 mysql死锁监测



```bash
pt-deadlock-logger h='127.0.0.1' --user=root --password=123456
```

## 2.6 主键冲突检查



```bash
pt-duplicate-key-checker --database=world h='127.0.0.1' --user=root --password=123456
```

## pt-kill 语句



```bash
常用参数说明
--daemonize  放在后台以守护进程的形式运行；
--interval  多久运行一次，单位可以是s,m,h，d等默认是s –不加这个默认是5秒
--victims 默认是oldest,只杀最古老的查询。这是防止被查杀是不是真的长时间运行的查询，他们只是长期等待 这种种匹配按时间查询，杀死一个时间最高值。
--all 杀掉所有满足的线程
--kill-query      只杀掉连接执行的语句，但是线程不会被终止
--print               打印满足条件的语句
--busy-time 批次查询已运行的时间超过这个时间的线程；
--idle-time 杀掉sleep 空闲了多少时间的连接线程，必须在--match-command sleep时才有效—也就是匹配使用 -- –match-command 匹配相关的语句。
----ignore-command 忽略相关的匹配。 这两个搭配使用一定是ignore-commandd在前 match-command在后，
--match-db cdelzone 匹配哪个库
command有：Query、Sleep、Binlog Dump、Connect、Delayed insert、Execute、Fetch、Init DB、Kill、Prepare、Processlist、Quit、Reset stmt、Table Dump

例子：
---杀掉空闲链接sleep 5秒的 SQL 并把日志放到/home/pt-kill.log文件中
/usr/bin/pt-kill  --user=用户名 --password=密码 --match-command Sleep  --idle-time 5 --victim all --interval 5 --kill --daemonize -S /tmp/mysql.sock --pid=/tmp/ptkill.pid --print --log=/tmp/pt-kill.log &

---查询SELECT 超过1分钟路

/usr/bin/pt-kill --user=用户名 --password=密码 --busy-time 60  --match-info "SELECT|select" --victim all --interval 5 --kill --daemonize -S  -S /tmp/mysql.sock --pid=/tmp/ptkill.pid --print --log=/tmp/pt-kill.log &

--- Kill掉 select IFNULl.*语句开头的SQL

pt-kill --user=用户名 --password=密码 --victims all --busy-time=0 --match-info="select IFNULl.*" --interval 1 -S /tmp/mysqld.sock --kill --daemonize --pid=/tmp/ptkill.pid --print --log=/tmp/pt-kill.log &

----kill掉state Locked

/usr/bin/pt-kill --user=用户名 --password=密码  --victims all --match-state='Locked' --victim all --interval 5 --kill --daemonize -S /tmp/mysqld.sock --pid=/tmp/ptkill.pid --print --log=/tmp/pt-kill.log &

---kill掉 a库，web为10.0.0.11的链接

pt-kill  --user=用户名 --password=密码 --victims all  --match-db='a' --match-host='10.0.0.11' --kill --daemonize --interval 10  -S /tmp/mysqld.sock  --pid=/tmp/ptkill.pid --print-log=/tmp/pt-kill.log &

---指定哪个用户kill

pt-kill   --user=用户名 --password=密码 --victims all --match-user='root' --kill  --daemonize --interval 10 -S /home/zb/data/my6006/socket/mysqld.sock --pid=/tmp/ptkill.pid --print --log=/home/pt-kill.log &

---查询SELECT 超过1分钟路

pt-kill  --user=用户名 --password=密码 --busy-time 60 --match-info "SELECT|select" --victim all  --interval 5 --kill --daemonize -S /tmp/mysqld.sock --pid=/tmp/ptkill.pid --print --log=/tmp/pt-kill.log &


----kill掉 command query | Execute

pt-kill --user=用户名 --password=密码 --victims all  --match-command= "query|Execute" --interval 5 --kill --daemonize -S /tmp/mysqld.sock --pid=/tmp/ptkill.pid --print --log=/home/pt-kill.log &
```

## 其他



```swift
pt-find ---找出几天之前建立的表
pt-slave-restart -----主从报错，跳过报错
pt-summary ---整个系统的的概述
pt-mysql-summary ---MySQL的表述，包括配置文件的描述
pt-duplicate-key-checker ---检查数据库重复索引
```



