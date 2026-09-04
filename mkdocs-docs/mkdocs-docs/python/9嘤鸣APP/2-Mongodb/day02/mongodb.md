<img src="./assets/mongodb-logo.png" alt="img" style="zoom:150%;float: left;" />

# MongoDB基础

官方文档：https://docs.mongodb.com/

中文文档：https://www.mongodb.org.cn/

mongoDB的生态、理念非常先进而且成熟、但是mongoDB不仅有开源版本，还有企业版本。所以有部分公司比较担心，哪天无法使用mongoDB了，所以也会产生一些替代产品。

```
DynamoDB  : AWS
SequoiaDB : 巨杉数据库
```



## 基本介绍 

MongoDB 是由C++语言编写并基于分布式文件存储的开源数据库，属于NOSQL 。

MongoDB 是一款介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的NOSQL数据库。它面向文档存储，而且安装和操作起来都比较简单和容易，而且它支持各种流行编程语言进行操作，如Python，Node.js，Java，C++，PHP，C#等。

目前在大数据、内容管理、持续交付、移动应用、社交应用、用户数据管理、数据中心等领域皆有广泛被使用。

### 什么是mongodb？

MongoDB是一个文档数据库，提供好的性能，领先的非关系型数据库。采用BSON存储文档数据。

BSON（）是一种类json的一种二进制形式的存储格式，全称：Binary JSON.

相对于json多了date类型和二进制数组。



### 为什么用MongoDB？

1.  数据结构简单，没有固定的数据结构

2.  没有复杂的连接，没有复杂的外键约束

3.  深度查询能力,MongoDB支持动态查询，查询api是基于v8引擎（javascript）。

4.  容易调试

5.  容易扩展

6.  不需要转化/映射应用对象到数据库对象

7.  使用内部内存作为存储工作区,以便更快的存取数据。

### mongodb的应用场景

1.  大数据
2.  内容管理系统
3.  移动端App
4.  数据管理
5.  日志处理
6.  游戏道具处理

### MongoDB相对于RDBMS的优势

游戏道具：

​	[{“id”:1, "name": "衣服", "防御值": 1000},

​	{“id”:2, "name": "武器", "攻击力": 9999,  "攻击距离": 50},

​	{“id”:3, "name": "鞋子", "移动速度": 1.1,  "颜色": "蓝色"},]

| id   | name | 防御值 | 攻击力 | 攻击距离 | 移动速度 | 颜色 |
| ---- | ---- | ------ | ------ | -------- | -------- | ---- |
| 2    | 武器 | None   | 9999   | 50       | None     | None |
| 1    | 衣服 | 1000   | None   | None     | None     | None |
| 3    | 鞋子 | None   | None   | None     | 1.1      | 蓝色 |



-   无固定结构 。面向文档，以 JSON 格式的文档保存数据，数据结构由键值(key=>value)对组成。MongoDB 的文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组，单个对象的结构是清晰的。
-   没有复杂的表连接。不需要维护表与表之间的内在关联关系。
-   查询功能强大，丰富的查询语言。MongoDB的查询功能几乎与SQL一样强大，使用基于文档的查询语言，可以对文档进行动态查询，提供丰富的查询操作和索引支持，也有事务操作，可以更快地更稳定的访问数据。(mongoDB4.0以后才真正支持所谓的多文档事务操作)
-   易于调优和扩展。具备高性能、高可用性及可伸缩性等特性
-   应用程序对象与数据库对象天然对应。
-   可分片，对数据存储友好，可以基于内存存储或者硬盘文件存储。
-   任何属性都可以建立索引，而且提供丰富多样的索引。

### 术语对比

|        **RDBMS**        |     **Mongodb**     | 描述                                                 |
| :---------------------: | :-----------------: | ---------------------------------------------------- |
|     库（database）      |   库（database）    |                                                      |
|       表（Table）       | 集合（Collection）  |                                                      |
|  行/记录（Row/Record）  |  文档（Document）   | Document就是json结构的一条数据记录                   |
| 列/字段（Column/Field） | 字段/键/域（Field） | 属性字段名                                           |
|   主键（Primary Key）   | 对象ID（ObjectId）  | _id: ObjectId("10c191e8608f19729507deea")            |
|      索引（Index）      |    索引（Index）    | 都有普通索引, 唯一索引, 主键索引, 联合索引这么区分的 |

### MySQL 与 MongoDB 的差别

差别在多方面，例如：数据的表示、查询、关系、事务、模式的设计和定义、速度和性能。

MongoDB 是由 C++语言编写的，是一个基于分布式文件存储的开源数据库系统。在高负载的

情况下，添加更多的节点，可以保证服务器性能。

MongoDB 旨在为 WEB 应用提供可扩展的高性能数据存储解决方案。

MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类

似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。

MongoDB 是一个面向文档的数据库，目前由 10gen 开发并维护，它的功能丰富齐全，所以完全可以替代 MySQL。

与 MySQL 等关系型数据库相比，MongoDB 的优点如下：

1.  弱一致性，更能保证用户的访问速度。

2.  文档结构的存储方式，能够更便捷的获取数据。

3.  内置 GridFS，支持大容量的存储。

4.  内置 Sharding。

5.  第三方支持丰富。(这是与其他的 NoSQL 相比，MongoDB 也具有的优势)

6.  性能优越

MongoDB 相对于MySQL，它还算比较年轻的一个产品，所以它的问题，就是成熟度肯定没有传统 MySQL那么成熟稳定。所以在使用的时候，第一，尽量使用稳定版，不要在线上使用开发版，这是一个大原则；

另外一点，备份很重要，MongoDB 如果出现一些异常情况，备份一定是要能跟上。除了通过传统的复制的方式来做备份，离线备份也还是要有，不管你是用什么方式，都要有一个完整的离线备份。往往最后出现了特殊情况，它能帮助到你；

另外，MongoDB 性能的一个关键点就是索引，索引是不是能有比较好的使用效率，索引是不是能够放在内存中，这样能够提升随机读写的性能。如果你的索引不能完全放在内存中，一旦出现随机读写比较高的时候，它就会频繁地进行磁盘交换，这个时候，MongoDB 的性能就会急剧下降，会出现波动。

另外，MongoDB 还有一个最大的缺点，就是它占用的空间很大，因为它属于典型空间换时间原则的类型。那么它的磁盘空间比普通数据库会浪费一些，而且到目前为止它还没有实现在线压缩功能，在 MongoDB 中频繁的进行数据增删改时，如果记录变了，例如数据大小发生了变化，这时候容易产生一些数据碎片，出现碎片引发的结果，一个是索引会出现性能问题，另外一个就是在一定的时间后，所占空间会莫明其妙地增大，所以要定期把数据库做修复，定期重新做索引，这样会提升 MongoDB 的稳定性和效率。



### 基本安装

目前moongDB的最新版本为6.0版本。我们使用ubuntu20.04安装，需要完成以下命令步骤：

```bash
# 安装依赖包
sudo apt-get install -y libcurl4 openssl

# 关闭和卸载原有的mongodb
sudo systemctl stop mongod
sudo apt-get purge mongodb*
sudo apt-get auto-remove
sudo rm -r /var/lib/mongodb
sudo rm -r /var/log/mongodb


# 导入包管理系统使用的公钥
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
# 如果命令执行结果没有显示OK，则执行此命令在把上一句重新执行：sudo apt-get install gnupg

# 注册mongodb源
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# 更新源
sudo apt-get update

# 安装mongodb
sudo apt-get install -y mongodb-org

# 等待上面的安装过程中，可以先创建mongoDB的数据存储目录
sudo mkdir -p /data/db
```

启动和关闭MongoDB

```bash
# 安装完成以后，默认情况下moongDB是没有启动的，需要我们手动加载数据库配置，并启动mongodb
sudo systemctl daemon-reload
sudo systemctl start mongod
# 进入mongo终端：
mongosh

# 退出mongo终端
.exit
# 也可以使用以下命令，退出终端：
#  quit()

# 查看运行状态
sudo systemctl status mongod
# 如果mongodb状态为stop，则运行 sudo systemctl enable mongod

# 停止mongodb
sudo systemctl stop mongod

# 重启mongodb
sudo systemctl restart mongod
```

>   注意：
>
>   MongoDB在刚安装完成后，默认是没有进行用户登录的权限验证，默认是不需要输入用户名密码即可登录的，但是注意，mongoDB是提供了用户身份认证功能的。
>
>   所以，我们也可以在后面启动用户身份与权限认证，但是必须注意：
>
>   mongodb默认是没有管理员账号的，所以要先切换到admin数据库添加管理员账号，再开启权限认证，否则就玩大了。

进入mongo终端的打印效果，如下：

```bash
Current Mongosh Log ID:	63452259fc4d746f759ce077  # log日志的ID
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.0   # 终端连接url地址
Using MongoDB:		6.0.2  # mongo的版本号
Using Mongosh:		1.6.0   # mongo交互终端程序的版本号

# 如果要查看更多关于mongoDB交互终端的操作文档如下：
For mongosh info see: https://docs.mongodb.com/mongodb-shell/

------
   The server generated these startup warnings when booting
   # 警告：强烈建议使用XFS文件系统，并使用WiredTiger存储引擎。 （mongoDB的WiredTiger存储引擎类似于 MySQL中的InnoDB存储引擎）
   # 解释：因为当前ubuntu20.04使用的是ext4文件系统，mongodb官方建议使用XFS文件系统功能更能发挥mongodb的性能，忽略不管
   2022-10-11T15:57:00.605+08:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   # 警告：当前mongodb没有为数据库启用访问控制。对数据和配置的读写访问是不受限制的，因此会带来不必要的安全隐患。
   # 解释：后面会创建数据库用户采用密码登陆的。暂时不用管
   2022-10-11T15:57:01.254+08:00: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
   # 警告：当前vm虚拟机的进程内存相关参数max_map_count最大内存映射区域数 设置的数值太小了。
   # 解析：max_map_count的默认值是65536，设置到262144这个数值即可。
   2022-10-11T15:57:01.254+08:00: vm.max_map_count is too low
------

------
   Enable MongoDB's free cloud-based monitoring service, which will then receive and display
   metrics about your deployment (disk utilization, CPU, operation statistics, etc).
   
   The monitoring data will be available on a MongoDB website with a unique URL accessible to you
   and anyone you share the URL with. MongoDB may use this information to make product
   improvements and to suggest MongoDB products and deployment options to you.
   
   To enable free monitoring, run the following command: db.enableFreeMonitoring()
   To permanently disable this reminder, run the following command: db.disableFreeMonitoring()
------

Warning: Found ~/.mongorc.js, but not ~/.mongoshrc.js. ~/.mongorc.js will not be loaded.
  You may want to copy or rename ~/.mongorc.js to ~/.mongoshrc.js.

```

开启和关闭云监控平台

![image-20211102160327594](assets/image-20211102160327594.png)

```javascript
// 开启云监控平台[公司一般不会允许内部信息泄露，所以不会开启这个功能]
db.enableFreeMonitoring()
// 关闭云监控平台
db.disableFreeMonitoring()
```

成功运行了mongoDB以后，对于mongod和mongosh的区别

mongod是处理MongoDB系统的主要进程。主要负责处理数据请求，管理数据存储和执行后台管理操作。当我们运行mongod命令意味着正在启动MongoDB进程, 并且在后台运行。

mongosh是一个命令行实现的客户端操作mongodb的工具，用于连接一个特定的mongod实例。当我们没有带参数运行mongosh命令它将使用默认的localhost:27017和mongod进行连接。

mongoDB的默认端口：27017



```bash
# 查看交互终端的版本
mongosh --version
# 或者终端内部使用 version()
```



## 基本操作

### 通用操作

#### 查看帮助文档

```javascript
help
```

终端效果：

```bash
db                    查看当前用户所在数据库的数据库对象
use <db>         set current database   切换操作的数据库
show                 'show databases'/'show dbs': Print a list of all available databases. 查看当前系统所有的数据库
                         'show collections'/'show tables': Print a list of all collections for current database. 查看当前数据库所有的数据集合
                         'show profile': Prints system.profile information.  查看当前系统的环境配置
                         'show users': Print a list of all users for current database. 查看当前数据库中所有的管理员用户
                         'show roles': Print a list of all roles for current database.  查看当前数据库中所有的管理员角色
                         'show log <type>': log for current connection, if type is not set uses 'global'  查看指定日志信息
                         'show logs': Print all logs.  查看全部日志
it                       result of the last line evaluated; use to further iterate  查看更多的查询结果，相当于下一页
exit                    quit the mongo shell  退出终端
sleep                 Sleep for the specified number of milliseconds   睡眠函数，指定睡眠毫秒
load                  Loads and runs a JavaScript file into the current shell environment  加载指定js文件的js代码到当前mongo shell交互终端下
cls                     Clears the screen like console.clear()   清屏
print                  Prints the contents of an object to the output   打印输出一个终端对象
```



#### 当前服务器状态

```javascript
db.serverStatus()
```

终端效果：

