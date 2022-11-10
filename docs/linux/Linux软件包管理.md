
修改中英文
```
export LC_ALL=en_US.UTF-8
export LC_ALL=zh_CN.UTF-8
```

# Linux软件包管理

windows程序  exe
macos程序 dmg

Linux程序

```
软件包顾名思义就是将应用程序、配置文件和数据打包的产物，所有的linux发行版都采用了某种形式的软件包系统，这使得linux软件管理和在windows下一样方便，suse、red hat、fedora等发行版都是用rpm包，Debian和Ubuntu则使用.deb格式的软件包。
mysql-5-3-4.rpm
redis-3-4-3.rpm
nginx2-3-2.rpm
```
## 编程语言


- 系统级开发：
   - C/C++：httpd、nginx
   - golang：docker
- 应用及开发：
   - java：hadoop，hbase
   - python：openstack
   - perl
   - ruby
   - php
## 程序格式
**C/C++程序源代码**
```
文本格式的程度代码
```
编译开发环境
```
编译器、头文件、开发库
```
二进制格式组成
```
程序(软件)组成部分：
    二进制程序  可执行命令
    库     .so文件
    配置文件    .conf
    帮助文件    readme    /usr/share/man
```
**java/python程序**
源代码
```
编译成能够在python虚拟机pvm上运行的格式
```
**项目构建工具**
```
c/c++  ：make工具
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830568-9040db87-0a19-44a8-bc02-0b42cbee013a.png#align=left&display=inline&height=542&margin=%5Bobject%20Object%5D&originHeight=542&originWidth=1160&size=0&status=done&style=none&width=1160)
## 程序包管理器
在 RPM(红帽软件包管理器)公布之前，要想在 Linux 系统中安装软件只能采取源码包 的方式安装。早期在 Linux 系统中安装程序是一件非常困难、耗费耐心的事情，而且大多数 的服务程序仅仅提供源代码，需要运维人员自行编译代码并解决许多的软件依赖关系，因此 要安装好一个服务程序，运维人员需要具备丰富知识、高超的技能，甚至良好的耐心。而且在 安装、升级、卸载服务程序时还要考虑到其他程序、库的依赖关系，所以在进行校验、安装、 卸载、查询、升级等管理软件操作时难度都非常大。
RPM 机制则为解决这些问题而设计的。RPM 有点像 Windows 系统中的控制面板，会建 立统一的数据库文件，详细记录软件信息并能够自动分析依赖关系。

Linux程序包管理器，几个发行版

- debian(Ubuntu)：dpt、dpkg、
   - .deb
- redhat：`redhat package manager，简称rpm`
- suse：`rpm`

**源代码格式**
```
格式：name-version.tar.gz
nginx-1.12.0.tar.gz
node-v10.15.3-linux-x64.tar
```
**rpm包格式**
```
格式：name-version-release.arch.rpm
wget-1.14-18.el7.x86_64.rpm
名字，版本号，架构型号
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830577-b65bb101-e3e4-4f55-8591-40db95a2278c.png#align=left&display=inline&height=884&margin=%5Bobject%20Object%5D&originHeight=884&originWidth=2278&size=0&status=done&style=none&width=2278)
## 获取程序包的途径
互联网上提供的软件，可能存在后门，存在安全隐患，插件
_最为正确的途径_

- 操作系统发行版本光盘
- 文件服务器
- 镜像站点

开源镜像站
```
http://mirrors.aliyun.com
http://mirrors.sohu.com
http://mirrors.sohu.com/centos/7.9.2009/isos/x86_64/
http://mirrors.163.com
```

- epel，提供centos众多额外的第三方包，可信任的第三方软件包组织
```
http://mirrors.sohu.com/fedora-epel/7/x86_64/Packages/
https://mirrors.aliyun.com/epel/7/x86_64/Packages/m/
```

