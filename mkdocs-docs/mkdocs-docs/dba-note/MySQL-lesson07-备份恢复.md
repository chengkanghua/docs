# 1. 运维在数据库备份恢复方面的职责

## 1.1 设计备份策略



```undefined
全备  、增量、时间、自动
```

## 1.2 日常备份检查



```undefined
备份存在性
备份空间够用否
```

## 1.3 定期恢复演练(测试库)



```undefined
一季度 或者 半年
```

## 1.4 故障恢复



```undefined
通过现有备份,能够将数据库恢复到故障之前的时间点.       
```

## 1.5 迁移



```undefined
1. 停机时间
2. 回退方案
```

# 2. 备份类型

## 2.1 热备



```undefined
在数据库正常业务时,备份数据,并且能够一致性恢复（只能是innodb）
对业务影响非常小
```

## 2.2 温备



```undefined
锁表备份,只能查询不能修改（myisam）
影响到写入操作
```

## 2.3 冷备



```undefined
关闭数据库业务,数据库没有任何变更的情况下,进行备份数据.
业务停止
```

# 3. 备份方式及工具介绍

## 3.1 逻辑备份工具



```undefined
基于SQL语句进行备份
mysqldump       *****
mysqlbinlog     *****
```

## 3.2 物理备份工具



```undefined
基于磁盘数据文件备份
xtrabackup(XBK) ：percona 第三方   *****
MySQL Enterprise Backup（MEB）
```

# 4.  逻辑备份和物理备份的比较

## 4.1 mysqldump (MDP)



```undefined
优点：
1.不需要下载安装
2.备份出来的是SQL，文本格式，可读性高,便于备份处理
3.压缩比较高，节省备份的磁盘空间

缺点：
4.依赖于数据库引擎，需要从磁盘把数据读出
然后转换成SQL进行转储，比较耗费资源，数据量大的话效率较低
建议：
100G以内的数据量级，可以使用mysqldump
超过TB以上，我们也可能选择的是mysqldump，配合分布式的系统
1EB  =1024 PB =1000000 TB
```

## 4.2 xtrabackup(XBK)



```undefined
优点：
1.类似于直接cp数据文件，不需要管逻辑结构，相对来说性能较高
缺点：
2.可读性差
3.压缩比低，需要更多磁盘空间
建议：
>100G<TB
```

# 5.备份策略



```undefined
备份方式：
全备:全库备份，备份所有数据
增量:备份变化的数据
逻辑备份=mysqldump+mysqlbinlog
物理备份=xtrabackup_full+xtrabackup_incr+binlog或者xtrabackup_full+binlog
备份周期:
根据数据量设计备份周期
比如：周日全备，周1-周6增量
```

# 6.备份工具使用-mysqldump

## 6.1 mysqldump (逻辑备份的客户端工具)

### 6.1.1 客户端通用参数



```undefined
-u  -p   -S   -h  -P    
本地备份:
mysqldump -uroot -p  -S /tmp/mysql.sock
远程备份:
mysqldump -uroot -p  -h 10.0.0.51 -P3306
```

### 6.1.2 备份专用基本参数

#### -A   全备参数



```swift
例子1:
[root@db01 ~]# mkdir -p /data/backup
mysqldump -uroot -p -A >/data/backup/full.sql
Enter password: 

mysqldump: [Warning] Using a password on the command line interface can be insecure.
Warning: A partial dump from a server that has GTIDs will by default include the GTIDs of all transactions, even those that changed suppressed parts of the database. If you don't want to restore GTIDs, pass --set-gtid-purged=OFF. To make a complete dump, pass --all-databases --triggers --routines --events. 

# 补充:
# 1.常规备份是要加 --set-gtid-purged=OFF,解决备份时的警告
# [root@db01 ~]# mysqldump -uroot -p123 -A  --set-gtid-purged=OFF  >/backup/full.sql
# 2.构建主从时,做的备份,不需要加这个参数
# [root@db01 ~]# mysqldump -uroot -p123 -A    --set-gtid-purged=ON >/backup/full.sql
```

#### -B db1  db2  db3  备份多个单库



```kotlin
说明：生产中需要备份，生产相关的库和MySQL库
例子2 :
mysqldump -B mysql gtid --set-gtid-purged=OFF >/data/backup/b.sql 
```

#### 备份单个或多个表



```bash
例子3 world数据库下的city,country表
mysqldump -uroot -p world city country >/backup/bak1.sql
以上备份恢复时:必须库事先存在,并且ues才能source恢复
```