```bash
{
	"host" : "ubuntu",    # 主机名
	"version" : "6.0.2",  # mongodb server 版本
	"process" : "mongod", # mongodb进程，主要有mongod和mongos(分片集群中)两种
	"pid" : NumberLong(1034),  # mongod的pid进程号，可以在linux终端下使用命令 pidof mongod 验证
	"uptime" : 105063,    # mongodb服务启动的秒数，时间短则表示近期有重启，时间长则表示在稳定运行
	"uptimeMillis" : NumberLong(105063193), # mongod服务启动的毫秒数
	"uptimeEstimate" : NumberLong(105063),  # mongod内部自己计算的启动秒数
	"localTime" : ISODate("2020-12-08T16:01:08.230Z"), # 本地时间，相当于 python的 datetime.now()
	# 客户端连接数相关 
	"connections" : {
		"current" : 8,  # 当前连接数的编号
		"available" : 51192, # 可用最大连接数
		"totalCreated" : 1,  # 截止目前为止总共历史创建的连接数
		"active" : 1,   # 还在活跃的连接数，查看并发连接数主要参考这个值
	},
        # 全局锁相关信息
	"globalLock" : {
		"totalTime" : NumberLong("105063115000"), # mongod启动后到现在的总时间，单位微秒
		"currentQueue" : { # 当前等待锁队列
			"total" : 0,   # 当前全局锁的等待个数
			"readers" : 0, # 当前全局读锁等待个数
			"writers" : 0  # 当前全局写锁等待个数
		},
		"activeClients" : {
			"total" : 0,   # 当前活跃客户端的个数
			"readers" : 0, # 当前活跃客户端中进行读操作的个数
			"writers" : 0  # 当前活跃客户端中进行写操作的个数
		}
	},

	"network" : { # 网络相关
		"bytesIn" : NumberLong(1611),    # 数据库接收到的网络传输字节数
		"bytesOut" : NumberLong(51269),  # 从数据库发送出去的网络传输字节数
		"numRequests" : NumberLong(16),  # mongod接收到的总请求次数
	},
	
	# 操作计数器
	"opcounters" : {
		"insert" : NumberLong(0),  # 本次mongod实例启动至今收到的插入操作总数 
		"query" : NumberLong(287), # 本次mongod实例启动至今收到的查询总数。
		"update" : NumberLong(0),  # 本次mongod实例启动至今收到的更新操作总数 。
		"delete" : NumberLong(0),  # 本次mongod实例启动至今的删除操作总数。
		"getmore" : NumberLong(0), # 本次mongod实例启动至今“getmore”操作的总数。
		"command" : NumberLong(588)# 本次mongod实例启动至今向数据库发出的命令总数 。
	},

	# 存储引擎,是MongoDB的核心组件, 负责管理数据如何存储在硬盘（Disk）和内存（Memory）上的组件
	# MongoDB 支持多种不同的存储引擎（Storage Engine），MongoDB支持的存储引擎有：WiredTiger，MMAPv1和In-Memory。
	# 1. WiredTiger，将数据持久化存储在硬盘文件中；从MongoDB 3.2 版本开始，成为MongDB默认存储引擎
	# 2. In-Memory，将数据存储在内存中
	# 3. MMAPv1，将数据持久化存储在硬盘文件中; MongoDB 3.2 版本以前的默认存储引擎，类似mysql里面的 MyISAM
	
	# WiredTiger 是比MMAPv1更好用，更强大的存储引擎，WiredTiger的写操作会先写入缓存(Cache)中，并持久化到WAL(Write ahead log，写日志)，每60s或日志文件达到2GB时会做一次Checkpoint(检查点)，将当前数据进行持久化，产生一个新的快照。Wiredtiger连接初始化时，首先将数据恢复至最新的快照状态，然后根据WAL恢复数据，以保证存储可靠性。
	# Checkpoint，检测点。将内存中的数据变更冲刷到磁盘中的数据文件中，并做一个标记点。
	#             表示此前的数据表示已经持久存储在了数据文件中，此后的数据变更存在于内存（CPU缓存）和WAL日志中.
	#             是一种让数据库redo（重做）和data（数据）文件保持一致的机制。这种机制，并非Mongodb独有的，mysql中的InnoDB也有。

	"storageEngine" : {
		"name" : "wiredTiger",   # 当前mongoDB系统默认的存储引擎是 wiredTiger
		"supportsCommittedReads" : true,
		"oldestRequiredTimestampForCrashRecovery" : Timestamp(0, 0),
		"supportsPendingDrops" : true,
		"dropPendingIdents" : NumberLong(0),
		"supportsTwoPhaseIndexBuild" : true,
		"supportsSnapshotReadConcern" : true,
		"readOnly" : false,
		"persistent" : true,
		"backupCursorOpen" : false
	},
	
        # 多文档事务，mongodb4.0以后新增特性
	"transactions" : {
		"retriedCommandsCount" : NumberLong(0),
		"retriedStatementsCount" : NumberLong(0),
		"transactionsCollectionWriteCount" : NumberLong(0),
		"currentActive" : NumberLong(0),
		"currentInactive" : NumberLong(0),
		"currentOpen" : NumberLong(0),
		"totalAborted" : NumberLong(0),
		"totalCommitted" : NumberLong(0),
		"totalStarted" : NumberLong(0),
		"totalPrepared" : NumberLong(0),
		"totalPreparedThenCommitted" : NumberLong(0),
		"totalPreparedThenAborted" : NumberLong(0),
		"currentPrepared" : NumberLong(0)
	},
	"locks":{ # 锁相关
	
	},
	"mem" : { # 内存相关
		"bits" : 64, # 操作系统位数
		"resident" : 18,  # 物理内存消耗,单位：M
		"virtual" : 1566, # 虚拟内存消耗,单位：M
		"supported" : true # 是否显示额外的内存信息
	},
}
```



#### 查看当前db的连接机器地址

```
db.getMongo()
```



#### 查看日志

```javascript
show logs
// global
// startupWarnings

// 如果要查看具体文件的日志。
show log global   
// global是全局日志，默认保存的日志文件在 /var/log/mongodb/mongod.log
// 如果mongoDB无法启动，查看错误就可以来到默认日志文件查看
```



#### 数据备份与恢复

MongdoDB一共提供了4个命令行工具给我们对数据进行备份与恢复以及导入与导出数据。

备份与恢复操作的数据文件格式是bson格式，二进制文件，不需要进入mongo终端

导入与导出数据的数据文件格式是json格式，文本文档格式，不需要进入mongo终端



##### 准备测试数据

mongoDB终端下进行以下操作：

```javascript
// 进入mongo交互终端
mongosh

use test  // mongoDB中可以使用use切换数据库，针对不存在的数据库会自动创建，可通过db在终端查看当前所在数据库

// 声明了一个函数，生成一个指定随机整数，不足10，前面补0
formatnumber = (start, end)=>{
    num = Math.round(Math.random() * (end-start)) + start
    if(num<10){
        return "0"+num;
    }else{
        return num;
    }
}

// 声明了一个函数，生成具有随机标题
rand_title = ()=>{
    num = Math.round( Math.random() * 10 );
    num1 = Math.round( Math.random() * 10 );
    return [
        "赠送礼品-"+num,
        "购物狂欢-"+num,
        "随便买买-"+num,
        "愉快购物-"+num,
        "赠送礼物-"+num,
        "商品购买-"+num,
        "买多送多-"+num,
        "买年货-"+num,
        "买买买买-"+num,
        "充值会员-"+num
    ][num1];
}

// 创建一个函数，循环生成指定的数据
function rand_data(size=200000){
    for(var i=0; i<size; i++){
        // 往当前数据库的orders集合(相当于mysql的orders数据表) 添加1条数据
        db.orders.insertOne({
            "order_number": ( "0000000000000000" + i ).substr( String(i).length ),  
            "date": "20"+formatnumber(0,21)+"-"+formatnumber(1,12)+"-"+formatnumber(1,31),  
            "title": rand_title(i),
            "user_id": parseInt(i/200)+1,
            "items" :[{ 
                "goods_id" : parseInt(i/200)+1,
                "goods_number" : formatnumber(2, 10),  
                "price" : formatnumber(50, 1000)
            },{ 
                "goods_id" : parseInt(i/200)+2,
                "goods_number" :formatnumber(2, 10),  
                "price" : formatnumber(50, 1000)
            }]
        })
        // 判断循环过程中，i每逢1000则打印一次数据
        if(i%10000==0){
            print("已经添加了"+Math.ceil(i/10000)+"万条数据！");
        }
    }
}

// 调用上面生成测试数据的函数
rand_data()

// 查看上面生成的数据
db.orders.find()
// 每次显示的数据，mongoDB交互终端默认只会显示20条，所以如果要查看更多，则根据提示输入it可以查看下一页数据。
```



##### 数据备份

命令格式：

```bash
mongodump -h dbhost -d dbname -o dbdirectory
```

参数说明：

| 选项 | 作用                          | 备注                           |
| ---- | ----------------------------- | ------------------------------ |
| -h   | MongoDB服务端地址和端口的简写 | --host=MongoDB地址 --port=端口 |
| -d   | 备份的数据库名称              | --db=数据库名称                |
| -o   | 备份数据保存目录所在路径      | 备份数据保存目录需要提前创建   |

例如：备份上面的test数据库

```bash
mongodump -h 127.0.0.1:27017 -d test -o /home/moluo/Desktop/

# 删除demo数据库
mongosh
use test
db.dropDatabase()
# 再次查看，可以发现没有任何数据了
db.orders.find()
```



##### 数据恢复

命令格式：

```bash
mongorestore -h dbhost -d dbname --dir dbdirectory --drop
```

参数说明：

| 选项   | 作用                                | 备注                           |
| ------ | ----------------------------------- | ------------------------------ |
| -h     | MongoDB服务端地址和端口的简写       | --host=MongoDB地址 --port=端口 |
| -d     | 恢复的数据库名称                    | --db=数据库名称                |
| --dir  | 备份数据所在目录                    |                                |
| --drop | 恢复数据前，先删除MongoDB中的旧数据 |                                |

例如：恢复上面备份的test数据库

```bash
mongorestore -h 127.0.0.1:27017 -d test --dir /home/moluo/Desktop/test  --drop

# 进入数据库查看
use test
# 统计当前数据库下orders集合里面所有的文档总数
db.orders.countDocuments()
```



##### 数据导出

命令格式：

```bash
mongoexport -h dbhost -d dbname -c collectionname -o file --type json/csv -f field
```

参数说明：

| 选项   | 作用                          | 备注                                                         |
| ------ | ----------------------------- | ------------------------------------------------------------ |
| -h     | MongoDB服务端地址和端口的简写 | --host=MongoDB地址 --port=端口                               |
| -d     | 要导出的数据库名称            | --db=数据库名称                                              |
| -c     | 要导出的集合名称              | --collection=集合名称                                        |
| -o     | 导出数据保存的文件名          |                                                              |
| -f     | 导出数据的文档字段列表        | 如果不执行-f，则默认导出文档的全部字段                       |
| --type | 导出数据的文件格式            | 默认是json，也可以是csv，当数据格式为csv时，另需加上-f "字段1,字段2,...." |



例如：导出上面的test数据库的orders集合的所有数据

```bash
mongoexport  -h 127.0.0.1:27017 -d test -c orders -o /home/moluo/Desktop/test_orders.json --type json
```



##### 数据导入

命令格式：

```bash
mongoimport -h dbhost -d dbname -c collectionname --file filename --type json/csv  --headerline -f field
```

参数说明：

| 选项   | 作用                          | 备注                                                         |
| ------ | ----------------------------- | ------------------------------------------------------------ |
| -h     | MongoDB服务端地址和端口的简写 | --host=MongoDB地址 --port=端口                               |
| -d     | 要导入的数据库名称            | --db=数据库名称                                              |
| -c     | 要导入的集合名称              | --collection=集合名称                                        |
| --file | 导入数据保存的文件名          |                                                              |
| --type | 导入数据的文件格式            | 默认是json，<br>也可以是csv，当数据格式为csv时：<br>1. 需加上-f "字段1,字段2,...."<br>2. 可以选择加上--headerline，把首行视为导入字段行，不认为是实际数据 |

例如：把上面导出的json文件中的数据，导入到demo数据库的orders集合中

```bash
mongoimport   -h 127.0.0.1:27017 -d test -c orders --file /home/moluo/Desktop/test_orders.json --type json
```



### 用户管理

#### 创建用户

```javascript
db.createUser(user, pwd, writeConcern)
```

创建一个数据库新用户用db.createUser()方法，如果用户存在则返回一个用户重复错误。

错误信息：`uncaught exception: Error: couldn't add user: User "用户名@数据库" already exists`

**详细语法**：

```javascript
db.createUser({
    user: "<用户名>",
    pwd: "<密码>",
    customData: { <any information> }, // 任意内容，主要是为了表示用户身份的相关介绍 
    roles: [ // 角色和权限分配，一个用户可以绑定多个角色，也就是具备多个角色的权限
	{ role: "<角色名>", db: "<数据库名>" },  // 也可以直接填写由mongoDB内置的角色，例如: "<role>"
	...
    ]
})
```

>   注意：
>
>   与之前学习的redis或MySQL不同，mongoDB的用户是**以数据库为单位**来分别建立和管理用户访问控制权限的，每个数据库有属于自己的一个或多个管理员。
>
>   管理员可以管理自己的数据库，但是不能直接管理其他数据库，要先在内置数据库admin认证后才可以。
>
>   管理员的权限设置包含了2块，分别是角色和权限，由创建用户时通过roles属性进行设置。

##### 内置角色

也叫内建角色，是MongoDB安装以后默认创建提供给我们使用的。

```javascript
数据库用户角色：read、readWrite
数据库管理角色：dbAdmin、dbOwner、userAdmin
集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager
备份恢复角色：backup、restore
所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase 
超级用户角色：root
// 超级用户角色 提供了系统超级用户的访问权限
// 有几个角色间接或直接提供了系统超级用户的访问权限（dbAdmin、dbOwner 、userAdmin、userAdminAnyDatabase、dbAdminAnyDatabase）
```



##### 内置权限

```
Read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
root：只在admin数据库中可用。超级账号，擁有超级权限，对所有数据具有超级权限。
```



##### 给Admin数据库创建账户管理员（相当于给mpongoDB创建了一个HR）

当前账号只能用于管理admin数据库账号，不能进行其他数据库的操作。

