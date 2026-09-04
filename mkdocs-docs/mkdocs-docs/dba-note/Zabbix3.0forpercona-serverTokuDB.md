# 安装perconna源



```ruby
yum install http://www.percona.com/downloads/percona-release/redhat/0.1-6/percona-release-0.1-6.noarch.rpm
```

# 安装依赖



```csharp
yum install epel-release -y
yum install jemalloc -y
++++++++++++++++++++++++++++++++++++++

TokuDB storage engine requires libjemalloc library 3.3.0 or greater. If the version in the distribution repository is lower than that you can use one from Percona Software Repositories or download it from somewhere else.

If the libjemalloc wasn’t installed and enabled before it will be automatically installed when installing the TokuDB storage engine package by using the apt` or yum package manager, but Percona Server instance should be restarted for libjemalloc to be loaded. This way libjemalloc will be loaded with LD_PRELOAD. You can also enable libjemalloc by specifying malloc-lib variable in the [mysqld_safe] section of the my.cnf file:

[mysqld_safe]
malloc-lib= /path/to/jemalloc
+++++++++++++++++++++++++++++++++++++++
```

# 关闭大页内存



```kotlin
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

+++++++++++++++++++++++++++++++++++
TokuDB won’t be able to start if the transparent huge pages are enabled. Transparent huge pages is feature available in the newer kernel versions. You can check if the Transparent huge pages are enabled with:
$ cat /sys/kernel/mm/transparent_hugepage/enabled
 [always] madvise never
If transparent huge pages are enabled and you try to start the TokuDB engine you’ll get the following message in you error.log:
Transparent huge pages are enabled, according to /sys/kernel/mm/redhat_transparent_hugepage/enabled
Transparent huge pages are enabled, according to /sys/kernel/mm/transparent_hugepage/enabled
You can disable transparent huge pages permanently by passing transparent_hugepage=never to the kernel in your bootloader (NOTE: For this change to take an effect you’ll need to reboot your server).

You can disable the transparent huge pages by running the following command as root (NOTE: Setting this will last only until the server is rebooted):

echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
++++++++++++++++++++++++++++++++++++++++
```

# 安装percona数据库及tokudb插件



```css
yum install  Percona-Server-tokudb-57.x86_64
```

# 启动mysql



```undefined
systemctl start mysqld
```

# 登录并更改密码和过期策略



```bash
登录：
mysql -u root -p
,c!)fa/Cd9kD

更改密码及过期策略：
SET PASSWORD = PASSWORD('Qwe_1234');
ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
flush privileges;
```

# 配置root用户远程登录（只是为了测试，不代表生产操作）



```csharp
grant all privileges on *.* to root@"%" identified by "Qwe_1234";
```

# 测试本地登录与远程登录(我数据库IP为10.0.0.12)



```css
 mysql -uroot -pQwe_1234
 mysql -uroot -pQwe_1234 -h 10.0.0.12 -P3306
```

# 加载插件



```dart
ps_tokudb_admin --enable -uroot -pPassw0rd

INSTALL PLUGIN tokudb SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_file_map SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_fractal_tree_info SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_fractal_tree_block_map SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_trx SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_locks SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_lock_waits SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_background_job_status SONAME 'ha_tokudb.so';

show engines;
show plungins;
SELECT @@tokudb_version;
添加zabbix用户
grant all on zabbix.* to zabbix@'localhost' identified by 'Zabbix_pass123';
创建数据库：
create database zabbix charset utf8;
```

# zabbix安装



```ruby
[root@oldboy ~]# vim /etc/yum.repos.d/zabbix.repo
[root@oldboy ~]# cat /etc/yum.repos.d/zabbix.repo 
[zabbix]
name=Zabbix Official Repository - $basearch
baseurl=https://mirrors.tuna.tsinghua.edu.cn/zabbix/zabbix/3.0/rhel/7/$basearch/
enabled=1
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-ZABBIX

[zabbix-non-supported]
name=Zabbix Official Repository non-supported - $basearch 
baseurl=https://mirrors.tuna.tsinghua.edu.cn/zabbix/non-supported/rhel/7/$basearch/
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-ZABBIX
gpgcheck=0
[root@oldboy ~]# 

yum install -y zabbix-server-mysql zabbix-web-mysql zabbix-agent
```

# 修改配置文件



```csharp
[root@oldboy zabbix]# vim zabbix_server.conf 
DBPassword=Zabbix_pass123
vim /etc/httpd/conf.d/zabbix.conf 
php_value date.timezone Asia/Shanghai
```

# 导入zabbix数据库



```csharp
[root@oldboy conf.d]# rpm -ql zabbix-server-mysql
/etc/logrotate.d/zabbix-server
/etc/zabbix/zabbix_server.conf
/usr/lib/systemd/system/zabbix-server.service
/usr/lib/tmpfiles.d/zabbix-server.conf
/usr/lib/zabbix/alertscripts
/usr/lib/zabbix/externalscripts
/usr/sbin/zabbix_server_mysql
/usr/share/doc/zabbix-server-mysql-3.0.21
/usr/share/doc/zabbix-server-mysql-3.0.21/AUTHORS
/usr/share/doc/zabbix-server-mysql-3.0.21/COPYING
/usr/share/doc/zabbix-server-mysql-3.0.21/ChangeLog
/usr/share/doc/zabbix-server-mysql-3.0.21/NEWS
/usr/share/doc/zabbix-server-mysql-3.0.21/README
/usr/share/doc/zabbix-server-mysql-3.0.21/create.sql.gz
/usr/share/man/man8/zabbix_server.8.gz
/var/log/zabbix
/var/run/zabbix
[root@oldboy conf.d]# 
[root@oldboy conf.d]# cd /usr/share/doc/zabbix-server-mysql-3.0.21/
[root@oldboy zabbix-server-mysql-3.0.21]# gunzip create.sql.gz 
注意：如果使用tokudb，需要将sql脚本中的InnoDB替换为tokudb
mysql -uroot -pQwe_1234 
```

重启zabbix相关服务



```csharp
[root@oldboy ~]# systemctl restart zabbix-server
[root@oldboy ~]# systemctl restart zabbix-agent
[root@oldboy ~]# systemctl restart httpd
```

# web登录配置zabbix（略）

# 安装percona监控模板rpm包



```php
注意：修改采集脚本用户密码
/var/lib/zabbix/percona/scripts
 vim get_mysql_stats_wrapper.sh 
 RES=`HOME=~zabbix mysql -u root -pQwe_1234 
vim ss_get_mysql_stats.php
# 
$mysql_user = 'root';
$mysql_pass = 'Qwe_1234';
```

# 命令行测试监控项



```csharp
yum install zabbix-get.x86_64 -y
systemctl restart zabbix-agent.service 
cat /etc/zabbix/zabbix_agentd.d/userparameter_percona_mysql.conf 
zabbix_get -s 127.0.0.1 -k MySQL.Open-files
```



