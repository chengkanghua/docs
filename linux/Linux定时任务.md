
你每天是怎么起床的？有的人有女朋友，，或是男朋友，，而我是被穷醒的.   
**什么是计划任务：** 后台运行，到了预定的时间就会自动执行的任务，前提是：事先手动将计划任务设定好。

- 周期性任务执行
- 清空/tmp目录下的内容
- mysql数据库备份
- redis数据备份

这就用到了crond服务。
**检查crond服务相关的软件包**

```
[root@MiWiFi-R3-srv ~]# rpm -qa |grep cron
cronie-anacron-1.4.11-14.el7.x86_64        
crontabs-1.11-6.20121102git.el7.noarch     
cronie-1.4.11-14.el7.x86_64    #定时任务主程序包，提供crond守护进程等工具
rpm -ivh  安装rpm软件
rpm -qa 查看软件是否安装
rpm -ql 查看软件详细信息s
rpm -qf 查看命令属于的安装包
rpm -e  卸载软件
```
**检查crond服务是否运行**

```
systemctl status crond.service  #centos7
service crond status    #centos6
```
## crond定时任务服务应用

```
cron 定时任务的名字
crond 定时任务进程名
crontab 管理定时任务命令
```

Cron是Linux系统中以后台进程模式周期性执行命令或指定程序任务的服务软件名。
Linux系统启动后，cron软件便会启动，对应的进程名字叫做crond，默认是定期（每分钟检查一次)检查系统中是否有需要执行的任务计划，如果有，则按计划进行，好比我们平时用的闹钟。

- crond定时任务默认最快的频率是每分钟执行
- 若是需要以秒为单位的计划任务，则编写shell脚本更格式，crond不适用了

```
#秒级shell脚本
[root@pylinux tmp]# cat test_cron.sh
#!/bin/bash
while true
do
echo "哥哥还是强呀"
sleep 1
done
[root@pylinux tmp]# sh test_cron.sh #每秒打印一次
```

### 为什么需要crond定时任务

- 夜间数据库定时备份
- 夜间网站数据（用户上传、文件、图片、程序）备份
- 备份等待时间过长
- 任务重复性高

利用Linux的定时任务cron工具可以解决重复性、周期性的、自动备份等运维工作
### linux下定时任务软件

- `at`定时任务工具，依赖于`atd`服务，适用于执行一次就结束的调度任务

例如突发任务，某天夜里3点需要临时性备份数据，可以使用at软件

```
语法
HH:MM
YYYY-mm-dd
noon    正午中午12点
midnight    午夜晚12点
teatime    下午茶时间，下午四点
tomorrow    明天
now+1min  #一分钟之后
now+1minutes/hours/days/weeks
```

```
一分钟之后运行ls /opt
at now+1min
[root@chaogelinux ~]# at  now+1min        #ctrl+d提交任务
at> ls /data
at> <EOT>
job 2 at Thu Nov 21 10:38:00 2019
运行之后，通过邮件检查
[root@chaogelinux ~]#
您在 /var/spool/mail/root 中有新邮件
[root@chaogelinux ~]# mail  #通过mail，检查at的任务结果
#检查定时任务
at -l  #列出等待中的作业
#通过文件交互式读取任务，不用交互式输入
[root@chaogelinux data]# cat mytasks.at
echo "chaoge 666"
[root@chaogelinux data]# at -f ./mytasks.at now+3min
job 5 at Thu Nov 21 10:51:00 2019
#删除任务
at -d 6
atrm 6  #效果一样
```

- `cron`定时任务依赖于`crond`服务，启动`crond服务后`通过linux命令`crontab`可以配置周期性定时任务，是Linux运维最常用的工具
### 定时任务与邮件服务
任务计划触发执行后，会通过邮件发送给用户，（并非互联网上的邮件，而是系统内部的邮件服务）