### 6.1.3 高级参数应用

#### 特殊参数1使用（必须要加）



```csharp
-R            备份存储过程及函数
--triggers  备份触发器
-E             备份事件

例子4:
[root@db01 backup]# mysqldump -uroot -p -A -R -E --triggers >/data/backup/full.sql
(5) 特殊参数2使用
```

#### -F  在备份开始时,刷新一个新binlog日志



```jsx
例子5:
mysqldump -uroot -p  -A  -R --triggers -F >/bak/full.sql
```

#### --master-data=2



```kotlin
以注释的形式,保存备份开始时间点的binlog的状态信息

mysqldump -uroot -p  -A  -R --triggers --master-data=2   >/back/world.sql
[root@db01 ~]# grep 'CHANGE' /backup/world.sql 
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000035', MASTER_LOG_POS=194;

功能：
（1）在备份时，会自动记录，二进制日志文件名和位置号
0 默认值
1  以change master to命令形式，可以用作主从复制
2  以注释的形式记录，备份时刻的文件名+postion号
（2） 自动锁表
（3）如果配合--single-transaction，只对非InnoDB表进行锁表备份，InnoDB表进行“热“”备，实际上是实现快照备份。
```

#### --single-transaction



```kotlin
innodb 存储引擎开启热备(快照备份)功能       
master-data可以自动加锁
（1）在不加--single-transaction ，启动所有表的温备份，所有表都锁定
（1）加上--single-transaction ,对innodb进行快照备份,对非innodb表可以实现自动锁表功能
例子6: 备份必加参数
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
```

#### --set-gtid-purged=auto



```kotlin
auto , on
off 
使用场景:
1. --set-gtid-purged=OFF,可以使用在日常备份参数中.
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
2. auto , on:在构建主从复制环境时需要的参数配置
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=ON >/data/backup/full.sql
```

#### --max-allowed-packet=#



```csharp
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF --max-allowed-packet=256M >/data/backup/full.sql

 --max-allowed-packet=# 
The maximum packet length to send to or receive from server.
```

#### 6.2 小练习：

6.2.1. 实现所有表的单独备份



```csharp
提示：
information_schema.tables
mysqldump -uroot -p123 world city >/backup/world_city.sql

select concat("mysqldump -uroot -p123 ",table_schema," ",table_name," --master-data=2 --single-transaction --set-gtid-purged=0  -R -E --triggers>/backup/",table_schema,"_",table_name,".sql") from information_schema.tables where table_schema not in ('sys','information_schema','performance_schema');
```

#### 6.2.2.模拟故障案例并恢复



```csharp
（1）每天全备
（2）binlog日志是完整
（3）模拟白天的数据变化
（4）模拟下午两点误删除数据库

需求： 利用全备+binlog回复数据库误删除之前。
故障模拟及恢复：
1. 模拟周一23:00的全备
mysqldump -uroot -p -A -R -E --triggers --master-data=2  --single-transaction --set-gtid-purged=OFF >/data/backup/full.sql
2. 模拟白天的数据变化
Master [(none)]>create database day1 charset utf8;
Master [(none)]>use day1
Master [day1]>create table t1(id int);
Master [day1]>insert into t1 values(1),(2),(3);
Master [day1]>commit;
Master [world]>update city set countrycode='CHN';
Master [world]>commit;
模拟磁盘损坏：
[root@db01 data]# \rm -rf /data/mysql/data/*
3. 恢复故障
[root@db01 data]# pkill mysqld
[root@db01 data]# \rm -rf /data/mysql/data/*
4. 恢复思路
1.检查备份可用性
2.从备份中获取二进制日志位置
3.根据日志位置截取需要的二进制日志
4.初始化数据库,并启动
5.恢复全备
6.恢复二进制日志
```

## 6.3. 压缩备份并添加时间戳



```jsx
例子：
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz
mysqldump -uroot -p123 -A  -R  --triggers --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F-%T).sql.gz

mysqldump备份的恢复方式（在生产中恢复要谨慎，恢复会删除重复的表）
set sql_log_bin=0;
source /backup/full_2018-06-28.sql

注意：
1、mysqldump在备份和恢复时都需要mysql实例启动为前提。
2、一般数据量级100G以内，大约15-45分钟可以恢复，数据量级很大很大的时候（PB、EB）
3、mysqldump是覆盖形式恢复的方法。

一般我们认为，在同数据量级，物理备份要比逻辑备份速度快.
逻辑备份的优势:
1、可读性强
2、压缩比很高
```