```javascript
// 进入/切换数据库到admin中
use admin
// 创建账户管理员
// [用户名:admin，密码:123456，数据库:admin，角色userAdminAnyDatabase，表示admin用户在admin数据库中具有超级用户权限]
db.createUser({
	user: "admin",
	pwd: "123456",
	roles: [
		{role: "userAdminAnyDatabase",db:"admin"},
	]
});

// 终端效果如下：
Successfully added user: {
	"user" : "admin",
	"roles" : [
		{
			"role" : "userAdminAnyDatabase",
			"db" : "admin"
		}
	]
}
```



##### 创建超级管理员

当前账号可以进行数据库相关操作。

```javascript
// 进入/切换数据库到admin中
use admin
// 创建超级管理员账号
db.createUser({
    user: "root",
    pwd: "123456",
    roles: [
    	{role:"root", db:"admin"},  // 也可以这样简写："root",
    ]
})

// 终端效果如下：
Successfully added user: {
	"user" : "root",
	"roles" : [
		{
			"role" : "root",
			"db" : "admin"
		}
	]
}

```



##### 创建用户自己的数据库的角色

帐号是跟着数据库绑定的，所以是什么数据库的用户，就必须先到指定库里授权和验证！！！

一般开发中，往往一个项目就分配一个数据库，并给这个数据库分配一个管理员！！！

```javascript
// 切换数据库，如果当前库不存在则自动创建
use yingmingapp;
// 创建管理员用户，为了保证不会报错，所以先删除同名管理员 db.system.users.remove({user:"yingmingapp"});
db.createUser({
    user: "yingmingapp",
    pwd: "123456",
    roles: [
        { role: "dbOwner", db: "yingmingapp"}
    ]
})

// 终端下的效果
/*
Successfully added user: {
	"user" : "yingmingapp",
	"roles" : [
		{
			"role" : "dbOwner",
			"db" : "yingmingapp"
		}
	]
}
*/

// 查看当前仓库下的用户
show users;
/* 效果：
{
	"_id" : "yingmingapp.yingmingapp",
	"userId" : UUID("126f2bd2-cddc-450a-9814-3e8937827ab3"),
	"user" : "yingmingapp",
	"db" : "yingmingapp",
	"roles" : [
		{
			"role" : "dbOwner",
			"db" : "yingmingapp"
		}
	],
	"mechanisms" : [
		"SCRAM-SHA-1",
		"SCRAM-SHA-256"
	]
}
*/

// 也可以在admin库中全局显示所有用户
use admin
db.system.users.find()
```



#### 用户信息

##### 查看当前数据库下的管理用户

只需要切换到对应的库中即可查看

```javascript
use yingmingapp
show users
```

##### 查看系统中所有的用户

需要切换到admin中使用账号管理员的权限进行操作

```javascript
use admin
// db.auth("root","123456") // 如果开启了mongoDB的访问控制，就需要下用户认证密码才能继续往下操作
db.system.users.find() // 只能在admin数据库中使用。
// db.system.users.find().pretty()  // 在mongoDB5.0以前的版本中，pretty表示在返回多个查询结果时，以结构化格式显示数据
```



#### 删除用户

语法格式：

```javascript
db.system.users.remove(json条件)
```

例如，删除上面的用户名为yingmingapp的用户。

```javascript
// 有多种删除方式，下面是根据user用户名删除用户
use admin
db.system.users.deleteOne({user:"yingmingapp"});

// 删除效果：
WriteResult({ "nRemoved" : 1 })  // nRemoved 大于0表示成功删除管理员，等于0则表示没有删除。
```



#### 修改密码

必须切换到对应的数据库下才能给用户修改密码。

所以针对账户管理员或者超级管理员，需要在admin下修改，而其他数据库管理员则必须到对应数据库下才能修改。

```js
db.changeUserPassword("账户名", "新密码");
```

mongo终端操作：

```javascript
use yingmingapp
// 添加测试账号：
db.createUser({
    user: "yingmingapp",
    pwd: "123456",
    roles: [
        { role: "dbOwner", db: "yingmingapp"}
    ]
})
// 注册必须保证有这个管理员
db.changeUserPassword("yingmingapp", "123");
```



#### 开启账户认证

开启账户认证功能，必须要修改配置文件，然后重启mongoDB才能生效。

```javascript
sudo vim /etc/mongod.conf
// 找到31行附近的 security，去掉左边注释符号(#)
security:
    authorization: enabled

:wq
// 重启mongdb，配置生效
sudo systemctl restart mongod

// 开启了账户认证机制以后，再次进入yingmingapp
mongosh
use yingmingapp
show users    // 此处会报错如：uncaught exception: Error: command usersInfo requires authentication
db.auth("yingmingapp","123")   // 此处认证时填写正确密码：
// { ok: 1 }

exit
mongosh
use yingmingapp
db.auth("yingmingapp","123456")  // 此处认证时填写错误密码：
// MongoServerError: Authentication failed.


// 注意：如果实现以某个库的账户管理员登录数据库以后，要切换账号操作其他数据库，则必须先退出当前登录状态。
```



### 数据库管理

显示所有数据库列表【空数据库不会显示，或者说空数据库已经被mongoDB回收了。】

```javascript
show dbs
show databases
```

切换数据库，如果数据库不存在则创建数据库。

```javascript
use  <database>
```

查看当前工作的数据库

```javascript
db   // 是 db.getName() 的简写
```

删除当前数据库，如果数据库不存在，也会返回`{"ok":1}`

```javascript
use <db>          // 先切换到要删除的数据库中，然后才能删除数据库
db.dropDatabase()
```

查看当前数据库状态

```json
test> db.stats()
{
  db: 'test', // 当前数据库名
  collections: 1,  // 当前数据库中的数据集合数量，相当于mysql的数据表
  views: 0, // 当前数据库中的视图数量
  objects: 200000, // 当前数据库中的文档数据，相当于mysql中的数据记录
  avgObjSize: 235.415035,  // 当前数据库中的文档平均大小
  dataSize: 47083007, // 当前数据库中的数据总文件大小
  storageSize: 10096640,  // 存储引擎占据的文件大小
  indexes: 1,   // 当前数据库中的索引数量
  indexSize: 2756608, // 当前数据库中的索引文件大小
  totalSize: 12853248,   // 数据库中总数据总文件大小
  scaleFactor: 1,
  fsUsedSize: 41576349696,  // 文件系统空间占用大小
  fsTotalSize: 51989970944,  // 文件系统的总占用空间大小
  ok: 1
}
```

在mongoDB中，最重要的核心是文档，如果一个库或者一个库下的集合中的文档全部被删除了，则这个库和这个集合就意味着不存在，会被mongoDB回收删除。



### 集合管理

mongoDB中的集合有2种：固定集和动态集。

#### 创建集合

一般工作中使用的是动态集，但是在mongoDB优化时，可以对部分数据转换成使用固定集来保存，性能更好，查询速度更快。

在mongodb中如果使用的动态集，其实不需要专门创建集合，直接添加文档，mongodb也会自动生成动态集合的。而固定集需要设置存储的文档上限数量，所以需要提前创建集合。

```javascript
// name为必填参数，options为可选参数。capped若设置值为true，则size必须也一并设置
db.createCollection(
	<集合名称>,   //  同一数据库中，集合名是唯一的，不能重复创建，否则报错！
	{ 
		capped : <boolean>,       // 当前创建的集合是否是固定集，固定集指限制固定数据大小的集合，当数据达到最大值会自动覆盖最早添加的文档内容
		size : <bytes_size>,          // 如果capped值为True，则表示创建固定集，需要指定固定集合存储的最大字节数，单位：字节数.
		max : <collection_size>   // 如果capped值为True，则表示创建固定集，需要指定固定集合中包含文档的最大数量，单位：字节数
	}
);

// db.createCollection不填写第二个参数则表示创建的是动态集
// 添加文档到不存在的集合中，mongodb会自动创建动态集合，
// db.<集合名称>.insert({"name":"python入门","price" : 31.4})
db.courses.insert({"name":"python入门","price" : 31.4})
```



#### 固定集的使用操作

固定集一般用于日志，历史记录中。固定集，会因为设置了max或size上限而出现文档被驱逐/出列的情况。后面新增超出部分的数据依旧被添加到集合中，但是最早添加的同等数据数据会被删除掉。

```javascript
// 创建固定集记录用户的访问足迹，集合名：history
> db.createCollection("history", {capped:true, size: 1000000, max: 5, });
{ "ok" : 1 }

// 可以通过show tables 直接查看当前数据库中所有的集合列表
> show tables;
// history
// orders

// 添加数据到固定集
test > db.history.insert({"name":"python入门","price" : 31.4})
// WriteResult({ "nInserted" : 1 })
test > db.history.insert({"name":"python入门","price" : 32.4})
// WriteResult({ "nInserted" : 1 })
test > db.history.insert({"name":"python入门","price" : 33.4})
// WriteResult({ "nInserted" : 1 })
test > db.history.insert({"name":"python入门","price" : 34.4})
// WriteResult({ "nInserted" : 1 })
test > db.history.insert({"name":"python入门","price" : 35.4})
// WriteResult({ "nInserted" : 1 })
test > db.history.insert({"name":"python入门","price" : 36.4})
// WriteResult({ "nInserted" : 1 })

// 上面一共添加了6条数据到固定集，当时因为创建固定时设置了只允许5条数据，
// 所以固定集中针对旧的数据已经删除，只保留最新的5数据。
test > db.history.find()
// [
//   {_id: ObjectId("634563f011b6d817d0188edd"), name: 'python入门', price: 32.4 }, 
//   {_id: ObjectId("634563f211b6d817d0188ede"), name: 'python入门', price: 33.4 }, 
//   {_id: ObjectId("634563f511b6d817d0188edf"), name: 'python入门', price: 34.4 },
//   {_id: ObjectId("634563f711b6d817d0188ee0"), name: 'python入门', price: 35.4 },
//   {_id: ObjectId("634563f911b6d817d0188ee1"), name: 'python入门', price: 36.4 }
// ]
```



#### 集合列表

```javascript
show collections // 或 show tables   或 db.getCollectionNames()
```

#### 删除集合

删除集合，那么集合中原有的文档数据也被删除掉。

```javascript
db.集合.drop()
```

#### 查看集合

```javascript
// 获取集合的对象
// db.getCollection("集合名称")   或者 db.集合名称

test> db.getCollection("orders")
test.orders
test> db.orders
test.orders

```

##### 查看集合状态信息

```javascript
// db.集合名称.stats()
db.orders.stats()
// 打印效果：
{
  ns: 'test.orders',   // 当前集合的命名空间（namespace）
  size: 47083007,    // 当前集合的数据总字节数
  count: 200000,     // 当前集合的文档数量
  avgObjSize: 235,  // 当前集合的每个文档平均字节数
  capped: false,       // 当前集合是否是固定集
  },
  nindexes: 1,           // 当前集合的索引数量，默认如果没有特定设置，默认mongoDB会给文档添加一个_id作为主键。
  totalIndexSize: 2756608,  // 当前集合的索引的总字节数
  totalSize: 12853248,         // 当前集合的数据总字节数
  indexSizes: { _id_: 2756608 },   // 当前集合的索引的数值上限
}

```



### 文档管理

mongodb中，文档也叫 object/document。对应的就是存储的bson数据记录，对应的就是python中的字典或者列表。

mongodb中，允许文档中有各种的自定义字段，每一个字段对应的值也存在不同数据格式，根据不同的格式产生不同的数据类型。

#### 数据类型

| Type               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **ObjectID**       | 用于存储文档的ID,相当于主键，区分文档的唯一字段，mongoDB中就是一个ObjectID对象的返回值。一共由3部分组成：4个字节的时间戳、5个字节的客户端进程生成的随机数、3个字节的增量计数器，一共12字节长度的十六进制数，以此保证了每一个文档的唯一性。 |
| **String**         | 字符串是最常用的数据类型，MongoDB中的字符串必须是UTF-8编码。 |
| **Integer**        | 整数类型用于存储数值。整数可以是32位，也可以是64位，这取决于你的服务器。 |
| **Double**         | 双精度类型，用于存储浮点值，mongodb中没有float浮点数这个说法 |
| **Boolean**        | 布尔类型用于存储布尔值(true/ false)，注意：是小写的！！！    |
| **Arrays**         | 将数组、列表或多个值存储到一个键，[]                         |
| **Timestamp**      | 时间戳，用于记录文档何时被修改或创建。Date()，Timestamp()，ISODate() ,默认是ISODate() |
| **Date**           | 用于以UNIX时间格式存储当前日期或时间。                       |
| **Object**         | 用于嵌入文档, 相当于子属性是另一个json文档而已，这种方式就可以实现嵌套。{} |
| **Null**           | 空值，相当于 python的None                                    |
| Symbol             | 与字符串用法相同，常用于某些使用特殊符号的语言，可以理解为一种二进制格式字符串 |
| **Binary data**    | 二进制数据，常用于保存文件的内容，往往是图片、音频、视频等数据本身。 |
| Code               | 用于将JavaScript代码存储到文档中                             |
| Regular expression | 正则表达式                                                   |

虽然，MongoDB中提供了数据类型，但是mongoDB中对于文档的添加，是不需要预先约束字段值类型的，而是一种自动推断类型。因此，上面的这些类型，我们知道即可。



#### 添加文档

mongodb中，文档的数据结构和 JSON 基本一样。所有存储在集合中的数据在内部存储的格式都是 BSON 格式。

BSON 是一种类似 JSON 的二进制形式的存储格式，是 Binary JSON 的简称。

```javascript
// 添加文档
// 方式1
db.<集合名称>.insertOne(          // 如果文档存在_id主键为更新数据，否则就添加数据。
   <document>
)

// 方式2：
// 一次性添加多个文档, 多次给同一个集合建议使用insertMany比insertOne效率更好
db.<集合名称>.insertMany([
    <document>,
    <document>,
    ...
])
```

操作：