- 搜索引擎
```
http://www.rpmfind.net/
http://www.rpmfind.net/linux/mageia/distrib/7/x86_64/media/core/release/lrzsz-0.12.21-22.mga7.x86_64.rpm
```
## rpm命令
```
rpm命令：rpm  [OPTIONS]  [PACKAGE_FILE]
# i表示安装 v显示详细过程 h以进度条显示，每个#表示2%进度
安装软件的命令格式                rpm -ivh filename.rpm    
升级软件的命令格式                rpm -Uvh filename.rpm
卸载软件的命令格式                rpm -e filename.rpm
查询软件描述信息的命令格式         rpm -qpi filename.rpm
列出软件文件信息的命令格式         rpm -qpl filename.rpm
查询文件属于哪个 RPM 的命令格式 　 rpm -qf filename
```
案例
```
wget http://www.rpmfind.net/linux/mageia/distrib/7/x86_64/media/core/release/lrzsz-0.12.21-22.mga7.x86_64.rpm
#测试rpm包
[root@gegelinux pyrpm]# rpm -ivh --test lrzsz-0.12.21-22.mga7.x86_64.rpm
警告：lrzsz-0.12.21-22.mga7.x86_64.rpm: 头V4 RSA/SHA256 Signature, 密钥 ID 80420f66: NOKEY
准备中...                          ################################# [100%]
[root@gegelinux pyrpm]# rpm -ivh lrzsz-0.12.21-22.mga7.x86_64.rpm
警告：lrzsz-0.12.21-22.mga7.x86_64.rpm: 头V4 RSA/SHA256 Signature, 密钥 ID 80420f66: NOKEY
准备中...                          ################################# [100%]
正在升级/安装...
   1:lrzsz-0.12.21-22.mga7            ################################# [100%]
#升级rpm包
[root@gegelinux pyrpm]# rpm -Uvh lrzsz-0.12.21-22.mga7.x86_64.rpm
警告：lrzsz-0.12.21-22.mga7.x86_64.rpm: 头V4 RSA/SHA256 Signature, 密钥 ID 80420f66: NOKEY
准备中...                          ################################# [100%]
正在升级/安装...
   1:lrzsz-0.12.21-22.mga7            ################################# [100%]
#卸载lrzsz工具
rpm -e lrzsz
```
## 软件包依赖关系
在早期系统运维中，安装软件是一件非常费事费力的事情。系统管理员不得不下载软件源代码编译软件，并且为了系统做各种调整。
尽管源代码编译形式的软件增强了用户定制的自由度，但是在小软件上耗费精力是缺乏效率的，于是软件包应运而生。
软件包管理可以将管理员从无休止的兼容问题中释放。yum工具就可以自动搜索依赖关系，并执行安装。
rpm软件包在安装的时候，由作者定义依赖关系
```
必须解决依赖关系，软件才能正常工作
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830598-ee7d3fe9-b0bc-4688-81cf-7aedb49a4b8a.png#align=left&display=inline&height=804&margin=%5Bobject%20Object%5D&originHeight=804&originWidth=1318&size=0&status=done&style=none&width=1318)
### 自动解决依赖关系软件包管理器

- Yum，红帽系列rpm包管理工具
- apt-get，deb包管理工具
- zypper，suse的rpm包管理工具

_windows软件管理工具_
			360软件管家 等等
_Linux软件管理_

![image-20221110125011325](Linux%E8%BD%AF%E4%BB%B6%E5%8C%85%E7%AE%A1%E7%90%86.assets/image-20221110125011325.png)


**yum命令**是在Fedora和RedHat以及SUSE中基于rpm的软件包管理器，它可以使系统管理人员交互和自动化地更细与管理RPM软件包，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软体包，无须繁琐地一次次下载、安装。
尽管 RPM 能够帮助用户查询软件相关的依赖关系，但问题还是要运维人员自己来解决， 而有些大型软件可能与数十个程序都有依赖关系，在这种情况下安装软件会是非常痛苦的。
Yum 软件仓库便是为了进一步降低软件安装难度和复杂度而设计的技术。Yum 软件仓库可以 根据用户的要求分析出所需软件包及其相关的依赖关系，然后自动从服务器下载软件包并安装到系统。
Yum 软件仓库中的 RPM 软件包可以是由红帽官方发布的，也可以是第三方发布的，当然也可以是自己编写的。

### yum工具

- Yum（全称为 Yellow dog Updater, Modified）是一个在Fedora和RedHat以及CentOS中的Shell前端软件包管理器。基于RPM包管理，能够从指定的服务器自动下载RPM包并且安装，可以自动处理依赖性关系，并且一次安装所有依赖的软件包，无须繁琐地一次次下载、安装。
- 说到yum源就必须说到linux系统中特有的依赖关系问题，yum就是为了解决依赖关系而存在的。yum源就相当是一个目录项，当我们使用yum机制安装软件时，若需要安装依赖软件，则yum机制就会根据在yum源中定义好的路径查找依赖软件，并将依赖软件安装好。
- YUM是“Yellow dog Updater, Modified”的缩写，是一个软件包管理器，YUM从指定的地方（相关网站的rpm包地址或本地的rpm路径）自动下载RPM包并且安装，能够很好的解决依赖关系问题。
- YUM的基本工作机制如下： 服务器端：在服务器上面存放了所有的RPM软件包，然后以相关的功能去分析每个RPM文件的依赖性关系，将这些数据记录成文件存放在服务器的某特定目录内。 客户端：如果需要安装某个软件时，先下载服务器上面记录的依赖性关系文件(可通过WWW或FTP方式)，通过对服务器端下载的纪录数据进行分析，然后取得所有相关的软件，一次全部下载下来进行安装。
- Yum repository：yum仓库，存储了众多的软件包，以及相关的元数据文件
   - 文件服务器
      - ftp://
      - http://
      - nfs://
      - file://
   - yum仓库可以存在多个，自动选择软件最新的，以及优先选择离我们近的仓库下载
```
#yum其实也是一个rpm软件
[root@gegelinux pyrpm]# rpm -qa yum
yum-3.4.3-163.el7.centos.noarch
```
### yum客户端
```
/etc/yum.conf  #为所有仓库提供公共配置
[root@gegelinux yum.repos.d]# cat /etc/yum.conf
[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0                                    #本地缓存是否保留，0否，1是
debuglevel=2                                #调试日志级别
logfile=/var/log/yum.log        #日志路径
exactarch=1                                    #精确系统平台版本匹配
obsoletes=1            
gpgcheck=1                                    #检查软件包的合法性
plugins=1                
installonly_limit=5                    #同时安装几个工具包
bugtracker_url=http://bugs.centos.org/set_project.php?project_id=23&ref=http://bugs.centos.org/bug_report_page.php?category=yum
distroverpkg=centos-release        
#  This is the default, if you make this bigger yum won't see if the metadata
# is newer on the remote and so you'll "gain" the bandwidth of not having to
# download the new metadata and "pay" for it by yum not having correct
# information.
#  It is esp. important, to have correct metadata, for distributions like
# Fedora which don't keep old packages around. If you don't like this checking
# interupting your command line usage, it's much better to have something
# manually check the metadata once an hour (yum-updatesd will do this).
# metadata_expire=90m
#请放置你的仓库在这里，并且命名为*.repo类型
# PUT YOUR REPOS HERE OR IN separate files named file.repo
# in /etc/yum.repos.d
```
### repo仓库文件
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830586-c4e86238-e9a0-4078-856d-a26dd66ab974.png#align=left&display=inline&height=1634&margin=%5Bobject%20Object%5D&originHeight=1634&originWidth=2538&size=0&status=done&style=none&width=2538)
```
/etc/yum.repos.d/*.repo #提供仓库的地址文件
CentOS-Base.repo
[base]
name=CentOS-$releasever - Base - mirrors.aliyun.com        #仓库文件的说明
failovermethod=priority    #存在多个url的时候，按顺序来连接，如果是roundrobin，意为随机挑选
baseurl=http://mirrors.aliyun.com/centos/$releasever/os/$basearch/    #指定仓库的网站地址
        http://mirrors.aliyuncs.com/centos/$releasever/os/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/os/$basearch/
gpgcheck=1    #是否检测秘钥
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7      #公钥文件存放路径
#released updates  指定rpm包需要升级的地址，此处可以去网页上寻找对应的包
[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/$releasever/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/$releasever/updates/$basearch/
        http://mirrors.cloud.aliyuncs.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-7
epel.conf
[epel]
name=Extra Packages for Enterprise Linux 7 - $basearch
baseurl=http://mirrors.aliyun.com/epel/7/$basearch
failovermethod=priority
enabled=1        #是否启用此仓库
gpgcheck=0
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
```
自定义一个简单的repo文件

```
touch gege.repo #写入
[base]
name=gege repo 
baseurl=http://gege.com/centos/7/os/x86_64/
gpgcheck=0
[epel]
name=gege epel repo
baseurl=http://gege.com/epel/7/os/x86_64/
gpgcheck=0
```
### 配置yum源

- `[http://mirrors.163.com/](http://mirrors.163.com/)`
- `[https://opsx.alibaba.com/mirrors](https://opsx.alibaba.com/mirrors)`




```
1.备份现有repo仓库
2.下载新的repo文件
CentOS 6
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
CentOS 7
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
3.清空旧yum缓存，生成新的缓存
yum clean all
yum makecache
4.针对阿里云镜像，可能出现无法解析地址的异常
sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
5.配置epel源
epel(RHEL 7)
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
epel(RHEL 6)
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-6.repo
epel(RHEL 5)
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-5.repo
```

- `[http://mirrors.sohu.com/](http://mirrors.sohu.com/)`
### yum命令



```
yum命令的用法：
    yum [options] [command] [package ...]
   command is one of:
    * install package1 [package2] [...]
    * update [package1] [package2] [...]
    * update-to [package1] [package2] [...]
    * check-update
    * upgrade [package1] [package2] [...]
    * upgrade-to [package1] [package2] [...]
    * distribution-synchronization [package1] [package2] [...]
    * remove | erase package1 [package2] [...]
    * list [...]
    * info [...]
    * provides | whatprovides feature1 [feature2] [...]
    * clean [ packages | metadata | expire-cache | rpmdb | plugins | all ]
    * makecache
    * groupinstall group1 [group2] [...]
    * groupupdate group1 [group2] [...]
    * grouplist [hidden] [groupwildcard] [...]
    * groupremove group1 [group2] [...]
    * groupinfo group1 [...]
    * search string1 [string2] [...]
    * shell [filename]
    * resolvedep dep1 [dep2] [...]
    * localinstall rpmfile1 [rpmfile2] [...]
       (maintained for legacy reasons only - use install)
    * localupdate rpmfile1 [rpmfile2] [...]
       (maintained for legacy reasons only - use update)
    * reinstall package1 [package2] [...]
    * downgrade package1 [package2] [...]
    * deplist package1 [package2] [...]
    * repolist [all|enabled|disabled]
    * version [ all | installed | available | group-* | nogroups* | grouplist | groupinfo ]
    * history [info|list|packages-list|packages-info|summary|addon-info|redo|undo|rollback|new|sync|stats]
    * check
    * help [command]
显示仓库列表：
    repolist [all|enabled|disabled]
显示程序包：
    list
        # yum list [all | glob_exp1] [glob_exp2] [...]
        # yum list {available|installed|updates} [glob_exp1] [...]
安装程序包：
    install package1 [package2] [...]
    reinstall package1 [package2] [...]  (重新安装)
升级程序包：
    update [package1] [package2] [...]
    downgrade package1 [package2] [...] (降级)
检查可用升级：
    check-update
卸载程序包：
    remove | erase package1 [package2] [...]
查看程序包information：
    info [...]
查看指定的特性(可以是某文件)是由哪个程序包所提供：
    provides | whatprovides feature1 [feature2] [...]
清理本地缓存：
clean [headers|packages|metadata|dbcache|plugins|expire-cache|all]
构建缓存：
    makecache
搜索：
    search string1 [string2] [...]
    以指定的关键字搜索程序包名及summary信息；
查看指定包所依赖的capabilities：
    deplist package1 [package2] [...]
查看yum事务历史：
    history [info|list|packages-list|packages-info|summary|addon-info|redo|undo|rollback|new|sync|stats]
安装及升级本地程序包：
    * localinstall rpmfile1 [rpmfile2] [...]
       (maintained for legacy reasons only - use install)
    * localupdate rpmfile1 [rpmfile2] [...]
       (maintained for legacy reasons only - use update)
包组管理的相关命令：
    * groupinstall group1 [group2] [...]
    * groupupdate group1 [group2] [...]
    * grouplist [hidden] [groupwildcard] [...]
    * groupremove group1 [group2] [...]
    * groupinfo group1 [...]
如何使用光盘当作本地yum仓库：
    (1) 挂载光盘至某目录，例如/media/cdrom
        # mount -r -t iso9660 /dev/cdrom /media/cdrom
    (2) 创建配置文件
    [CentOS7]
    name=
    baseurl=
    gpgcheck=
    enabled=
yum的命令行选项：
    --nogpgcheck：禁止进行gpg check；
    -y: 自动回答为“yes”；
    -q：静默模式；
    --disablerepo=repoidglob：临时禁用此处指定的repo；
    --enablerepo=repoidglob：临时启用此处指定的repo；
    --noplugins：禁用所有插件；
yum的repo配置文件中可用的变量：
    $releasever: 当前OS的发行版的主版本号；
    $arch: 平台；
    $basearch：基础平台；
    $YUM0-$YUM9
[base]
name=gege repo 
baseurl=http://gege.com/centos/7/os/x86_64/  #使用变量替换，就很方便了
baseurl=http://gege.com/centos/6/os/x86_64/
baseurl=http://gege.com/centos/5/os/x86_64/
gpgcheck=0
```
## systemctl命令
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830589-0c02fdf1-f42d-456c-99c6-7979f0b68958.png#align=left&display=inline&height=632&margin=%5Bobject%20Object%5D&originHeight=632&originWidth=2202&size=0&status=done&style=none&width=2202)
## 源代码编译安装
无论是rpm命令或是yum命令，都是安装二进制格式的程序包，别人编译好的

```
mysql-xx.rpm
redis-xx.rpm
nginx-xx.rpm
```
可能存在的问题，别人给的rpm包，可能版本较低，不合适我们现有的需求
### yum和编译安装的区别
_yum的优缺点_

- yum是自动去yum源中寻找rpm包下载且安装，自动解决依赖，自动指定安装路径，无须人为干预
- 适合初学者，不用考虑依赖关系即可安装使用大部分软件
- 功能由rpm包控制，这个rpm包也是别人编译好的，版本可能较低，功能受限，存在漏洞
- yum自动安装的软件不能定义软件的路径，与功能，机器数量较多，与后期维护成本较大

_编译安装优缺点_

- 可以手动下载最新源代码，按照指定需求，设置参数，指定安装路径，扩展第三方功能，更加灵活
- 无法自动解决依赖关系，对新手不友好

**建议方式**
```
yum和编译安装结合使用，能够最大程度解决问题
```
### 编译三部曲
前提条件：准备好开发工具以及开发环境

```
开发工具：gcc make等
开发组件：
yum groupinstall "Development Tools"
yum groupinstall "Server Platform Development"
```
![](https://cdn.nlark.com/yuque/0/2021/png/194754/1610856830587-03f0c7d6-94fa-4dab-ad16-f8dcfa9379ec.png#align=left&display=inline&height=580&margin=%5Bobject%20Object%5D&originHeight=580&originWidth=958&size=0&status=done&style=none&width=958)
第一曲，执行脚本`configure`文件
```
./configure --prefix=软件安装路径
针对C、C++代码，进行编译安装，需要指定配置文件`Makefile`，需要通过`configure`脚本生成
通过选项传递参数，指定启用特性、安装路径等<执行时会生成makefile
检查依赖到的外部环境
```
第二曲，执行make命令

```
make是Linux开发套件里面自动化编译的一个控制程序，他通过借助 Makefile 里面编写的编译规范进行自动化的调用 gcc 、ld 以及运行某些需要的程序进行编译的程序。一般情况下，他所使用的 Makefile 控制代码，由 configure 这个设置脚本根据给定的参数和系统环境生成。
make这一步就是编译，大多数的源代码包都经过这一步进行编译（当然有些perl或python编写的软件需要调用perl或python来进行编译）
make 的作用是开始进行源代码编译，以及一些功能的提供，这些功能由他的 Makefile 设置文件提供相关的功能，比如 make install 一般表示进行安装，make uninstall 是卸载，不加参数就是默认的进行源代码编译。
```
第三曲：开始安装 make install

```
开始安装软件到./configure指定的安装路径
```
### 源码编译安装nginx

```
1.准备编译环境
yum install gcc patch libffi-devel python-devel  zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel openssl openssl-devel -y
2.获取nginx源代码
wget -c https://nginx.org/download/nginx-1.12.0.tar.gz
3.解压缩nginx源代码
tar -zxvf nginx-1.12.0.tar.gz
4.进入源码目录
cd nginx-1.12.0
5.开始编译三部曲
./configure --prefix=/opt/nginx112/  --with-http_ssl_module --with-http_stub_status_module 
6.执行make指令，调用gcc等编译工具
make
7.开始安装
make install
8.安装后启动nginx软件，找到二进制程序，以绝对路径执行
/opt/ngx112/sbin/nginx
9.检查环境变量，需要手动配置nginx的PATH路径，否则必须绝对路径才能找到
编辑文件/etc/profile.d/nginx.sh
写入export PATH=/opt/ngx112/sbin:$PATH
10.退出回话，重新登录机器
logout
11.检查环境变量
[root@gegelinux ngx112]# cat /etc/profile.d/nginx.sh
export PATH=/opt/ngx112/sbin:$PATH
12.启动nginx，可以访问页面
```
### 环境变量配置文件

```
/etc/profile
用于设置系统级的环境变量和启动程序，在这个文件下配置会对所有用户生效。当用户登录(login)时，文件会被执行，并从/etc/profile.d目录的配置文件中查找shell设置。如果对/etc/profile修改的话必须重启才会生效
~/.profile
每个用户都可使用该文件输入专用于自己使用的shell信息,当用户登录时,该文件仅仅执行一次!默认情况下,他设置一些环境变量,执行用户的.bashrc文件.
~/.bashrc
该文件包含专用于你的bash shell的bash信息,当登录时以及每次打开新的shell时,该该文件被读取.
~/.bash_logout
当每次退出系统(退出bash shell)时,执行该文件，通常存放清理工作的命令。
执行顺序
登陆shell
登陆shell时，首先执行/etc/profile，之后执行用户目录下的~/.profile,~/.profile中会执行~/.bashrc。
```