# 7、企业故障恢复案例

## 7.1 背景环境：



```css
正在运行的网站系统，mysql-5.7.20 数据库，数据量50G，日业务增量1-5M。
```

## 7.2 备份策略：



```css
每天23:00点，计划任务调用mysqldump执行全备脚本
```

## 7.3 故障时间点：



```undefined
年底故障演练:模拟周三上午10点误删除数据库，并进行恢复.
```

## 7.4 思路：



```css
1、停业务，避免数据的二次伤害
2、找一个临时库，恢复周三23：00全备
3、截取周二23：00  --- 周三10点误删除之间的binlog，恢复到临时库
4、测试可用性和完整性
5、 
    5.1 方法一：直接使用临时库顶替原生产库，前端应用割接到新库
    5.2 方法二：将误删除的表导出，导入到原生产库
6、开启业务
处理结果：经过20分钟的处理，最终业务恢复正常
```

## 7.5 故障模拟演练

### 7.5.1 准备数据



```csharp
create database backup;
use backup
create table t1 (id int);
insert into t1 values(1),(2),(3);
commit;
rm -rf /backup/*
```

### 7.5.2 周二 23：00全备



```tsx
mysqldump -uroot -p123 -A  -R  --triggers --set-gtid-purged=OFF --master-data=2  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz
```

### 7.5.3 模拟周二 23：00到周三 10点之间数据变化



```csharp
use backup
insert into t1 values(11),(22),(33);
commit;
create table t2 (id int);
insert into t2 values(11),(22),(33);
```

### 7.5.4 模拟故障,删除表(只是模拟，不代表生产操作)



```rust
drop database backup;
```

## 7.6 恢复过程

### 7.6.1 准备临时数据库（多实例3307）



```undefined
systemctl start mysqld3307
```

### 7.6.2 准备备份



```ruby
（1）准备全备：
cd /backup
gunzip full_2018-10-17.sql.gz 
（2）截取二进制日志
-- CHANGE MASTER TO MASTER_LOG_FILE='mysql-bin.000036', MASTER_LOG_POS=793;
mysqlbinlog --skip-gtids --include-gtids='3ca79ab5-3e4d-11e9-a709-000c293b577e:6-7' /data/binlog/mysql-bin.000036 >/backup/bin.sql
```

### 7.6.3 恢复备份到临时库



```bash
mysql -S /data/3307/mysql.sock
set sql_log_bin=0;
source /backup/full_2018-10-17.sql
source /backup/bin.sql
```

### 7.6.4 将故障表导出并恢复到生产



```bash
mysqldump   -S /data/3307/mysql.sock backup t1 >/backup/t1.sql
mysql -uroot -p123 
set sql_log_bin=0
use backup 
source /backup/t1.sql;
```

# 8. 课下作业：



```undefined
练习：
1、创建一个数据库 oldboy
2、在oldboy下创建一张表t1
3、插入5行任意数据
4、全备
5、插入两行数据，任意修改3行数据，删除1行数据
6、删除所有数据
7、再t1中又插入5行新数据，修改3行数据
需求，跳过第六步恢复表数据
写备份脚本和策略
```

# 9. 备份时优化参数:



```tsx
(1) max_allowed_packet   最大的数据包大小

mysqldump -uroot -p123 -A  -R  --triggers --set-gtid-purged=OFF --master-data=2 max_allowed_packet=128M  --single-transaction|gzip > /backup/full_$(date +%F).sql.gz

(2) 增加key_buffer_size    (临时表有关)
(3) 分库分表并发备份       (作业)
(4) 架构分离,分别备份      (架构拆分,分布式备份)
```

# 10. MySQL物理备份工具-xtrabackup(XBK、Xbackup)

## 10.1安装

### 10.1.1 安装依赖包：



```cpp
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum -y install perl perl-devel libaio libaio-devel perl-Time-HiRes perl-DBD-MySQL libev
```

### 10.1.2 下载软件并安装



```ruby
wget https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.12/binary/redhat/7/x86_64/percona-xtrabackup-24-2.4.12-1.el7.x86_64.rpm

https://www.percona.com/downloads/XtraBackup/Percona-XtraBackup-2.4.4/binary/redhat/6/x86_64/percona-xtrabackup-24-2.4.4-1.el6.x86_64.rpm

yum -y install percona-xtrabackup-24-2.4.4-1.el7.x86_64.rpm
```

## 10.2、备份命令介绍:



```undefined
xtrabackup
innobackupex    ******
```

## 10.3 备份方式——物理备份



```ruby
（1）对于非Innodb表（比如 myisam）是，锁表cp数据文件，属于一种温备份。
（2）对于Innodb的表（支持事务的），不锁表，拷贝数据页，最终以数据文件的方式保存下来，把一部分redo和undo一并备走，属于热备方式。
```

## 面试题： xbk 在innodb表备份恢复的流程



```ruby
  0、xbk备份执行的瞬间,立即触发ckpt,已提交的数据脏页,从内存刷写到磁盘,并记录此时的LSN号
  1、备份时，拷贝磁盘数据页，并且记录备份过程中产生的redo和undo一起拷贝走,也就是checkpoint LSN之后的日志
  2、在恢复之前，模拟Innodb“自动故障恢复”的过程，将redo（前滚）与undo（回滚）进行应用
  3、恢复过程是cp 备份到原来数据目录下
```

## 10.4、innobackupex使用

### 10.4.1 全备



```csharp
[root@db01 backup]# innobackupex --user=root --password=123  /data/backup
```

### 自主定制备份路径名



```csharp
[root@db01 backup]# innobackupex --user=root --password=123 --no-timestamp /data/backup/full
```

### 备份集中多出来的文件：



```ruby
-rw-r----- 1 root root       24 Jun 29 09:59 xtrabackup_binlog_info
-rw-r----- 1 root root      119 Jun 29 09:59 xtrabackup_checkpoints
-rw-r----- 1 root root      489 Jun 29 09:59 xtrabackup_info
-rw-r----- 1 root root     2560 Jun 29 09:59 xtrabackup_logfile

xtrabackup_binlog_info ：（备份时刻的binlog位置）
[root@db01 full]# cat xtrabackup_binlog_info 
mysql-bin.000003    536749
79de40d3-5ff3-11e9-804a-000c2928f5dd:1-7
记录的是备份时刻，binlog的文件名字和当时的结束的position，可以用来作为截取binlog时的起点。

xtrabackup_checkpoints ：
backup_type = full-backuped
from_lsn = 0            上次所到达的LSN号(对于全备就是从0开始,对于增量有别的显示方法)
to_lsn = 160683027      备份开始时间(ckpt)点数据页的LSN    
last_lsn = 160683036    备份结束后，redo日志最终的LSN
compact = 0
recover_binlog_info = 0
（1）备份时刻，立即将已经commit过的，内存中的数据页刷新到磁盘(CKPT).开始备份数据，数据文件的LSN会停留在to_lsn位置。
（2）备份时刻有可能会有其他的数据写入，已备走的数据文件就不会再发生变化了。
（3）在备份过程中，备份软件会一直监控着redo的undo，如果一旦有变化会将日志也一并备走，并记录LSN到last_lsn。
从to_lsn  ----》last_lsn 就是，备份过程中产生的数据变化.
```

### 10.4.2 全备的恢复

#### 准备备份（Prepared）



```ruby
将redo进行重做，已提交的写到数据文件，未提交的使用undo回滚掉。模拟了CSR的过程
[root@db01 ~]# innobackupex --apply-log  /backup/full
```

#### 恢复备份



```undefined
前提：
1、被恢复的目录是空
2、被恢复的数据库的实例是关闭
systemctl stop mysqld
```

创建新目录



```csharp
[root@db01 backup]# mkdir /data/mysql1
```

#### 数据授权



```kotlin
chown -R mysql.mysql /data/mysql1
```

#### 恢复备份



```ruby
[root@db01 full]# cp -a /backup/full/* /data/mysql1/
```

#### 启动数据库



```kotlin
vim /etc/my.cnf
datadir=/data/mysql1
[root@db01 mysql1]# chown -R mysql.mysql /data/mysql1
systemctl start mysqld
```

## 10.4.3 innobackupex 增量备份(incremental)



```undefined
（1）增量备份的方式，是基于上一次备份进行增量。
（2）增量备份无法单独恢复。必须基于全备进行恢复。
（3）所有增量必须要按顺序合并到全备中。
```

#### 增量备份命令