```javascript
use test;

// 添加一条数据[insert是过去版本的MongoDB提供的添加数据方法]
db.users.insertOne({
    "name": "laoli",  // string
    "age": 33,         // integer
    "sex": true,       // boolean
    "child": {           // Object
        "name":"xiaohuihui",  // string
        "age":6    // integer
    }
});
// WriteResult({ "nInserted" : 1 })


// mongoDB原则上内置了js解释引擎，所以支持js语法
> db.users.findOne()._id
// ObjectId("61552b913ccd8ec29dbf6512")
> db.users.findOne().name
// laoli

// javascrit总可以通过typeof 来查看数据的类型
> typeof db.users.findOne().name
// string
> typeof db.users.findOne()._id
// object
> typeof db.users.findOne.sex
// boolean
> typeof db.users.findOne.age
// number
> typeof db.users.findOne.child
// object
> typeof db.users.findOne.child.name
// string


// 添加一条数据
db.users.insertOne({"name":"xiaozhang","age":18,"sex":true, "money": 300.50});
// {
// 	"acknowledged" : true,
// 	"insertedId" : ObjectId("605021e6d5c7a55cc95c1cb7")
// }


// 添加多条数据
db.users.insertMany([
    {"name":"xiaolan","age":16},
    {"name":"xiaoguang","age":16}
]);

// {
// 	"acknowledged" : true,
// 	"insertedIds" : [
// 		ObjectId("60502235d5c7a55cc95c1cba"),
// 		ObjectId("60502235d5c7a55cc95c1cbb")
// 	]
// }
db.users.find()
```



#### 删除文档

```json
// 方式1: 删除一条数据
db.<集合名称>.deleteOne(
   <filter>,  // removed的条件表达式，一般写法：{"字段":{查询器函数:值}}，如果不填写删除条件，删除所有文档
)

// 方式2：删除多条数据
db.<集合名称>.deleteMany(
   <filter>,  // removed的条件表达式，一般写法：{"属性":{条件:值}}，如果不填写条件，删除所有文档
)
```

操作：

```javascript
// 添加多条测试数据
document1 = {"name":"xiaohei","age":16}
document2 = {"name":"xiaobai","age":15}
document3 = {"name":"xiaolan","age":18}
document4 = {"name":"xiaohui","age":11}
document5 = {"name":"xiaoming","age":13}
db.users.insertMany([document1,document2,document3,document4,document5]);

// 删除满足条件的第一条数据
// mongoDB中的条件格式: {字段名:{$运算符:值}
// 条件：{"age":{$eq:16}}   相当于SQL语句的age=16
db.users.deleteOne({"age":{$eq:16}})
db.users.deleteOne({"age":16}); // 等于可以省略不写，相当于 db.users.remove({"age":{$eq:16}});


// 再次 添加多条测试数据
db.users.insertOne({"name": "laozhang", "age": 33, "sex": true, child: {name: "xiaozhang", "age": 4}})
db.users.insertOne({"name": "laowang", "age": 32, "sex": true, child: {name: "xiaowang", "age": 2}})
db.users.insertOne({"name": "laoli", "age": 33, "sex": true, child: {name: "xiaoli", "age": 1}})
db.users.insertOne({"name": "laosun", "age": 34, "sex": true, child: {name: "xiaosun", "age": 7}})
db.users.insertOne({"name": "laozhao", "age": 32, "sex": true, child: {name: "xiaozhao", "age": 6}})
db.users.insertOne({"name": "laoyang", "age": 35, "sex": true, child: {name: "xiaoyang", "age": 4}})
db.users.insertOne({"name": "laohuang", "age": 36, "sex": true, child: {name: "xiaohuang", "age": 3}})

// 删除一条
db.users.deleteOne({"child.age": {$lte: 2}})  // 删除1条 孩子年龄小于或等于2岁的家长数据，

// 删除多条
db.users.deleteMany({"child.age": {$lt: 5}})  // 把所有孩子年龄小于5岁的家长数据全部删除
```

mongoDB中的条件，不仅用于删除数据的条件，也可以是查询或者更新的过滤条件。



#### 查询文档

```json
// 直接显示查询的所有，find和findOne的第二个参数，也是一个json对象，一般称之为字段投影，表示设置是否显示或隐藏指定数据字段。

// 获取一条
db.集合.findOne(
    <query>，     // 查询条件，删除、查询、修改都需要设置条件、条件写法基本一样的。
    {                      // 查询结果的字段投影，用于指定查询结果以后，显示的字段列
    	<field>: 0, // 隐藏指定字段，例如："_id":0,
    	<field>: 1, // 显示指定字段，例如："title":1,
    	....
    }
)

// 获取多条
db.集合.find(
	<query>,      // 查询条件
    {
    	<key>: 0, // 隐藏指定字段，例如："_id":0,
    	<key>: 1, // 显示指定字段，例如："title":1,
    	....
    }
)

// 以易读的方式来格式化显示读取到的数据，只能在find方法后面使用。mongoDB6.0版本以后。默认以易读的方式来格式化显示
db.集合.find().pretty()
```

操作：

```javascript
// 切换数据库
use yingmingapp;

// 查询整个集合的所有数据
db.users.find()
db.users.find({})  // 没有设置任何条件

// 查询一条数据
db.users.findOne()    // 获取集合中第一条数据
db.users.findOne({})  // 同上
```



##### 字段投影

`find()`方法默认将返回文档的所有数据，但是可以通过设置`find()`的第二个参数projection，设置值查询部分数据。

操作：

```javascript
// 设置字段投影，显示结果中字段列
db.users.find({}, {"child": 0})    // 获取集合中所有数据，并隐藏child属性的数据
db.users.find({}, {"_id": 0, "child": 0})    // 获取集合中所有数据，并隐藏_id 与 child属性的数据
db.users.find({}, {"name": 1})    //  获取集合中所有数据，并只显示name属性与_id主键的字段数据[注意：_id如果不明确隐藏，默认显示的]
db.users.find({}, {"name": 1, "_id": 0})    //  获取集合中所有数据，并只显示name属性的字段数据
```



##### 条件运算符

mongoDB中，条件运算符也叫查询器（query selector）

###### 比较运算

| 操作       | 格式                                                   | 语法例子                               | SQL中的类似语句            |
| :--------- | :----------------------------------------------------- | :------------------------------------- | :------------------------- |
| 等于       | 写法1：`{<key>:<val>`}<br>写法2：`{<key>:{$eq:<val>}}` | `db.集合.find({"name":"xiaoming"})`    | `where name = 'xiaoming'`  |
| 小于       | `{<key>:{$lt:<val>}}`                                  | `db.集合.find({"age":{$lt:17}})`       | `where age  < 17`          |
| 小于或等于 | `{<key>:{$lte:<val>}}`                                 | `db.集合.find({"age":{$lte:17}})`      | `where age  <= 17`         |
| 大于       | `{<key>:{$gt:<val>}}`                                  | `db.集合.find({"age":{$gt:17}})`       | `where age  > 17`          |
| 大于或等于 | `{<key>:{$gte:<val>}}`                                 | `db.集合.find({"age":{$gte:17}})`      | `where age  >= 17`         |
| 不等于     | `{<key>:{$ne:<val>}}`                                  | `db.集合.find({"age":{$ne:17}})`       | `where age != 17`          |
| 包含       | `{<key>:{$in:[<val>...]}}`                             | `db.集合.find({"age":{$in:[1,2,3]}})`  | `where age in (1,2,3)`     |
| 不包含     | `{<key>:{$nin:[<val>...]}}`                            | `db.集合.find({"age":{$nin:[1,2,3]}})` | `where age not in (1,2,3)` |

终端运行

```javascript
// 添加测试数据
db.users.insertOne({"name": "laozhang", "age": 33, "sex": true, child: {name: "xiaozhang", "age": 4}})
db.users.insertOne({"name": "laowang", "age": 32, "sex": true, child: {name: "xiaowang", "age": 2}})
db.users.insertOne({"name": "laoli", "age": 33, "sex": true, child: {name: "xiaoli", "age": 1}})
db.users.insertOne({"name": "laosun", "age": 34, "sex": true, child: {name: "xiaosun", "age": 7}})
db.users.insertOne({"name": "laozhao", "age": 32, "sex": true, child: {name: "xiaozhao", "age": 6}})
db.users.insertOne({"name": "laoyang", "age": 35, "sex": true, child: {name: "xiaoyang", "age": 4}})
db.users.insertOne({"name": "laohuang", "age": 36, "sex": true, child: {name: "xiaohuang", "age": 3}})
db.users.insertOne({"name": "zhangsanfeng"})

// 查询年龄大于33岁的用户信息
db.users.find({"age":{$gt:33}})
// 查询年龄小于33岁的用户信息
db.users.find({"age":{$lt:33}})
// 查询年龄在32，33，34岁范围里面用户信息
db.users.find({"age":{$in:[32,33,34]}})
// 注意：没有当前字段的文档是不会被通过大于、小于或等于查询出来，因为默认条件不成立
// 所以依靠不存在的字段，是无法使用比较运算符查询出上面添加zhangsanfeng的
db.users.find({"age":{$lt:33}})
db.users.find({"age":{$gte:33}})
db.users.find({"age":{$in:[33]}})
db.users.find({"age":{$nin:[33]}})  // 使用排除范围的方式，可以查询出来。
db.users.find({"age":{$ne: 33}})    // 使用不等于的方式，可以查询出来。
```



###### 逻辑运算

| 操作                  | 语法                                                         | 语法例子                                                     |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `$and`                | 写法1：`{<key>:<val>,<key>:<val>,...}`<br>写法2：`{$and: [{key:{$运算符:<val>}},....]}` | db.集合.find({key1:value1, key2:value2})                     |
| `$or`                 | `{$or: [{<key>: {$运算符:<val>}}, ....]}`                    | db.集合.find({$or: [{key1: value1}, {key2:value2}]})         |
| `$and`和`$or`组合使用 | 写法1：`{<key>:<val>, $or: [{<key>: {<$运算符>:<val>}},...]}`<br>写法2：`{$and:[{$or:[{<key>:{<$运算符>:<val>}},..]},$or:[{<key>:{<$运算符>:<val>}},..]}]}` | db.集合.find({key1:value1, $or: [{key1: value1}, {key2:value2}]}) |
| $not                  | `{<key>:{$not:{<$运算符>:<val>}}}`                           | db.集合.find({key1:{$not:{$运算符: val1}}})                  |

```javascript
SQL:
	(class=301 and sex =true)  or (class=302 and sex=false)
mongo:
	{
            $or: [
        	{$and: [{class:301}, {sex:true}]},
        	{$and: [{class:302}, {sex:false}]},
            ]
       }
```



$and，终端操作：

```javascript
// 查询age>34 并且 child.age<5
db.users.find({
    $and:[
        {"age":{$gt:34}},
        {"child.age":{$lt: 5}}
    ]
})
// 简写；
db.users.find({"age": {$gt:34}, "child.age": {$lt:5}})

// 查詢age=35，child.age=4
db.users.find({
    $and:[
        {"age":{$eq:35}},
        {"child.age":{$eq: 4}}
    ]
})

// 简写
db.users.find({
    $and:[
        {"age": 35},
        {"child.age": 4}
    ]
})

// 再次简写：
db.users.find({
        "age": 35, 
        "child.age": 4,
})
```

$or、$and与$or的组合使用，终端操作：

```javascript
// 查询age=33或者age=36
db.users.find({
    $or: [
        {"age":{$eq:33}},
        {"age":{$eq:36}}
    ]
})
// 简写：
db.users.find({
    $or:[
        {"age":33},
        {"age":36}
    ]
})

// 查询age=33，child.age==5 或者 age=35，child.age==4
db.users.find({
    $or: [
        {$and: [{age: {$eq: 33}}, {"child.age": {$eq: 5}}]},
        {$and: [{age: {$eq: 35}}, {"child.age": {$eq: 4}}]},
    ]
})

// 简写：
db.users.find({
    $or: [
        {$and: [{age: 33}, {"child.age": 5}]},
        {$and: [{age: 35}, {"child.age": 4}]},
    ]
})

// 再次简写：
db.users.find({
    $or: [
        {age: 33, "child.age": 5},
        {age: 35, "child.age": 4},
    ]
})
```

$not，终端操作：

```javascript
// 查询年龄!=16的
db.users.find({"age":{$not:{$eq:33}}})
// 简写：
db.users.find({"age":{$ne: 33}})
```



###### 其他运算符

| 操作    | 格式                                                         | 语法例子                                  | 说明                                                         |
| ------- | ------------------------------------------------------------ | ----------------------------------------- | ------------------------------------------------------------ |
| $type   | `{<key>:{$type: <datetype>}}`                                | `db.集合.find({"name":{$type:'string'}})` | 匹配指定键是指定数据类型的文档<br>number 数值型<br>string 字符串<br>bool 布尔类型<br>object json文档对象类型<br>array 数组类型 |
| $exists | `{<key>:{$exists:<bool>}`                                    | `db.集合.find({"title":{$exists:true}})`  | 匹配具有指定键的文档，存在指定字段的文档                     |
| $regex  | `{ <key>:/模式/<修正符>}`<br>`{<key>:{$regex:/模式/<修正符>}}` | `db.集合.find({"name":{$regex:/张$/}})`   | 按正则匹配                                                   |
| $mod    | `{<key>: {$mod: [除数, 余数]}}`                              | `db.集合.find({"age":{$mod:[10,0]}})`     | 算数运算，取模，语法中举例是age除以10==0                     |
|         |                                                              |                                           |                                                              |

终端操作：