```
1.检查服务器端口，25号邮件端口是否打开,centos5是sendmail，centos6、7是postfix服务
ss -tnl |grep 25
netstat -tnl |grep 25
2.发现未启动25端口的话，则需要启动postfix服务，用于发送邮件
首先更改postfix配置文件
    vim /etc/postfix/main.cf
修改如下参数
  inet_interfaces = all
  inet_protocols = all
3.启动postfix服务
systemctl start postfix
```
**本地电子邮件服务**
[网易邮箱邮件协议解释](http://help.163.com/09/1223/14/5R7P6CJ600753VB8.html)

```
smtp：simple mail transmission protocol
    pop3：Post Office Procotol
    imap4：Internet Mail Access Procotol
```

**mailx命令**

了解三个概念：
MTA：`Mail Transport Agent`，邮件传送代理，也就是`postfix`服务
MUA：`Mail User Agent`，收发邮件的客户端，可以是`foxmail`，也可以是`其他客户端`
Centos7通过命令`mailx`发送邮件，通过`mail`命令是收邮件

```
[root@chaogelinux ~]# mailx -s "hello gege" gege    # 给gege系统用户发送邮件，-s 添加主题
hi chaoge,how are you?    #文章内容
.        #输入点，退出邮件
EOT    #结束符号，end out
```
**mail命令**

按下q退出

```
& q
Held 1 message in /var/spool/mail/chaoge
You have mail in /var/spool/mail/chaoge
```
**非交互式发邮件**
用gege用户给root回一封邮件，从文本中读取数据

```
[gege@gegelinux ~]$ echo "I fine,thank you root,and you?" > fine.txt
[gege@gegelinux ~]$
[gege@gegelinux ~]$ mail -s "hello root" root < fine.txt
[gege@gegelinux ~]$ logout
您在 /var/spool/mail/root 中有邮件
[root@chaogelinux ~]# mail
```
### 定时任务cron实践
向crond进程提交任务的方式与at不同，crond需要读取配置文件，且有固定的文件格式，通过crontab命令管理文件
**cron任务分为两类**

- **系统定时任务**

crond服务除了会在工作时查看`/var/spool/cron`文件夹下的定时任务文件以外，还会查看`/etc/cron.d`目录以及`/etc/anacrontab`下面的文件内容，里面存放`每天、每周、每月需要执行的系统任务`

```
[root@pylinux ~]# ls -l /etc/|grep cron*
-rw-------.  1 root  root      541 4月  11 2018 anacrontab
drwxr-xr-x.  2 root  root     4096 8月  30 11:08 cron.d        #系统定时任务
drwxr-xr-x.  2 root  root     4096 8月   8 2018 cron.daily    #每天的任务
-rw-------.  1 root  root        0 4月  11 2018 cron.deny
drwxr-xr-x.  2 root  root     4096 8月   8 2018 cron.hourly    #每小时执行的任务
drwxr-xr-x.  2 root  root     4096 6月  10 2014 cron.monthly    #每月的定时任务
-rw-r--r--   1 root  root      507 5月  10 2019 crontab
drwxr-xr-x.  2 root  root     4096 6月  10 2014 cron.weekly    #每周的定时任务
```
系统定时任务配置文件`/etc/crontab`

```
[root@chaogelinux data]# cat /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin        #路径信息很少，因此定时任务用绝对路径
MAILTO=root            #执行结果发送邮件给用户
# For details see man 4 crontabs
# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
#每一行，就是一条周期性任务
user-name 是以某一个用户身份运行任务
command to be executed  任务是什么
```

- **用户定时任务计划**

当系统管理员（root）或是普通用户(chaoge)创建了需要定期执行的任务，可以使用`crontab`命令配置，
crond服务在启动时，会每分钟查看`/var/spool/cron`路径下以`系统用户名`命名的`定时任务文件`，以确定是否有需要执行的任务。

```
#root用户有一个定时任务文件
[root@pylinux ~]# ls -l /var/spool/cron/
总用量 4
-rw------- 1 root root 141 10月  9 14:42 root
#查看此root定时任务文件的内容
[root@pylinux ~]# cat /var/spool/cron/root
*/1 * * * * /usr/local/qcloud/stargate/admin/start.sh > /dev/null 2>&1 &
0 0 * * * /usr/local/qcloud/YunJing/YDCrontab.sh > /dev/null 2>&1 &
#等同于如下命令
[root@pylinux ~]# crontab -l
*/1 * * * * /usr/local/qcloud/stargate/admin/start.sh > /dev/null 2>&1 &
0 0 * * * /usr/local/qcloud/YunJing/YDCrontab.sh > /dev/null 2>&1 &
```
### crontab命令
crontab命令被用来提交和管理用户的需要周期性执行的任务，与windows下的计划任务类似

| 参数 | 解释 | 使用示例 |
| --- | --- | --- |
| -l | list查看定时任务 | crontab -l |
| -e | edit编辑定时任务，建议手动编辑 | crontab -e |
| -i | 删除定时任务，提示用户确认删除，避免出错 | crontab -i |
| -r | 删除定时任务，移除/var/spool/cron/username文件，全没了 | crontab -r |
| -u user | 指定用户执行任务，root可以管理普通用户计划任务 | crontab -u gege -l |

crontab命令就是在修改`/var/spool/cron`中的定时任务文件
_用户查看定时任务_

```
crontab -l #列出用户设置的定时任务，等于cat var/spool/cron/root
crontab -e  #编辑用户的定时任务，等于如上命令编辑的是 vi /var/spool/cron/root文件
```
_检查crond服务是否运行_

```
[root@pylinux ~]# systemctl is-active crond
active
[root@pylinux ~]# ps -ef|grep crond
root       711     1  0 10月20 ?      00:00:01 /usr/sbin/crond -n
```
_定时任务相关的文件_

```
/var/spool/cron  定时任务的配置文件所在目录
/var/log/cron  定时任务日志文件
/etc/cron.deny  定时任务黑名单
```
![](https://cdn.nlark.com/yuque/0/2021/jpeg/194754/1610807990513-687b40f3-e5be-4bd2-aed2-daaa0b03309c.jpeg#align=left&display=inline&height=586&margin=%5Bobject%20Object%5D&originHeight=586&originWidth=1590&size=0&status=done&style=none&width=1590)
### 定时任务语法格式
口诀：什么时候做什么事
查看定时任务配置文件

```
[root@luffycity ~]# cat /etc/crontab
```
![](https://cdn.nlark.com/yuque/0/2021/jpeg/194754/1610807990527-6368805c-a7e3-49bf-ab9a-1528e9c298ad.jpeg#align=left&display=inline&height=878&margin=%5Bobject%20Object%5D&originHeight=878&originWidth=2266&size=0&status=done&style=none&width=2266)
案例

```
每天上午8点30，去上学
30 08 * * *  go to school
每天晚上12点回家回家睡觉
00 00  *  * *  go home
```
_定时任务符号_

```
crontab任务配置基本格式：
*  *　 *　 *　 *　　command
分钟(0-59)　小时(0-23)　日期(1-31)　月份(1-12)　星期(0-6,0代表星期天)　 命令
第1列表示分钟1～59 每分钟用*或者 */1表示
第2列表示小时1～23（0表示0点）
第3列表示日期1～31
第4列表示月份1～12
第5列标识号星期0～6（0表示星期天）
第6列要运行的命令
（注意：day of month和day of week一般不同时使用）
（注意：day of month和day of week一般不同时使用）
（注意：day of month和day of week一般不同时使用）
```
时间表示法：

- 特定值，时间点有效取值范围内的值
- 通配符，某时间点有效范围内的所有值，表示"每"的意思
| 特殊符号 | 含义 |
| --- | --- |
| * | _号，表示"每"cmd表示每月每周每日的23:00整点执行命令 |
| - | 减号表示时间范围分隔符，如17-19，代表每天的17、18、19点 |
| , | 逗号，表示分隔时段，如30 17,18,19 * cmd 表示每天的17、18、19的半点执行命令 |
| /n | n表示可以整除的数字，每隔n的单位时间，如每隔10分钟表示 _* cmd |

示例

```
0 * * * *   每小时执行，每小时的整点执行
1 2 * * 4   每周执行，每周四的凌晨2点1分执行
1 2 3 * *   每月执行，每月的3号的凌晨2点1分执行
1 2 3 4 *    每年执行，每年的4月份3号的凌晨2点1分执行
1 2 * * 3,5   每周3和周五的2点1分执行
* 13,14 * * 6,0  每周六、周日的下午1点和2点的每一分钟都执行
0 9-18 * * 1-5   周一到周五的每天早上9点一直到下午6点的每一个整点(工作日的每个小时整点)
*/10 * * * *  每隔10分钟执行一次任务
*7 * * * *    如果没法整除，定时任务则没意义,可以自定制脚本控制频率
定时任务最小单位是分钟，想完成秒级任务，只能通过其他方式（编程语言）
```
![](https://cdn.nlark.com/yuque/0/2021/jpeg/194754/1610807990514-d44eb3a8-4b27-419b-8b37-377334bfdecb.jpeg#align=left&display=inline&height=2981&margin=%5Bobject%20Object%5D&originHeight=2981&originWidth=2270&size=0&status=done&style=none&width=2270)
案例1

```
*/1 * * * * /bin/sh  /scripts/data.sh      #每分钟执行命令
30 3,12 * * *  /bin/sh  /scripts/data.sh  #每天的凌晨3点半，和12点半执行脚本
30 */6 * * *    /bin/sh  /scripts/data.sh     #每隔6小时，相当于6、12、18、24点的半点时刻，执行脚本
30 8-18/2  * * * /bin/sh  /scripts/data.sh  #  30代表半点，8-18/2表示早上8点到下午18点之间每隔两小时也就是8、10、12、14、16、18的半点时刻执行脚本
30 21 * * *  /opt/nginx/sbin/nginx -s reload  #每天晚上9点30重启nginx
45 4 1,10 * *  /bin/sh  /scripts/data.sh   #每月的1、10号凌晨4点45执行脚本
10 1  * 6,0  /bin/sh  /scripts/data.sh   #每周六、周日的凌晨1点10分执行命令
0,30 18-23 * * *  #每天的18点到23点之间，每隔30分钟执行一次
00 */1 * * *  /bin/sh  /scripts/data.sh   #每隔一小时执行一次
00 11 * 4 1-3 /bin/sh  /scripts/data.sh        #4月份的周一到周三的上午11点执行脚本
```
案例2

```
# 每天早上7点到上午11点，每2小时运行cmd命令
00 07-11/2 * * * CMD
0 6 * * * /var/www/test.sh        #每天6点执行脚本
0 4 * * 6 /var/www/test.sh    #每周六凌晨4:00执行
5 4 * * 6 /var/www/test.sh    #每周六凌晨4:05执行
40 8 * * * /var/www/test.sh    #每天8:40执行
31 10-23/2 * * *    /var/www/test.sh    #在每天的10:31开始，每隔2小时重复一次
0 2 * * 1-5 /var/www/test.sh    #每周一到周五2:00
0 8,9 * * 1-5  /var/www/test.sh   #每周一到周五8:00，每周一到周五9:00
0 10,16 * * *  /var/www/test.sh   #每天10:00、16:00执行
```
### 生产环境用户配置定时任务流程
需求：每分钟向`/testcron/hellogege.txt` 文件中写入一句话“哥哥带你学linux”
第一步：新手要注意确保定时任务的正确执行，切莫编写了定时任务就不管不问了

```bash
root@VM-4-16-ubuntu:~# echo "哥哥带你学linux" >> /testcron/hellgege.txt
bash: /testcron/hellgege.txt: No such file or directory
root@VM-4-16-ubuntu:~# # 必须要确保文件夹存在
root@VM-4-16-ubuntu:~# mkdir /testcron
root@VM-4-16-ubuntu:~# echo "哥哥带你学linux" >> /testcron/hellgege.txt
root@VM-4-16-ubuntu:~# cat /testcron/hellgege.txt
哥哥带你学linux
```


第二步：编辑定时任务文件，写入需要定时执行的任务

```
crontab -e 
写入
* * * * * /usr/bin/echo "哥哥带你学linux" >> /testcron/hellochaoge.txt
保存后
[root@pylinux ~]# crontab -e
crontab: installing new crontab
```
第三步：检查定时任务

```
[root@pylinux ~]# crontab -l
* * * * * /usr/bin/echo "哥哥带你学linux" >> /testcron/hellogege.txt
```
第四步：可以检测文件内容

```
tail -f /testcron/hellogege.txt
```
### 每5分钟让服务器进行时间同步

```
crontab -e 
*/5 * * * * /usr/sbin/ntpdate  ntp1.aliyun.com &> /dev/null
```
### 每晚0点整，把站点目录/var/www/html下的内容打包备份到/data目录下

- 提醒，tar命令不建议使用绝对路径打包，特殊情况可以使用-P参数

```
1.检查文件夹是否存在，不存在则创建
[root@pylinux ~]# ls -d /var/www/html /data
ls: 无法访问/var/www/html: 没有那个文件或目录
ls: 无法访问/data: 没有那个文件或目录
2.创建文件夹
[root@pylinux ~]# mkdir -p /var/www/html  /data
[root@pylinux ~]# ls -d /var/www/html /data
/data  /var/www/html
3.创建测试文件
[root@pylinux ~]# touch /var/www/html/gege{1..10}.txt
[root@pylinux ~]# ls /var/www/html/
gege10.txt  gege1.txt  gege2.txt  gege3.txt  gege4.txt  gege5.txt  gege6.txt  gege7.txt  gege8.txt  gege9.txt
4.打包压缩命令
[root@pylinux www]# tar -zcvf /data/bak_$(date +%F).tar.gz  ./html/
```

**编写shell脚本，丢给定时任务定期执行**

```
[root@pylinux scripts]# cat bak.sh
#!/bin/bash
cd /var/www && \
/bin/tar -zcf /data/bak_$(date +%F).tar.gz ./html
```
**创建定时任务**

```
crontab -e
写入
00 00 * * * /bin/sh  /server/scripts/bak.sh > /dev/null 2>&1
#解释 >/dev/null 2>&1 代表把所有输出信息重定向到黑洞文件
> 是重定向符号
/dev/null是黑洞文件
2>&1 代表让标准错误和标准输出一样
此命令表示将脚本执行的正常或者错误日志都重定向到/dev/null，也就是什么都不输出
>/dev/null 2>&1 等价于  1>/dev/null 2>/dev/null  等价于 &> /dev/null
```
### 取消定时任务发邮件功能

```
1.定时任务的命令 >  /dev/null   #命令的执行正确结果输出到黑洞，标准错误还是报错
2.定时任务的命令 &>  /dev/null  #组合符  &> 正确和错误的输出，都写入黑洞，危险命令，有风险，慎用
```
### 补充anacron
如果由于机器故障关机，定时任务未执行，下次开机也不会执行任务
使用anacron下次开机会扫描定时任务，将未执行的，全部执行，服务器很少关机重启，所以忽略。