```csharp
（1）删掉原来备份
略.
（2）全备（周日）
[root@db01 backup]# innobackupex --user=root --password --no-timestamp /backup/full >&/tmp/xbk_full.log
（3）模拟周一数据变化
db01 [(none)]>create database cs charset utf8;
db01 [(none)]>use cs
db01 [cs]>create table t1 (id int);
db01 [cs]>insert into t1 values(1),(2),(3);
db01 [cs]>commit;

（4）第一次增量备份（周一）
innobackupex --user=root --password=123 --no-timestamp --incremental --incremental-basedir=/backup/full  /backup/inc1 &>/tmp/inc1.log
（5）模拟周二数据
db01 [cs]>create table t2 (id int);
db01 [cs]>insert into t2 values(1),(2),(3);
db01 [cs]>commit;
（6）周二增量
 innobackupex --user=root --password=123 --no-timestamp --incremental --incremental-basedir=/backup/inc1  /backup/inc2  &>/tmp/inc2.log
（7）模拟周三数据变化
db01 [cs]>create table t3 (id int);
db01 [cs]>insert into t3 values(1),(2),(3);
db01 [cs]>commit;
db01 [cs]>drop database cs;
```

#### 恢复到周三误drop之前的数据状态



```undefined
恢复思路：
1.  挂出维护页，停止当天的自动备份脚本
2.  检查备份：周日full+周一inc1+周二inc2，周三的完整二进制日志
3. 进行备份整理（细节），截取关键的二进制日志（从备份——误删除之前）
4. 测试库进行备份恢复及日志恢复
5. 应用进行测试无误，开启业务
6. 此次工作的总结
```

#### 恢复过程



```kotlin
1. 检查备份
1afe8136-601d-11e9-9022-000c2928f5dd:7-9
2. 备份整理（apply-log）+合并备份（full+inc1+inc2）
(1) 全备的整理
[root@db01 one]# innobackupex --apply-log --redo-only /data/backup/full
(2) 合并inc1到full中
[root@db01 one]# innobackupex --apply-log --redo-only --incremental-dir=/data/backup/inc1 /data/backup/full
(3) 合并inc2到full中
[root@db01 one]# innobackupex --apply-log  --incremental-dir=/data/backup/inc2 /data/backup/full
(4) 最后一次整理全备
[root@db01 backup]#  innobackupex --apply-log  /data/backup/full
3. 截取周二 23:00 到drop 之前的 binlog 
[root@db01 inc2]# mysqlbinlog --skip-gtids --include-gtids='1afe8136-601d-11e9-9022-000c2928f5dd:7-9' /data/binlog/mysql-bin.000009 >/data/backup/binlog.sql
4. 进行恢复
[root@db01 backup]# mkdir /data/mysql/data2 -p
[root@db01 full]# cp -a * /data/mysql/data2
[root@db01 backup]# chown -R mysql.  /data/*
[root@db01 backup]# systemctl stop mysqld
vim /etc/my.cnf
datadir=/data/mysql/data2
systemctl start mysqld
Master [(none)]>set sql_log_bin=0;
Master [(none)]>source /data/backup/binlog.sql
```

### 作业1



```css
 Xtrabackup企业级增量恢复实战
背景：
某大型网站，mysql数据库，数据量500G，每日更新量20M-30M
备份策略：
xtrabackup，每周日0:00进行全备，周一到周六00:00进行增量备份。
故障场景：
周三下午2点出现数据库意外删除表操作。
如何恢复？
```

### 作业2



```undefined
练习：mysqldump备份恢复例子
1、创建一个数据库 oldboy
2、在oldboy下创建一张表t1
3、插入5行任意数据
4、全备
5、插入两行数据，任意修改3行数据，删除1行数据
6、删除所有数据
7、再t1中又插入5行新数据，修改3行数据
需求，跳过第六步恢复表数据
```

### 作业3



```undefined
分别写备份脚本和策略
```

### 作业4：备份集中单独恢复表



```kotlin
思考:在之前的项目案例中,如果误删除的表只有10M,而备份有500G,该如何快速恢复误删除表?
提示：
drop table city;
create table city like city_bak;
alter table city discard tablespace;
cp /backup/full/world/city.ibd  /application/mysql/data/world/
chown -R mysql.mysql  /application/mysql/data/world/city.ibd 
alter table city import  tablespace;
```

### 作业5： 从mysqldump 全备中获取库和表的备份



```kotlin
1、获得表结构
# sed -e'/./{H;$!d;}' -e 'x;/CREATE TABLE `city`/!d;q'  full.sql>createtable.sql

2、获得INSERT INTO 语句，用于数据的恢复

# grep -i 'INSERT INTO `city`'  full.sqll >data.sql &

3.获取单库的备份

# sed -n '/^-- Current Database: `world`/,/^-- Current Database: `/p' all.sql >world.sql
```