```javascript
db.users.insert({"name":"xiaoming","sex":0,"age":"18", "mobile": "13313621234"});
db.users.insert({"name":"xiaoming","sex":1,"age":18, "mobile": "13441351234"});
db.users.insert({"name":"xiaoming","sex":1,"age":33, "mobile": "13851351234"});
db.users.insert({"name":"xiaoming","sex":0,"age":"33", "mobile": "13881351234", child: {"age": 3, "sex": true}});
db.users.insert({"name":"xiaoming","sex":1,"age":33, "mobile": "10086"});
// $type的使用
db.users.find({"sex":{$type:"number"}});
db.users.find({"sex":{$type:"bool"}});
db.users.find({"age":{$type:"string"}});


// $exists
db.users.find({"child":{$exists:true}}); // 查询出存在child字段的数据

// $regex 正则匹配
db.users.find({"mobile":{$regex: /^133/ }});
// 不符合手机号码格式的
db.users.find({"mobile":{$not:{$regex: /1[3-9]\d{9}/ }}});


// $mod 取模，注意：仅针对数值类型，对于字符串是不识别的，所以$mod[3,0]，对于 "18"来说，并非整除！
db.users.find({"age":{$mod: [3,0] }});
```



###### 自定义条件查询函数

慎用！效率差，因为需要额外调用javascript执行引擎才过滤，相对效率差。

```json
// 用法1，逻辑比较复杂的情况，可以使用更多的javascript进行运算处理：结果函数结果为true，则当前数据被查询出来。
db.<集合名称>.find({$where: function(){   // this代表的就是查询过程中，被循环的每一条文档数据
    return <this.字段> <运算符> <条件值>;
}}});

// 用法2，相对没那么复杂的，取函数的返回值作为条件值:
db.集合.find({$where: "<this.字段> <运算符> <条件值>"});
// db.集合.find({$where:"this.name=='xiaoming'"});
```

操作：

```javascript
db.users.find({$where: function(){
    return this.age>33 && this.child.age<4;
}});

// 把字符串作为代码条件执行，当结果为true，则返回当前符合的数据
db.users.find({$where: "this.age>33 && this.child.age<4"});
```



##### 排序显示

```json
db.集合.find().sort({<key>:1})  // 升序，默认为升序
db.集合.find().sort({<key>:-1}) // 倒序，
```

终端操作：

```javascript
db.users.find().sort({age:-1});
db.users.find().sort({age:-1, "child.age":-1});
```



##### 限制与偏移

`limit`方法用于限制返回结果的数量

`skip`方法用于设置返回结果的开始位置

```json
db.集合.find(...).limit(结果数量).skip(开始下标)
```

终端操作：

```javascript
db.users.find().sort({age:-1}).limit(3);  // 年龄最大的三个人
db.users.find().sort({age:-1}).limit(3).skip(3)  // 按年龄倒序排序，找到排名在4-6之间的用户

db.users.find({},{"_id":0,"name":1,"age":1}).sort({"age":1}).limit(5);  // 年龄升序排序，第1-5名

db.users.find({},{"_id":0,"name":1,"age":1}).sort({"age":1}).limit(5).skip(0); // 年龄升序排序，第一页，第1-5名
db.users.find({},{"_id":0,"name":1,"age":1}).sort({"age":1}).limit(5).skip(5); // 年龄升序排序，第二页，第6-10名
```



#### 更新文档

文档：https://www.mongodb.com/docs/manual/tutorial/update-documents/

```json
// 更新一条
db.集合.updateOne(
   <query>,   // update的查询条件，一般写法：{"属性":{条件:值}}
   <update>,  // update的更新数据，一般写法 { $set:{"属性":"值",....} } 或者 { $inc:{"属性":"值"} }
   {
     upsert: <boolean>, // 可选参数，如果文档不存在，是否插入objNew, true为插入，默认是false，不插入
     multi: <boolean>,  // 可选参数，是否把满足条件的所有数据全部更新，设置更新1条还是多条
     writeConcern: <document> // 可选参数，抛出异常的级别。
   }
)

// 更新多条
db.集合.updateMany(
   <query>,   // update的查询条件，一般写法：{"属性":{条件:值}}
   <update>,  // update的对象，一般写法 { $set:{"属性":"值"} } 或者 { $inc:{"属性":"值"} }
   {
     upsert: <boolean>, // 可选参数，如果文档不存在，是否插入objNew, true为插入，默认是false，不插入
     multi: <boolean>,  // 可选参数，是否把满足条件的所有数据全部更新
     writeConcern: <document> // 可选参数，抛出异常的级别。
   }
)

// 替换一条数据
db.collection.replaceOne(
   <filter>,
   <replacement>,
   {
     upsert: <boolean>,      // 可选参数，如果文档不存在，是否插入objNew, true为插入，默认是false，不插入
     writeConcern: <document>,  // 可选参数，抛出异常的级别。
     collation: <document>,
   }
)
```



##### update更新运算符[修改器]

| 操作                   | 语法                                                         |                                                              |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `$inc`                 | `db.集合.updateOne(查询条件,{$inc:{<key2>:<val2>}})`         | 更新key1=val1的文档中key2的值为val2，类似python的递增递减<br>递减，则`{ $inc:{<key2>:-<val2>} }` |
| `$set`                 | `db.集合.updateOne(查询条件, {$set:{<key2>:<val2>}})`        | 更新key1=val1的文档中key2的值为val2，如果key2不存在则新增对应键值对 |
| `$unset`               | `db.集合.updateOne(查询条件, {$unset:{<key2>:<val2>}})`      | 移除key1=val1的文档中key2=val2这个键值对                     |
| `$push`                | `db.集合.updateOne(查询条件, {$push:{<key2>:<val2>}})`       | 给key1=val1的文档中key2列表增加1个数组成员val2。<br>key2必须是数组。 |
| `$addToSet 结合 $each` | `db.集合.updateOne(查询条件, {$addToSet:{<key2>: {$each: [<val2>, <val3>....]}}})` | 一次性给属性key2的数组中追加多个成员。重复成员不会追加       |
| `$pull`                | `db.集合.updateOne(查询条件, {$pull:{<key2>:<val2>}})`       | 与push相反，给key1=val1的文档中key2列表删除1个指定成员val2   |
| `$pullAll`             | `db.集合.updateOne(查询条件, {$pullAll:{<key2>:[<val2>,<val3>]}})` | 与$pull作用一样，用于删除多个指定成员                        |
| `$pop`                 | `db.集合.updateOne(查询条件, {$pop:{<key2>:<val2>}})`        | 给key1=val1的文档中key2列表移除第一个或最后一个成员。<br>val2的值只能是1(最后面)或-1(最前面)，与python相反 |
| `$rename`              | `db.集成.updateOne(查询条件, {$rename: {<key2>: <key3>}})`   | 把属性key2重命名为key3                                       |

终端操作：

```javascript
// $inc
// 把符合条件的用户的年龄+2岁
db.users.updateOne({"name":"laoli"},{$inc:{"age": 2}}); // 更新一条
db.users.updateMany({"name":"laoli"},{$inc:{"age":2}}); // 更新多条
// 把符合条件的用户的孩子年龄+2岁
db.users.updateMany({"name":"laoli"},{$inc:{"child.age": 2}});   // 更新多条


// $set
// 如果字段不存在，则新增字段的键值对，如果字段存在，则修改字段的值
//更新laoli的手机号码
db.users.updateOne({"name":"laoli"},{$set:{"mobile":"18012312312"}}); // 更新一条
// 重新设置年龄
db.users.updateOne({"name":"laoli"},{$set:{"age":18}});

// $unset
// 移除laoli的性别键值对
db.users.updateOne({"name": "laoli"}, {$unset: {"sex": true}})

// $push  往数组字段的值追加成员
db.users.updateOne({"name": "laoli"}, {$push: {"lve": "TV"}})  // 不存在的字段，自动设置成新字段，并把TV作为数组成员。 lve: [ 'TV' ]
db.users.updateOne({"name": "laoli"}, {$push: {"lve": "game"}})  // 已存在的字段，自动追加成员到数组中。lve: [ 'TV', 'game' ]
db.users.updateOne({"name": "laoli"}, {$push: {"lve": ["code"]}})  // 所有设置的值，都会作为成员被追加数组中作为成员，lve: [ 'TV', 'game', [ 'code' ] ]

// $pull  从数组属性中移除成员
db.users.updateOne({"name":"laoli"}, {$pull:{"lve": "TV"}})   /// lve: [ 'game', [ 'code' ] ]
db.users.updateOne({"name":"laoli"}, {$pull:{"lve": ["code"]}})  //   lve: [ 'game' ]

// $addToSet 结合 $each 把多个成员添加到数组属性中
db.users.updateOne({"name": "laoli"}, {$addToSet:{"lve": {$each: ["shoping", "walk"]}}})

// $pullAll 移除多个成员
db.users.updateOne({"name": "laoli"}, {$pullAll: {"lve": ["game", "walk"]}})

// 添加多个测试数据
db.users.updateOne({"name": "laoli"}, {$addToSet:{"lve": {$each: ["shoping", "walk", "TV", "game"]}}})

// $pop
db.users.updateOne({"name":"laoli"}, {$pop: {"lve": -1}}) // 左边移除列表的第一个成员
db.users.updateOne({"name":"laoli"}, {$pop: {"lve": 1}}) // 右边移除列表的最后一个成员

// $rename 字段名/属性名 重命名
db.users.updateOne({"name": "laoli"}, {$rename: {"lve": "love"}})

// replaceOne 替换数据
db.users.replaceOne({"name": "laoli"}, {"name":"xiaoli", "age": 21, "sex": false}) // 除了主键，全部被替换，如果有声明主键，也能替换
```



### 索引操作

前面学习过MySQL，我们知道数据库里给数据构建索引通常能够**极大的提高数据查询的效率**，缩短查询耗时，如果没有索引，数据库在查询数据时必然会扫描数据表中的每个记录并提取那些符合查询条件的记录。同理，**在MongoDB中构建索引也可以提高数据的查询效率和缩短查询耗时**，没有索引的情况也是一样，MongoDB也会再查询数据时扫描集合中的每个文档并提取符合查询条件的文档。这种扫描全集合的查询效率是无疑是非常低下的，特别在处理大量的集合数据时，查询时间可能会达到几十秒甚至几分钟，这对用户体验来说是非常致命的。

文档：https://docs.mongodb.com/manual/indexes/



#### 准备数据

```javascript
// 进入mongo交互终端
mongosh

use test  // mongoDB中可以使用use切换数据库，针对不存在的数据库会自动创建，可通过db在终端查看当前所在数据库

// 声明了一个函数，生成一个指定随机整数，不足10，前面补0
formatnumber = (start, end)=>{
    num = Math.round(Math.random() * (end-start)) + start
    if(num<10){
        return "0"+num;
    }else{
        return num;
    }
}

// 声明了一个函数，生成具有随机标题
rand_title = ()=>{
    num = Math.round( Math.random() * 10 );
    num1 = Math.round( Math.random() * 10 );
    return [
        "赠送礼品-"+num,
        "购物狂欢-"+num,
        "随便买买-"+num,
        "愉快购物-"+num,
        "赠送礼物-"+num,
        "商品购买-"+num,
        "买多送多-"+num,
        "买年货-"+num,
        "买买买买-"+num,
        "充值会员-"+num
    ][num1];
}

// 创建一个函数，循环生成指定的数据
function rand_data(size=200000){
    for(var i=0; i<size; i++){
        // 往当前数据库的orders集合(相当于mysql的orders数据表) 添加1条数据
        db.orders.insertOne({
            "order_number": ( "0000000000000000" + i ).substr( String(i).length ),  
            "date": "20"+formatnumber(0,21)+"-"+formatnumber(1,12)+"-"+formatnumber(1,31),  
            "title": rand_title(i),
            "user_id": parseInt(i/200)+1,
            "items" :[{ 
                "goods_id" : parseInt(i/200)+1,
                "goods_number" : formatnumber(2, 10),  
                "price" : formatnumber(50, 1000)
            },{ 
                "goods_id" : parseInt(i/200)+2,
                "goods_number" :formatnumber(2, 10),  
                "price" : formatnumber(50, 1000)
            }]
        })
        // 判断循环过程中，i每逢1000则打印一次数据
        if(i%10000==0){
            print("已经添加了"+Math.ceil(i/10000)+"万条数据！");
        }
    }
}

// 调用上面生成测试数据的函数
rand_data()

// 查看上面生成的数据
db.orders.countDocuments()
// 每次显示的数据，mongoDB交互终端默认只会显示20条，所以如果要查看更多，则根据提示输入it可以查看下一页数据。
```



#### 注意事项

1.  MongoDB的索引是存储在运行内存(RAM)中的，所以必须确保索引的大小不超过内存的限制。

    如果索引的大小超过了运行内存的限制，MongoDB会删除一些索引【这会涉及到mongoDB的驱逐机制，这将导致性能下降】。

2.  MongoDB的索引在部分查询条件下是不会生效的。

    -   正则表达式及非操作符，如 `$nin`,`$not` , 等。
    -   算术运算符，如 $mod, 等。
    -   $where自定义查询函数。
    -   ...

3.  索引会在写入数据（添加、更新和删除）时重排，如果项目如果是写多读少，则建议少使用或者不要使用索引。
4.  一个集合中索引数量不能超过64个。
5.  索引名的长度不能超过128个字符。
6.  一个复合索引最多可以有31个字段。
7.  mongodb索引统一在`system.indexes`集合中管理。这个集合只能通过`createIndex`和`dropIndexes`来操作。

#### 查看索引

```javascript
// 获取当前集合中已经创建的所有索引信息
db.集合.getIndexes()
/*
[{ 
	"v" : 2,   // 索引版本
	"key" : {  // 索引的字段及排序方向(1表示升序，-1表示降序)
		"_id" : 1   // 根据_id字段升序索引
    }, 
    "name" : "_id"   // 索引的名称
}]
*/
use admin
db.auth("root", "123456")
use test
// 获取当前集合中已经创建的索引总大小，以字节为单位返回结果
db.users.totalIndexSize()
```

