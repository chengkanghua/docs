# 5.6.44 二进制包安装部署

## 解压到以下目录



```ruby
[root@oldboy ~]# ll /usr/local/mysql56/
drwxr-xr-x.  2 root root   4096 Jun  3 11:20 bin
-rw-r--r--.  1 7161 31415 17987 Mar 15 15:38 COPYING
drwxr-xr-x.  3 root root     18 Jun  3 11:19 data
drwxr-xr-x.  2 root root     55 Jun  3 11:19 docs
drwxr-xr-x.  3 root root   4096 Jun  3 11:19 include
drwxr-xr-x.  3 root root   4096 Jun  3 11:19 lib
drwxr-xr-x.  4 root root     30 Jun  3 11:19 man
drwxr-xr-x. 10 root root   4096 Jun  3 11:19 mysql-test
-rw-r--r--.  1 7161 31415  2496 Mar 15 15:38 README
drwxr-xr-x.  2 root root     30 Jun  3 11:19 scripts
drwxr-xr-x. 28 root root   4096 Jun  3 11:20 share
drwxr-xr-x.  4 root root   4096 Jun  3 11:19 sql-bench
drwxr-xr-x.  2 root root    136 Jun  3 11:19 support-files
[root@oldboy ~]# 
```

## 修改配置文件



```tsx
[root@oldboy ~]# cat >/data/mysql56/my.cnf  <<EOF
[mysqld]
basedir=/usr/local/mysql56
datadir=/data/mysql56/data
socket=/tmp/mysql56.sock
user=mysql
log_error=/tmp/mysql56.log
skip_name_resolve
log_bin=/data/mysql56/mysql-bin
port=5606
server_id=5606
EOF
```

## 准备启动脚本



```ruby
cat >/etc/systemd/system/mysqld56.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql56/bin/mysqld --defaults-file=/data/mysql56/my.cnf
LimitNOFILE = 5000
EOF
```

## 初始化数据



```csharp
[root@oldboy ~]# mv /etc/my.cnf  /etc/my.cnf.aa
[root@oldboy ~]# /usr/local/mysql56/scripts/mysql_install_db --user=mysql --datadir=/data/mysql56/data --basedir=/usr/local/mysql56 
```

## 启动数据库



```csharp
chown -R mysql.mysql /data
[root@oldboy tmp]# systemctl start mysqld56
[root@oldboy tmp]# /usr/local/mysql56/bin/mysql -S /tmp/mysql56.sock 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 1
Server version: 5.6.44-log MySQL Community Server (GPL)
```

# 5.7.26 二进制包安装部署

## 解压到以下目录



```ruby
[root@oldboy ~]# ll /usr/local/mysql57/
total 36
drwxr-xr-x.  2 root root   4096 Jun  3 11:22 bin
-rw-r--r--.  1 7161 31415 17987 Apr 13 21:32 COPYING
drwxr-xr-x.  2 root root     55 Jun  3 11:22 docs
drwxr-xr-x.  3 root root   4096 Jun  3 11:21 include
drwxr-xr-x.  5 root root    230 Jun  3 11:22 lib
drwxr-xr-x.  4 root root     30 Jun  3 11:22 man
-rw-r--r--.  1 7161 31415  2478 Apr 13 21:32 README
drwxr-xr-x. 28 root root   4096 Jun  3 11:22 share
drwxr-xr-x.  2 root root     90 Jun  3 11:22 support-files
```

## 修改配置文件



```tsx
[root@oldboy ~]# cat > /data/mysql57/my.cnf <<EOF
[mysqld]
basedir=/usr/local/mysql57
datadir=/data/mysql57/data
socket=/tmp/mysql57.sock
user=mysql
log_error=/tmp/mysql57.log
skip_name_resolve
log_bin=/data/mysql57/mysql-bin
port=5706
server_id=5706
EOF
```

## 准备启动脚本



```ruby
cat >/etc/systemd/system/mysqld57.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql57/bin/mysqld --defaults-file=/data/mysql57/my.cnf
LimitNOFILE = 5000
EOF
```

## 初始化数据



```kotlin
[root@oldboy ~]# /usr/local/mysql57/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql57/ --datadir=/data/mysql57/data
```

## 启动数据库



```csharp
chown -R mysql.mysql /data
[root@oldboy tmp]# systemctl start mysqld57
[root@oldboy tmp]# /usr/local/mysql57/bin/mysql -S /tmp/mysql57.sock 
```

# 8.0.16 二进制包安装部署

## 解压到以下目录



```csharp
[root@oldboy ~]# ll /usr/local/mysql80/
drwxr-xr-x.  2 7161 31415   4096 Apr 14 07:06 bin
drwxr-xr-x.  2 7161 31415     86 Apr 14 07:06 docs
drwxr-xr-x.  3 7161 31415    261 Apr 14 07:06 include
drwxr-xr-x.  6 7161 31415   4096 Apr 14 07:06 lib
-rw-r--r--.  1 7161 31415 335809 Apr 13 19:46 LICENSE
-rw-r--r--.  1 7161 31415 101807 Apr 13 19:46 LICENSE.router
drwxr-xr-x.  4 7161 31415     30 Apr 14 07:06 man
-rw-r--r--.  1 7161 31415    687 Apr 13 19:46 README
-rw-r--r--.  1 7161 31415    700 Apr 13 19:46 README.router
drwxrwxr-x.  2 7161 31415      6 Apr 14 07:06 run
drwxr-xr-x. 28 7161 31415   4096 Apr 14 07:06 share
drwxr-xr-x.  2 7161 31415     77 Apr 14 07:06 support-files
drwxr-xr-x.  3 7161 31415     17 Apr 14 07:06 var
[root@oldboy ~]# 
```

## 修改配置文件



```tsx
[root@oldboy ~]# cat > /data/mysql80/my.cnf <<EOF
[mysqld]
basedir=/usr/local/mysql80
datadir=/data/mysql80/data
socket=/tmp/mysql80.sock
user=mysql
log_error=/tmp/mysql80.log
skip_name_resolve
log_bin=/data/mysql80/mysql-bin
port=8006
server_id=8006
EOF
```

## 准备启动脚本



```ruby
cat >/etc/systemd/system/mysqld80.service<<EOF
[Unit]
Description=MySQL Server
Documentation=man:mysqld(8)
Documentation=http://dev.mysql.com/doc/refman/en/using-systemd.html
After=network.target
After=syslog.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
Group=mysql
ExecStart=/usr/local/mysql80/bin/mysqld --defaults-file=/data/mysql80/my.cnf
LimitNOFILE = 5000
EOF
```

## 初始化数据



```kotlin
[root@oldboy ~]# /usr/local/mysql80/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql80  --datadir=/data/mysql80/data
```

## 启动数据库



```csharp
chown -R mysql.mysql /data
[root@oldboy tmp]# systemctl start mysqld80
[root@oldboy tmp]# /usr/local/mysql80/bin/mysql -S /tmp/mysql80.sock 
```



