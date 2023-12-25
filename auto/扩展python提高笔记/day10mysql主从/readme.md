



# 安全

要一个普通权限的普通用户！！！

dba root all

zhangkai@'%'     select update... drop



日志

备份恢复

主从

主从架构进行架构的演变

-   基础架构
-   高可用架构





MySQL中的重要日志有哪些？

-   binlog
-   slowlog
-   errorlog
-   innodb存储引擎：
    -   redo log
    -   undo log
    -   https://www.cnblogs.com/Neeo/articles/13883976.html



# 环境准备

VMware 16 + centos7.9克隆环境

**单机多实例环境**

单机：单个服务器

多实例：实例，一个MySQL的进程。多实例通常根据不同的端口来划分。

MySQL版本选择：5.7

**mysql安装过程**

参考：https://www.cnblogs.com/Neeo/articles/13527500.html

1.创建安装目录：

```bash
[root@cs ~]# mkdir -p /opt/software
[root@cs ~]# cd /opt/software/
[root@cs software]# pwd
/opt/software

```



2 初始化：

```bash
mysqld --initialize-insecure  --user=mysql --basedir=/opt/software/mysql --datadir=/data/mysql/3306/data


mysqld --initialize-insecure  --user=mysql --datadir=/data/mysql/3307/data --basedir=/opt/software/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/mysql/3308/data --basedir=/opt/software/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/mysql/3309/data --basedir=/opt/software/mysql
mysqld --initialize-insecure  --user=mysql --datadir=/data/mysql/3310/data --basedir=/opt/software/mysql
```





















# errorlog

```bash

[mysqld]
log_error=/data/mysql_data/mysql.err
```



# slowlog

```bash
[mysqld]
# 开启慢日志功能
slow_query_log=1
# 慢日志保存位置
slow_query_log_file=/logs/mysql_logs/slowlogs/slow.log
# 记录慢日志的时长
long_query_time=2
# 查询没走索引也记录到慢日志中
log_queries_not_using_indexes=1


mysqldumpslow -s c -t 3 /logs/mysql_logs/slowlogs/slow.log


-- 返回慢日志中记录的最多的前3条语句
mysqldumpslow -s r -t 3 /logs/mysql_logs/slowlogs/slow.log

-- 返回慢日志中记录的按照时间排序的前3条语句
mysqldumpslow -s t -t 3 /logs/mysql_logs/slowlogs/slow.log

-- 返回慢日志中记录的按照时间排序的前10条中包含left join的查询语句
mysqldumpslow -s t -t 10 -g "left join" /logs/mysql_logs/slowlogs/slow.log
```

`mysqldumpslow`有三个重要的参数：

-   `-s`表示以何种方式进行排序，可选参数有：
    -   `c`表示按照查询次数进行排序，`ac`表示平均数。
    -   `t`表示按照查询时间进行排序，`at`表示平均数。
    -   `l`表示按照锁定时间进行排序，`al`表示平均数。
    -   `r`表示返回的记录数进行排序，`ar`表示平均数。
-   `-t`表示`top n`的意思，表示返回结果集中的前`n`条慢日志记录。
-   `-g`表示正则，可以跟正则表达式，大小写不敏感。

# binlog

binlog之记录数据变更的日志，不记录查询的日志。逻辑日志。

```bash

[mysqld]
server_id=6		
log_bin=/data/mysql_data/binlog/mysql-bin
binlog_format=row


gtid-mode=on		
enforce-gtid-consistency=true	-- 强制gtid的一致性
```





```

create table t1(id int);




begin;
insert into t1 value(1);
commit;



mysqlbinlog --start-position=219 --stop-position=732 /data/mysql/3306/logs/binlog/mysql-bin.000001 > /tmp/t1.sql





```



**根据position号进行二进制日志的数据恢复案例**

必须开启二进制日志功能。

1.  确认当前使用的二进制日文件
2.  使用show命令分析要截取的二进制日志范围
3.  截取日志
4.  根据截取出来的日志，进行数据恢复。
    1.  `set sql_log_bin=0;`
    2.  `sorces /tmp/t1.sql`
    3.  `set sql_log_bin=1;`









备份：

```bash
# 备份周期： 一周为一个备份周期
每天全备：每天的晚上23点进行当前数据库的全部数据备份


周日全备，周一到周六 选择增量备份

周日全备，周一到周六使用binlog日志

```

保留两个全备周期的binlog日志。

![image-20210523121255423](assets/image-20210523121255423.png)

























