MongoDB会为插入的文档默认生成`_id`字段（如果文档本身没有指定该字段），`_id`是文档唯一的主键，为了保证能根据文档id快速查询文档，MongoDB默认会为集合创建_id字段的主键索引。



#### 查询分析

与SQL语句类似，MongoDB也提供了一个explain，供开发者进行查询分析，优化查询语句。

explain的使用有3个参数，分别是：queryPlanner、executionStats、allPlansExecution，默认是queryPlanner，开发中常用的是executionStats。

```javascript
db.orders.find({"title":"愉快购物-6"}).explain("executionStats");
/*
{
	"queryPlanner" : {  # 被查询优化器选择出来的查询计划
		"plannerVersion" : 1,  # 查询计划版本
		"namespace" : "test.orders", # 要查询的集合
		"indexFilterSet" : false,  # 是否了使用索引
		"parsedQuery" : {  # 查询条件
			"title" : {
				"$eq" : "购买商品-19"
			}
		},
		 queryHash: '244E9C29',    // 查询缓存的key值
                  planCacheKey: '244E9C29',    // 查询缓存的key值

		"winningPlan" : {     # 最佳执行计划
			"stage" : "COLLSCAN", # 扫描类型/扫描阶段
			"filter" : {     # 过滤条件
				"title" : {
					"$eq" : "购买商品-19"
				}
			},
			"direction" : "forward"  # 查询方向，forward为升序，backward表示倒序。
		},
		"rejectedPlans" : [ ]   # 拒绝的执行计划
	},
	"executionStats" : {  # 最佳执行计划的一些统计信息
		"executionSuccess" : true,  # 是否执行成功
		"nReturned" : 1,   # 返回的结果数
		"executionTimeMillis" : 346,  # 执行耗时
		"totalKeysExamined" : 0,      # 索引扫描次数
		"totalDocsExamined" : 1000000,  # 文档扫描次数，所谓的优化无非是让totalDocsExamined和nReturned的值接近。
		"executionStages" : {     # 执行状态
			"stage" : "COLLSCAN",  # 扫描方式/扫描阶段
			"filter" : {
				"title" : {
					"$eq" : "购买商品-19"
				}
			},
			"nReturned" : 1,   # 返回的结果数
			"executionTimeMillisEstimate" : 5,   # 预估耗时
			"works" : 1000002,   # 工作单元数
			"advanced" : 1,      # 优先返回的结果数
			"needTime" : 1000000,
			"needYield" : 0,
			"saveState" : 1000,
			"restoreState" : 1000,
			"isEOF" : 1,
			"direction" : "forward",
			"docsExamined" : 1000000   # 文档检查数目，与totalDocsExamined一致
		}
	},
	"serverInfo" : {   # 服务器信息
		"host" : "ubuntu",
		"port" : 27017,
		"version" : "4.4.2",
		"gitVersion" : "15e73dc5738d2278b688f8929aee605fe4279b0e"
	},
	"ok" : 1
}

*/

```

stage的扫描类型：

| 类型名称   | 描述                               | 期望  |
| ---------- | ---------------------------------- | ----- |
| COLLSCAN   | 全表扫描                           | False |
| **IXSCAN** | 索引扫描                           | True  |
| **FETCH**  | 根据索引去检索指定document         | True  |
| **IDHACK** | 针对_id进行查询                    | True  |
| COUNTSCAN  | count不使用Index进行count时返回    | False |
| COUNT_SCAN | count使用了Index进行count时返回    | True  |
| SUBPLA     | 未使用到索引的$or查询时返回        | False |
| **TEXT**   | 使用全文索引进行查询时返回         | -     |
| SORT       | 使用sort排序但是无index时返回      | False |
| SKIP       | 使用skip跳过但是无index时返回      | False |
| PROJECTION | 使用limit限定结果但是无index时返回 | False |



#### 创建索引

MongoDB支持多种类型的索引，包括普通索引(也叫单列索引或单字段索引)、复合索引(也叫多字段索引)、多列索引（也叫数组索引）、全文索引、[哈希索引](https://docs.mongodb.org/manual/core/index-hashed/)、[地理位置索引](https://docs.mongodb.org/manual/core/2d/)等，每种类型的索引有不同的使用场合。除此之外，还有一种特殊的ttl索引，ttl索引本质上就是普通索引，只是给索引添加一个过期时间而已。另外MongoDB的全文索引很弱智，如果真要用在开发中，还是建议使用elasticsearch或者Sphinx。

```json
// 创建索引
db.集合.createIndex({
    // 单个字段，则为普通索引，    // sort的值表示排序，值为1表示升序索引，-1表示降序索引
    "字段名1": <sort|type>,       // type的值可以是text，表示创建全文索引。db.集合.find({$text:{$search:"字符串"}})
    "字段名2": <sort|type>,       // 多个字段，则为复合索引
    "字段名3": [<值1>,<值2>,...],  // 多列索引
    ....
}, {
    background: <Boolean>,   // 建索引过程会阻塞数据库的其它操作，background可指定以后台方式创建索引，默认为false
    unique: <Boolean>,  // 是否建立唯一索引，默认值为false，也叫唯一索引
    name: <String>,   // 索引的名称，不填写，则MongoDB会通过连接索引的字段名和排序顺序生成一个索引名称 
    expireAfterSeconds: <integer>, // 设置索引的过期时间，类似redis的expire，也叫TTL索引
    sparse: <Boolean>,  // 对文档中不存在的字段数据是否不启用索引，默认为False
});


// 单字段索引[普通索引]
 db.集合.createIndex({
    "字段名": <sort>,    // sort的值表示排序，值为1表示升序索引，-1表示降序索引
 }, {
	....
 })
// 普通索引创建： db.orders.createIndex({"order_number":1})
// 查询基本使用： db.orders.find({"order_number":"0000000000030014"}).explain("executionStats");


// 多字段索引，也叫复合索引。[类似mysql里面的联合索引]
 db.集合.createIndex({
    "字段名1": <sort>,    // sort的值表示排序，值为1表示升序索引，-1表示降序索引
    "字段名2": <sort>,    // sort的值表示排序，值为1表示升序索引，-1表示降序索引
    "字段名3": <sort>,    // sort的值表示排序，值为1表示升序索引，-1表示降序索引
 }, {
	....
 })

// 复合索引的使用对单字段条件的查找是没有帮助的，必须多字段[必须包含复合索引的字段]条件使用
// 复合索引创建：db.orders.createIndex({"date":1,"user_id":1});
// 查询基本使用：
//     db.orders.find({"date":"2002-09-19","user_id":751}).explain("executionStats");   // 全字段匹配，走索引
//     db.orders.find({"date":"2014-06-12", "order_number":"0000000000030014"}).explain("executionStats");  // 靠左匹配原则，走索引
//     db.orders.find({"user_id":751}).explain("executionStats");  // 不走索引

// 全文索引
 db.集合.createIndex({
    "字段名1": "text",    // type的值只能是text，表示创建全文索引。db.集合.find({$text:{$search:"字符串"}})
 }, {
	....
 })

// 全文索引创建： db.orders.createIndex({"title":"text"});
// 查询基本使用： db.orders.find({$text:{$search:"充值会员-1"}}).explain("executionStats")



// 多列索引[应用的地方是在数组属性]
 db.集合.createIndex({
    "字段名3": [<值1>,<值2>,...],
 }, {
	....
 });

// 创建测试数据
db.doc.drop()
db.doc.insert({"title":"标题1","tags":["python","django"]})
db.doc.insert({"title":"标题1","tags":["python","django"]})
db.doc.insert({"title":"标题1","tags":["python","django"]})
db.doc.insert({"title":"标题2","tags":["java","mvp"]})
db.doc.insert({"title":"标题3","tags":["java","mvp"]})
db.doc.insert({"title":"标题2","tags":["java","mvp"]})
db.doc.insert({"title":"标题3","tags":["python"]})
db.doc.insert({"title":"标题4","tags":["python"]})
db.doc.insert({"title":"标题2","tags":["python","flask"]})
db.doc.insert({"title":"标题3","tags":["java"]})
// 创建多列索引： db.doc.createIndex({"tags":1})
// 查询数据： db.doc.find({"tags":["python"]}).explain("executionStats")



// 唯一索引
db.集合.createIndex({
    "字段名1": <sort>,
}, {
    unique: true,     // 是否建立唯一索引，默认值为false，也叫唯一索引
})
// 创建唯一索引： db.orders.createIndex({"order_number":1},{unique:true, "name": "order_number_unique_1"});
// 查询数据： db.orders.find({"order_number":"0000000000001019"}).explain("executionStats")



// ttl索引
// 使用ttl索引，索引关键字段的值类型必须是Date类型，如果该字段不是date类型或者文档中不存在该字段，则文档不会进行过期处理
// 数据过期的删除工作是在mongoDB中的独立线程内执行的，默认平均60s扫描一次有几率删除，不会立即删除。

// 例如：在文档创建10秒后删除文档
db.orders.createIndex({"date": 1},{expireAfterSeconds: 10});
db.orders.insertOne({
   "date": new Date("2022-01-10 17:30:00"), // 在python中需要通过 utctime
   "user_id": 2,
   "username": "xiaohong"
})

db.orders.insertOne({
   "date": new Date("2022-10-12 19:30:00"), // 在python中需要通过 utctime
   "user_id": 3,
   "username": "xiaolv"
})

// 在文档创建后，由索引字段值指定的时间删除文档
// 创建索引：db.tasks.createIndex({"expire_time":1},{expireAfterSeconds:0})
// 创建测试数据
db.tasks.insertOne( {
   "expire_time": new Date('2022-10-12 18:14:05'), // 在python中需要通过 utctime
   "user_id": 2,
   "username": "xiaoming",
});

db.tasks.insertOne( {
   "expire_time": new Date('2022-10-12 20:16:05'), // 在python中需要通过 utctime
   "user_id": 2,
   "username": "xiaoming"
});
db.tasks.insertOne( {
   "expire_time": new Date('2022-10-12 18:20:10'), // 在python中需要通过 utctime
   "user_id": 3,
   "username": "xiaoming"
});

// 重建索引[一般是在长期项目运行下来，索引创建时间太久了，性能下降的时候使用。]
// !!!!不能在高峰期时运行以下操作，会出现阻塞
db.集合.reIndex();
```



#### 删除索引

MongoDB给文档主键`_id`默认创建单字段索引是无法删除的。

```json
// 删除单个索引
db.集合.dropIndex("索引名称")
// db.orders.dropIndex("date_1")

// 删除所有索引（除了主键_id），慎用
db.集合.dropIndexes()
```





在python当中，一般常用于开发中操作monoDB的模块无非三个：pymongo, mongoEngine,  motor

moter是python中基于pymongo实现的异步操作库，类似于aiomysql，aiomysql也是python基于pymysql实现的异步库。

```python
mysql  pymysql  mysqlDB  aiomysql[基于pymysql实现的异步库]
redis  pyredis  redis    aioredis[基于pyredis实现的异步库]
mongo  pymongo  mongoengine[基于pymongo实现的ORM，高仿django的ORM]  motor[基于pymongo实现的异步库]
```



## PyMongo

文档：https://www.mongodb.com/docs/drivers/python/

文档：https://pymongo.readthedocs.io/en/stable/api/index.html

安装：

```bash
pip install pymongo -i https://pypi.douban.com/simple
```

### 数据库连接

**数据库连接，无密码**

```python
import pymongo

if __name__ == '__main__':
    # 无密码连接mongo[如果mongo没有开启用户访问控制机制的情况下，可以使用]
    mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    ret = mongo.list_databases()
```

**数据库连接，有密码**

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # 有密码连接[最主要的连接方式]
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    print(mongo.list_databases()) # 列出当前账户可操作的所有数据库
```



### 数据库管理

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # # 无密码连接mongo[如果mongo没有开启用户访问控制机制的情况下，可以使用]
    # mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    # ret = mongo.list_databases()


    # 有密码连接
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    print(mongo.list_databases()) # 列出当前账户可操作的所有数据库
    # 切换操作的数据库
    db = mongo["test"]
    print(db)
    # 列出当前数据库下的所有集合
    print(db.list_collections())
    # 获取当前数据库下的指定集合操作对象
    users_collection = db["orders"]
    print(users_collection)
    # 统计当前集合下所有的文档数量
    count = users_collection.count_documents({})
    print(count)
```



### 集合管理

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # # 无密码连接mongo[如果mongo没有开启用户访问控制机制的情况下，可以使用]
    # mongo = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    # ret = mongo.list_databases()


    # 有密码连接
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    print(mongo.list_databases()) # 列出当前账户可操作的所有数据库
    # 切换操作的数据库
    db = mongo["test"]
    print(db)
    print(db.list_collection_names())

    # 列出当前数据库下的所有集合
    print(db.list_collections())
    # 获取当前数据库下的指定集合操作对象
    users_collection = db["orders"]
    print(users_collection)
    # 统计当前集合下所有的文档数量
    count = users_collection.count_documents({})
    print(count)

    # 删除集合
    doc_collection = db["doc"]
    doc_collection.drop()

```



### 文档管理

#### 添加文档

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # 连接数据库
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    # 切换或新建数据库
    db = mongo["yingmingapp"]
    # 切换或新建数据集
    users = db["users"]

    # # 添加一个文档
    # document = {"name": "xiaoming", "mobile": "13012345678", "age": 16}
    # ret = users.insert_one(document)
    # print(ret.inserted_id)  # 返回新增文档的主键ID


    # 添加多个文档
    document_list = [
        {"name": "xiaoming", "mobile": "13033345678", "age": 17},
        {"name": "xiaohong", "mobile": "13044345678", "age": 18},
        {"name": "xiaohei", "mobile": "13612345678", "age": 18},
    ]
    ret = users.insert_many(document_list)
    print(ret.inserted_ids)  # 返回新增文档的主键ID列表
```



#### 删除文档

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # 连接数据库
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    # 切换或新建数据库
    db = mongo["yingmingapp"]
    # 切换或新建数据集
    users = db["users"]

    """删除文档"""
    # 删除一篇文档
    filter = {"name":"xiaoming"}
    ret = users.delete_one(filter)
    print(ret.deleted_count) # 返回删除文档的数量

    # 删除多篇文档
    filter = {"name": "xiaohong"}
    ret = users.delete_many(filter)
    print(ret.deleted_count) # 返回删除文档的数量

    # 按指定条件删除多个文档
    filter = {"age": {"$gte": 17}}  # age >= 17
    ret = users.delete_many(filter)
    print(ret.deleted_count)  # 返回删除文档的数量
    
```



#### 更新文档

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # 连接数据库
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    # 切换或新建数据库
    db = mongo["yingmingapp"]
    # 切换或新建数据集
    users = db["users"]

    """更新文档"""
    # # 更新一个文档
    # filter = {"name": "xiaoming"}
    # update = {"$set": {"name": "xiaohong"}, "$inc": {"age": -3}}
    # ret = users.update_one(filter=filter, update=update)
    # print(ret.modified_count)  # 返回更新文档的数量

    # # 更新多个文档
    # filter = {"name": "xiaohong"}
    # update = {"$set": {"sex": True}}
    # ret = users.update_many(filter=filter, update=update)
    # print(ret.modified_count)  # 返回更新文档的数量

    # 把满足条件的一个文档进行替换
    filter = {"name": "xiaoming"}
    replace = {"name": "xiaolan", "age": 16, "sex": False} # 因为是直接替换文档，所以不需要指定更新运算符
    ret = users.replace_one(filter, replace)
    print(ret.modified_count)  # 返回替换文档的数量
```



#### 查询文档

```python
import pymongo
from urllib.parse import quote_plus

if __name__ == '__main__':
    # 连接数据库
    username = quote_plus("root")
    password = quote_plus("123456")
    database = quote_plus("admin")
    mongo = pymongo.MongoClient(f"mongodb://{username}:{password}@127.0.0.1:27017/{database}")
    # 切换或新建数据库
    db = mongo["test"]
    # 切换或新建数据集
    users = db["users"]

    """添加文档"""
    # # 添加一个文档
    # document = {"name": "xiaoming", "mobile": "13012345678", "age": 16}
    # ret = users.insert_one(document)
    # print(ret.inserted_id)  # 返回新增文档的主键ID
    #
    #
    # # 添加多个文档
    # document_list = [
    #     {"name": "xiaoming", "mobile": "13033345678", "age": 17},
    #     {"name": "xiaohong", "mobile": "13044345678", "age": 18},
    #     {"name": "xiaohei", "mobile": "13612345678", "age": 18},
    # ]
    # ret = users.insert_many(document_list)
    # print(ret.inserted_ids)  # 返回新增文档的主键ID列表


    """删除文档"""
    # # 删除一篇文档
    # filter = {"name":"xiaoming"}
    # ret = users.delete_one(filter)
    # print(ret.deleted_count) # 返回删除文档的数量
    #
    # # 删除多篇文档
    # filter = {"name": "xiaohong"}
    # ret = users.delete_many(filter)
    # print(ret.deleted_count) # 返回删除文档的数量

    # # 按指定条件删除多个文档
    # filter = {"age": {"$gte": 17}}  # age >= 17
    # ret = users.delete_many(filter)
    # print(ret.deleted_count)  # 返回删除文档的数量


    """更新文档"""
    # # 更新一个文档
    # filter = {"name": "xiaoming"}
    # update = {"$set": {"name": "xiaohong"}, "$inc": {"age": -3}}
    # ret = users.update_one(filter=filter, update=update)
    # print(ret.modified_count)  # 返回更新文档的数量

    # # 更新多个文档
    # filter = {"name": "xiaohong"}
    # update = {"$set": {"sex": True}}
    # ret = users.update_many(filter=filter, update=update)
    # print(ret.modified_count)  # 返回更新文档的数量

    # # 把满足条件的一个文档进行替换
    # filter = {"name": "xiaoming"}
    # replace = {"name": "xiaolan", "age": 16, "sex": False} # 因为是直接替换文档，所以不需要指定更新运算符
    # ret = users.replace_one(filter, replace)
    # print(ret.modified_count)  # 返回替换文档的数量


    """查询文档"""
    # # 获取整个集合所有的文档数据
    # orders = db["orders"]
    # ducument_list = orders.find()
    # for document in ducument_list:
    #     print(document)

    # # 获取集合中第一个文档
    # orders = db["orders"]
    # document = orders.find_one()
    # print(document)
    # print(document.get("order_number"))  # 获取文档中的任意数据
    # print(document.get("items"))  # 获取文档中的任意数据
    # print(document["items"][0])  # 获取文档中的任意数据
    # print(document["items"][0]["price"])  # 获取文档中的任意数据

    # # 投影显示字段
    # document = users.find_one({}, {"_id": 0})
    # print(document)
    #
    # document = users.find_one({}, {"_id": 0, "name": 1, "age": 1})
    # print(document)


    # 按条件查询多条数据
    # filter = {"age": 18}
    # document_list = users.find(filter)
    # for document in document_list:
    #     print(document)

    # # 比较运算符
    # filter = {"age": {"$gt":17}}
    # document_list = users.find(filter)
    # for document in document_list:
    #     print(document)


    # # 结果排序，单字段排序
    # filter = {"age": {"$lt": 32}}
    # #  pymongo.ASCENDING 就是 -1 ，表示升序， 从小到大
    # #  pymongo.DESCENDING 就是 1 ，表示降序， 从大到小
    # document_list = users.find(filter).sort("age", pymongo.DESCENDING)
    # print(list(document_list))

    # # 结果排序，多字段排序
    # filter = {"age": {"$lte": 34}}
    # order = [("age", pymongo.DESCENDING), ("_id", pymongo.ASCENDING)]
    # document_list = users.find(filter).sort(order)
    # print(list(document_list))


    # # 限制查询结果数量
    # document_list = users.find().limit(3)
    # print(list(document_list))

    # # 偏移、跳过
    # #	skip(int)
    # document_list = users.find().limit(3).skip(3)  # 从第3篇文档开始获取3篇文档
    # print(list(document_list))

    # # 自定义条件函数
    # document_list = users.find({"$where": "this.age==18"})
    # print(list(document_list))

    ret = db.command("buildinfo")
    print(ret)
```



# mongodb进阶

mongodb集群有三种模式，主从模式，副本集模式、sharding分片集模式。主从模式官网也不再推荐上生产环境，主要是安全性太低。副本集和sharding分片集模式目前使用的最广的方案，通常这2种方案的选择通过数据量和并发数来权衡。在GB级别的基本上副本集方案可满足，TB级别或以上采用sharding分片集模式，解决单机容量和单机并发能力。这两种既有自己的优势也有自己的缺点，比如sharding分片集模式分片越多，性能自然下降越多。



## 副本集

也叫复制集，本质上来说就是一种具有监控能力的主从模式，类似redis中的哨兵主从集群。

一组Mongodb复制集，就是一组mongod进程，这些进程维护同一个数据集合。复制集提供了数据冗余和高等级的可靠性，这是生产部署的基础。说白了，就是高级主从。

保证数据在生产部署时的冗余和可靠性，通过在不同的机器上保存副本来保证数据的不会因为单点损坏而丢失。能够随时应对数据丢失、机器损坏带来的风险。



### 复制集的基本架构

+   副本集：一个副本集就是一组MongoDB实例组成的集群，由一个主（Primary）服务器和多个备份（Secondary）服务器构成
+   主节点（primary）：主节点接收所有**写入操作**。主节点将对其数据集所做的所有更改记录到其 oplog日志。
+   副节点（secondary）：复制主节点的 oplog日志 并将操作应用到其数据集，如果主节点不可用，一个合格的副节点将被**选举**为新的主节点。
+   仲裁节点（arbiter）：负载选举，当主节点不可用，它将从副节点中选一个作为主节点。



复制集的基本架构由3台服务器组成，有2种组成模式：

+   三成员的复制集，有3个主从节点(1主2从)

+   两成员的复制集，有2个主从节点，1个仲裁节点(arbiter)。（1主1从1仲裁）

#### 不存在arbiter节点

>   一个主节点；
>
>   两个从节点组成，主节点宕机时，这两个从节点都可以经过primary选举以后被选为主节点。


![img](assets/1190037-20180106145148128-1854811460.png)

​    当主库宕机后,两个从库都会进行竞选，其中一个变为主库，当原主库恢复后，作为从库加入当前的复制集群即可。

![img](assets/1190037-20180106145154284-397901575.png) 



#### 存在arbiter节点

在三个成员的复制集中，有两个正常的主从节点和一个arbiter节点：

>     一个主节点
>
>     一个从节点，可以在选举中成为主库
>
>     一个仲裁节点，在选举中，只进行投票，不能成为主库

![img](assets/1190037-20180106145207237-1647029849.png) 

说明：由于arbiter节点没有复制数据，因此这个架构中仅提供一个完整的数据副本。arbiter节点只需要更少的资源，代价是更有限的冗余和容错。

当主库宕机时，将会选择从库成为主，主库修复后，将其加入到现有的复制集群中即可。

![img](assets/1190037-20180106145221393-1674631191.png) 



### Primary选举

　　复制集通过replSetInitiate命令（或mongo shell的rs.initiate()）进行初始化，初始化后各个成员间开始发送心跳消息，并发起Priamry选举操作，获得『大多数 总服务器-仲裁节点/ 2 > 50%』成员投票支持的节点，会成为Primary，其余节点成为Secondary。

**『大多数』的定义**

　　假设复制集内投票成员数量为N，则大多数为 N/2 + 1，当复制集内存活成员数量不足大多数时，整个复制集将无法选举出Primary，复制集将无法提供写服务，处于只读状态。

| **投票成员数** | **大多数** | **容忍失效数** |
| -------------- | ---------- | -------------- |
| **1**          | 1          | 0              |
| **2**          | 2          | 0              |
| **3**          | 2          | 1              |
| **4**          | 3          | 1              |
| **5**          | 3          | 2              |
| **6**          | 4          | 2              |
| **7**          | 4          | 3              |

　　通常建议将复制集成员数量设置为**奇数**，从上表可以看出3个节点和4个节点的复制集都只能容忍1个节点失效，从『服务可用性』的角度看，其效果是一样的。（但无疑4个节点能提供更可靠的数据存储）

### docker-compose搭建MongoDB复制集

keyfile是mongodb副本集的实例之间的权限认证，复制集要求每一个服务器下的keyfile内容必须相同。内容不同，那么该实例添加到副本集的时候，会出现不可达的状态。同时对于keyfile文件还要求如下：

+   keyfile文件的权限必须是600/400；
+   keyfile文件的内容必须在各个服务器下完全相同。

生成keyfile秘钥文件命令如下，但是因为在windows下容易出现权限问题，所以我们可以基于系统镜像创建Dockerfile构建自定义镜像，并在Dockerfile中编写生成keyfile文件的命令和设置权限的命令。

756就是秘钥长度，最好3的倍数。

```bash
openssl rand -base64 756 > data/conf/mongodb.key
chmod 600 data/conf/mongodb.key
```

Dockerfile，内容：

```dockerfile
FROM mongo:4.4.11

RUN mkdir -p /data/conf \
  && openssl rand -base64 756 > /data/conf/mongodb.key \
  && chown mongodb:mongodb /data/conf/mongodb.key \
  && chmod 400 /data/conf/mongodb.key
```

编译镜像，如下;

```bash
docker build -t mongo-replica-set .
```

docker-compose.yml，代码：

```yaml
version: '3.7'

services:
  # 主节点
  master:
    image: mongo-replica-set
    restart: always
    privileged: true
    container_name: master
    ports:
      - 27017:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: 123
    command: --replSet replica-set --keyFile /data/conf/mongodb.key
    volumes:
      - ./data/mongo/d1:/data/db
  # 副节点
  secondary:
    image: mongo-replica-set
    restart: always
    privileged: true
    container_name: secondary
    ports:
      - 27018:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: 123
    command: --replSet replica-set --keyFile /data/conf/mongodb.key
    volumes:
      - ./data/mongo/d2:/data/db
  # 仲裁节点
  arbiter:
    image: mongo-replica-set
    restart: always
    privileged: true
    container_name: arbiter
    ports:
      - 27019:27017
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: 123
    command: --replSet replica-set --keyFile /data/conf/mongodb.key
    volumes:
      - ./data/mongo/d3:/data/db

networks:
  # 默认使用自己创建的网络
  default:

```



#### 复制集初始化配置

```bash
docker-compose -mongo docker-compose.yml up -d

# 选择一个容器进行配置
docker exec -it master /bin/bash

# 配置时需要在admin数据库中
mongo
use admin

# 验证权限
db.auth('root','123')
# 验证通过后，则可以执行副本集的初始化操作initiate()，设置当前mongodb为primary节点
rs.initiate({
	"_id" : "replica-set",
	"members" : [
		{
			"_id" : 0,
			"host" : "master:27017"
		},
		{
			"_id" : 1,
			"host" : "secondary:27017"
		},
		{
			"_id" : 2,
			"host" : "arbiter:27017"
		}
	]
})


# 最后，SECONDARY节点默认是不可读写的，所以要进入从节点，执行如下操作：
docker exec -it secondary /bin/bash
mongo
rs.secondaryOk()

docker exec -it arbiter /bin/bash
mongo
rs.slaveOk()
```



## 分片集

当数据量比较大的时候，我们需要把数据分片保存并运行在不同的服务器中，以降低CPU、内存和IO的压力，Sharding分片集就是mongo数据库用于横向扩容的技术。

分片是数据跨多台机器存储，MongoDB使用分片来支持具有非常大的数据集和高吞吐量操作的部署。MongoDB分片技术类似MySQL的水平切分和垂直切分，mongo数据库实现Shardin分片集主要有两种方式：垂直扩展和横向切分（也叫水平扩展）。

-   垂直扩展的方式就是进行计算机资源扩容，添加更多的CPU，内存，磁盘空间等。

-   水平扩展则是通过数据分片的方式将数据集分布在多个服务器上。，通过集群统一提供服务。

### 分片设计思想

分片为应对高吞吐量与大数据量提供了方法。使用分片减少了每个分片需要处理的请求数，因此通过水平扩展，集群可以提高自己的存储容量和吞吐量。举例来说，当插入一条数据时，项目应用只需要访问存储这条数据的分片.

使用分片减少了每个分片存储的数据。例如如果数据库1tb的数据集，并有4个分片，然后每个分片可能仅持有256 GB的数据。如果有40个分片，那么每个切分可能只有25GB的数据。

![img](assets/13587608-58483213c588ee8f.png)

### 分片机制的优势

**1.对集群进行抽象，让集群“不可见”**

MongoDB自带了一个叫做mongos的专有路由进程。mongos就是掌握统一路口的路由器，其会将客户端发来的请求准确无误的路由到集群中的一个或者一组服务器上，同时会把接收到的响应拼装起来发回到客户端。

**2.保证集群总是可读写**

MongoDB通过多种途径来确保集群的可用性和可靠性。将MongoDB的分片和复制功能结合使用，在确保数据分片到多台服务器的同时，也确保了每分数据都有相应的备份，这样就可以确保有服务器换掉时，其他的从库可以立即接替坏掉的部分继续工作。

**3.*使集群易于扩展**

当系统需要更多的空间和资源的时候，MongoDB使我们可以按需方便的扩充系统容量。



### 分片集群架构

| 组件          | 说明                                                         |
| ------------- | ------------------------------------------------------------ |
| Config Server | 配置服务器，是mongod实例，可以理解为真实数据的元数据，存储了集群的所有节点、分片数据路由等信息。默认需要配置3个Config Server节点。Config Server中存储的信息：所有存取数据的方式，所有shard节点的信息，分片功能的一些配置信息。 |
| Mongos        | 数据路由，作为与客户端打交道的模块，提供对外应用访问，所有操作均通过mongos执行。一般有多个mongos节点。数据迁移和数据自动平衡。Mongos本身并不持久化数据，Sharded cluster所有的元数据都会存储到Config Server，而用户的数据会议分散存储到各个shard。Mongos启动后，会从配置服务器加载元数据，开始提供服务，将用户的请求正确路由到对应的碎片。 |
| Mongod        | 真正的数据存储位置，存储应用数据记录。一般有多个Mongod节点，以chunk为单位存数据，达到数据分片目的。 |

![分片集群架构](assets/13587608-9f139e94370a15c8.png)

**Mongos的路由功能**

当数据写入时，MongoDB Cluster根据**分片键**设计写入数据。

当外部语句发起数据查询时，MongoDB根据数据分布自动路由至指定节点返回数据。



### 分片集群中的数据分布

（1）使用chunk（数据块）来把数据存储不同的分片（shard）

（2）集群搭建完成之后，默认开启一个chunk，大小是64M，chunk的大小容量可以通过配置chunksize修改。

（3）存储数据的容量只要超过64M，chunk会进行平均分裂，如果单位时间存储需求很大，设置更大的chunk

（4）chunk会被自动均衡迁移到各个Shard分片节点下面。

#### Chunk（数据库）是什么

就是一个存储数据的单位，是为了方便分割(分裂)数据和迁移数据的。在一个shard server内部，MongoDB还是会把数据分为chunks，每个chunk代表这个shard server内部一部分数据。chunk的产生，会有以下两个用途：

Splitting（切割）：当一个chunk的大小超过配置中的chunk size时，MongoDB的后台进程会把这个chunk切分成更小的chunk，从而避免chunk过大的情况

Balancing(迁移)：在MongoDB中，balancer是一个后台进程，负责chunk(数据块)的迁移，从而均衡各个shard server的负载，系统初始化时默认只有1个chunk，chunk size默认值64M，生产环境中根据业务选择合适的chunk size是最好的。mongoDB会自动拆分和迁移chunks。



#### Chunksize的选择

适合项目业务的chunksize是最好的。

chunk的分裂和迁移非常消耗IO资源；chunk分裂的时机：在插入和更新，读数据不会分裂。

小的chunksize：数据均衡是迁移速度快，数据分布更均匀。数据分裂频繁，路由节点消耗更多资源。

大的chunksize：数据分裂少。数据块迁移的时候就会比较集中消耗IO资源。

chunksize的值通过如果没有特殊的要求，可以设置为通常100-200M。

#### Chunk分裂及迁移

　　随着数据的增长，其中的数据大小超过了配置的chunksize，默认是64M，则这个chunk就会分裂成两个。数据的增长会让chunk分裂得越来越多。

 ![img](assets/1190037-20180106150630018-1017846225.png)

　　这时候，各个shard 上的chunk数量就会不平衡。这时候，mongos中的一个组件balancer 就会执行自动平衡。把chunk从chunk数量最多的shard节点挪动到数量最少的节点。

![img](assets/1190037-20180106150636096-1641567859.png) 

**chunkSize** **对分裂及迁移的影响**

　　MongoDB 默认的 chunkSize 为64MB，如无特殊需求，建议保持默认值或者100~200M左右；chunkSize 会直接影响到 chunk（数据块） 分裂、迁移的行为。

　　chunkSize 越小，chunk 分裂及迁移越多，数据分布越均衡；反之，chunkSize 越大，chunk 分裂及迁移会更少，但可能导致数据分布不均。

　　chunkSize 太小，容易出现 jumbo chunk（即分片键shardKey的某个取值出现频率很高，这些文档只能放到一个 chunk 里，无法再分裂）而无法迁移；chunkSize 越大，则可能出现 chunk 内文档数太多（chunk 内文档数不能超过 250000 ）而无法迁移。

　　chunk 自动分裂只会在数据写入时触发，所以如果将 chunkSize 改小，系统需要一定的时间来将 chunk 分裂到指定的大小。

　　**chunk 只会分裂，不会合并**，所以即使将 chunkSize 改大，现有的 chunk 数量不会减少，但 chunk 大小会随着写入不断增长，直到达到目标大小。



### 数据分片

#### 分片键

MongoDB中**数据的分片是以集合为基本单位的**，集合中的数据通过片键（Shard key）被分成多部分。其实分片键就是在集合中选一个键（字段），用该键的值作为数据拆分的依据。

所以一个好的分片键对分片至关重要。分片键必须是一个索引，通过sh.shardCollection加会自动创建索引（前提是此集合不存在相同索引的情况下）。一个自增的分片键对写入和数据均匀分布就不是很好，因为自增的分片键总会在一个分片上写入，后续达到某个阀值可能会写到别的分片。但是按照分片键查询会非常高效。

随机分片键对数据的均匀分布效果很好。注意尽量避免在多个分片上进行查询。在所有分片上查询，mongos会对结果进行归并排序。

对集合进行分片时，你需要选择一个分片键，**分片键是每条记录都必须包含的，且建立了索引的单个字段或复合字段**，MongoDB按照分片键将数据划分到不同的数据块(chunk)中，并将数据块(chunk)均衡地分布到所有分片节点中。

为了按照分片键划分数据块，MongoDB使用**基于范围**或者 **基于哈希**的分片方式。

**注意：**

-   分片键是不可变。

-   分片键必须有索引。

-   分片键大小限制512bytes。

-   分片键用于分片集中的路由查询(mongos)。

-   MongoDB不接受已进行collection级分片的collection上插入无分片

-   键的文档（也不支持空值插入）

#### 基于范围的分片

Sharded Cluster支持将单个集合的数据分散存储在多shard上，用户可以指定根据集合内文档的某个字段即shard key来进行范围分片（range sharding）。

#### 基于哈希的分片

对于基于哈希的分片，MongoDB计算一个字段的哈希值，并用这个哈希值来创建数据块。在使用基于哈希分片的系统中，拥有”相近”片键的文档很可能不会存储在同一个数据块中，因此数据的分离性更好一些。



**Hash分片与范围分片互补**，能将文档随机的分散到各个chunk，充分的扩展写能力，弥补了范围分片的不足，但不能高效的服务范围查询，所有的范围查询要分发到后端所有的Shard才能找出满足条件的文档。



### docker-compose搭建分片集集群

```bash
docker network create mongo
```

mongo-compose.yaml，代码：

```yaml
version: '3.7'
services:
  shard1:
    image: mongo:4.4.11
    container_name: mongo_shard1
    # --shardsvr: 这个参数仅仅只是将默认的27017端口改为27018,如果指定--port参数，可用不需要这个参数
    # --directoryperdb：每个数据库使用单独的文件夹
    command: mongod --shardsvr --directoryperdb --replSet shard1
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/shard1:/data/db
    privileged: true
    mem_limit: 16000000000
    networks:
      - mongo   

  shard2:
    image: mongo:4.4.11
    container_name: mongo_shard2
    command: mongod --shardsvr --directoryperdb --replSet shard2
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/shard2:/data/db
    privileged: true
    mem_limit: 16000000000
    networks:
      - mongo

  shard3:
    image: mongo:4.4.11
    container_name: mongo_shard3
    command: mongod --shardsvr --directoryperdb --replSet shard3
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/shard3:/data/db
    privileged: true
    mem_limit: 16000000000
    networks:
      - mongo

  config1:
    image: mongo:4.4.11
    container_name: mongo_config1
    # --configsvr: 这个参数仅仅是将默认端口由27017改为27019, 如果指定--port可不添加该参数
    command: mongod --configsvr --directoryperdb --replSet fates-mongo-config --smallfiles
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/config1:/data/configdb
    networks:
      - mongo

  config2:
    image: mongo:4.4.11
    container_name: mongo_config2
    command: mongod --configsvr --directoryperdb --replSet fates-mongo-config --smallfiles
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/config2:/data/configdb
    networks:
      - mongo

  config3:
    image: mongo:4.4.11
    container_name: mongo_config3
    command: mongod --configsvr --directoryperdb --replSet fates-mongo-config --smallfiles
    volumes:
      - ./data/mongo/localtime:/etc/localtime
      - ./data/mongo/config3:/data/configdb
    networks:
      - mongo

  mongos:
    image: mongo:4.4.11
    container_name: mongo_mongos
    # mongo3.6版默认绑定IP为127.0.0.1，此处绑定0.0.0.0是允许其他容器或主机可以访问
    command: mongos --configdb fates-mongo-config/config1:27019,config2:27019,config3:27019 --bind_ip 0.0.0.0 --port 27017
    ports:
     - 27017:27017
    volumes:
      - ./data/mongo/localtime:/etc/localtime
    depends_on:
      - config1
      - config2
      - config3
    networks:
      - mongo
networks:
  mongo:
    external: true
```

run.sh，代码：

```bash
#!/bin/sh
# docker-compose启动mongodb分片容器组服务
docker-compose -f mongo-compose.yaml up -d

# 睡眠半分钟，等待mongodb所有容器起来之后将它们配置加入分片
sleep 30s

# 操作config1，配置config副本集，将config容器组作为config角色,此时config1作为config副本集里的主节点
docker-compose -f mongo-compose.yaml exec config1 bash -c "echo 'rs.initiate({_id: \"mongo-config\",configsvr: true, members: [{ _id : 0, host : \"config1:27019\" },{ _id : 1, host : \"config2:27019\" }, { _id : 2, host : \"config3:27019\" }]})' | mongo --port 27019"

# 操作shard1、shard2、shard3，将shard容器组作为shard角色。
docker-compose -f mongo-compose.yaml exec shard1 bash -c "echo 'rs.initiate({_id: \"shard1\",members: [{ _id : 0, host : \"shard1:27018\" }]})' | mongo --port 27018"
docker-compose -f mongo-compose.yaml exec shard2 bash -c "echo 'rs.initiate({_id: \"shard2\",members: [{ _id : 0, host : \"shard2:27018\" }]})' | mongo --port 27018"
docker-compose -f mongo-compose.yaml exec shard3 bash -c "echo 'rs.initiate({_id: \"shard3\",members: [{ _id : 0, host : \"shard3:27018\" }]})' | mongo --port 27018"

# 将shard1、shard2、shard3加入分片集群组。
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard1/shard1:27018\")' | mongo"
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard2/shard2:27018\")' | mongo"
docker-compose -f mongo-compose.yaml exec mongos bash -c "echo 'sh.addShard(\"shard3/shard3:27018\")' | mongo"
```

运行

```bash
sh run.sh
```

上面仅仅借助docker-compose实现分片集的部署机制。真正的运维环境中，Mongodb集群应该分布在不同的机器，同时，Mongodb库默认是不会将你的表进行分片的，是需要手动配置的，如果不配置，数据都会全部存放在主节点，不会均匀分配到各个分片。

举例：

```javascript
// 注意：分片的片键必须是索引

// 先让当前库支持分片，school是举例数据库，可以填写实际要分片的库名。
sh.enableSharding("school")


// 把当前集合加入分片，递增片键(timestamp已经作为索引了)，student表示要分片的集合，可以填写实际要分片的集合名称。
sh.shardCollection('school.student',{timestamp:1})

// 刷新路由
db.adminCommand("flushRouterConfig")

// 让当前分片支持均衡调度， 当某个shard中的chunk达到一定的数量，则balancer会自动的将部分chunk块迁移到其它shard中，保证所有的shard中拥有的 chunk 块数量基本一致。
sh.enableBalancing("school.student")

// 开启均衡调度
sh.startBalancer()

// 查看详细分片信息
sh.status({"verbose":1})

// 查看该表的分片数据信息
db.student.getShardDistribution()
```
