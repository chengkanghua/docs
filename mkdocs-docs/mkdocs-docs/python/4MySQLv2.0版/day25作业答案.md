## day25 作业答案

1. 根据要求 创建表 结构并编写相应的SQL语句（基于MySQL自带客户端操作）

   | 列名     | 类型          | 备注                                           |
   | -------- | ------------- | ---------------------------------------------- |
   | id       | int           | 不为空 & 自增 & 主键                           |
   | name     | varchar(32)   | 不为空                                         |
   | password | varchar(64)   | 不为空                                         |
   | gender   | char(1)       | 不为空，支持：男、女                           |
   | email    | varchar(64)   | 可以为空                                       |
   | amount   | decimal(10,2) | 不为空 & 默认值为 0                            |
   | ctime    | datetime      | 新增时的时间<br />提示：可基于datetime模块实现 |

   - 根据上述表的要求创建相应的数据和表结构（注意编码）。

     ```sql
     create table admin(
     	id int not null auto_increment primary key,	-- 不允许为空 & 主键 & 自增
         name varchar(32) not null,
         password varchar(64) not null,
         gender char(1) not null,
         email varchar(64) null,
         amount decimal(10,2) not null default 0,
         ctime datetime
     )default charset=utf8;
     ```

   - 任意插入5条数据。

     ```sql
     insert into admin(name,password,gender,email,amount,ctime) values("武沛齐","123123","男","xxx@live.com",19991.12,NOW());
     insert into admin(name,password,gender,email,amount,ctime) values("alex","sb","男","alex@live.com",991.12,NOW());
     insert into admin(name,password,gender,email,amount,ctime) values("eric","8888","女","eric@live.com",991.12,NOW());
     
     insert into admin(name,password,gender,email,amount,ctime) values("tony","123123123","女","xxxxxxxx@live.com",200.12,NOW()), ("kelly","8888","女","kelly@live.com",991.12,NOW());
     ```

   - 将 `id>3`的所有人的性别改为  男。

     ```sql
     update admin set gender="男" where id >3;
     ```

   - 查询余额 `amount>1000`的所有用户。

     ```sql
     select * from admin where amount >1000;
     ```

   - 让每个人的余额在自己原的基础上 +1000 。

     ```sql
     update admin set amount=amount+1000;
     ```

   - 删除性别为男的所有数据。

     ```sql
      delete from admin where gender="男";
     ```

   - 通过Python代码实现上述除了第一个以外的操作。

     ```
     插入5条数据时，ctime那一列不要自己写“2021-11-11.。。” 而是使用datatime模块生成当前时间。
     ```

     - 插入5条数据。

       ```python
       import datetime
       import pymysql
       
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
       
       
       # 单独增加数据
       sql = 'insert into admin(name,password,gender,email,amount,ctime) values(%s,%s,%s,%s,%s,NOW());'
       cursor.execute(sql, ["武沛齐", "123123", "男", "xxx@live.com", 19991.12])
       conn.commit()
       
       # 单独增加数据
       sql = 'insert into admin(name,password,gender,email,amount,ctime) values(%s,%s,%s,%s,%s,%s);'
       cursor.execute(sql, ["武沛齐", "123123", "男", "xxx@live.com", 19991.12, datetime.datetime.now()])
       conn.commit()
       
       # 多条批量增加
       sql = 'insert into admin(name,password,gender,email,amount,ctime) values(%s,%s,%s,%s,%s,%s);'
       cursor.executemany(sql, [
           ["武沛齐", "123123", "男", "xxx@live.com", 19991.12, datetime.datetime.now()],
           ["alex", "sb", "男", "alex@live.com", 991.12, datetime.datetime.now()],
           ["eric", "8888", "女", "eric@live.com", 991.12, datetime.datetime.now()],
           ["tony", "123123123", "女", "xxxxxxxx@live.com", 200.12, datetime.datetime.now()],
           ["kelly", "8888", "女", "kelly@live.com", 991.12, datetime.datetime.now()],
       ])
       conn.commit()
       
       # 关闭数据库连接
       cursor.close()
       conn.close()
       ```

     - 将 `id>3`的所有人的性别改为  男。

       ```python
       import datetime
       import pymysql
       
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
       
       # 单独增加数据
       sql = 'update admin set gender="男" where id >3;'
       cursor.execute(sql)
       conn.commit()
       
       
       # 关闭数据库连接
       cursor.close()
       conn.close()
       
       ```

     - 查询余额 `amount>1000`的所有用户。

       ```python
       import datetime
       import pymysql
       
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
       
       # 单独增加数据
       sql = 'select * from admin where amount >1000;'
       cursor.execute(sql)
       result = cursor.fetchall()
       print(result)
       
       # 关闭数据库连接
       cursor.close()
       conn.close()
       ```

     - 让每个人的余额在自己原的基础上 +1000 。

       ```python
       import datetime
       import pymysql
       
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
       
       # 单独增加数据
       sql = 'update admin set amount=amount+1000;'
       cursor.execute(sql)
       conn.commit()
       
       # 关闭数据库连接
       cursor.close()
       conn.close()
       
       ```

     - 删除性别为男的所有数据。

       ```python
       import datetime
       import pymysql
       
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
       
       # 单独增加数据
       sql = 'delete from admin where gender="男";'
       cursor.execute(sql)
       conn.commit()
       
       # 关闭数据库连接
       cursor.close()
       conn.close()
       ```

     

2. 编写脚本实现将 csv 文件的内容录入到 MySQL 数据库中。
   要求：自己创建一个自增列作为主键（不要用csv文件中的第一列作为主键）。

   ```
   1715046,河北大学取消考试学生紧急离校,老师:回不了家的到老师家过年,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715046-15562045_adpkg-ad_hd.mp4
   1715020,重庆两口子因琐事吵架，男子怒将自家车推进涪江,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715020-15561817_adpkg-ad_hd.mp4
   1715031,成都九峰山因雪景引游客暴增，致垃圾遍地野猴觅食,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715031-15561980_adpkg-ad_hd.mp4
   1715014,女子子宫摘除32年后CT报告称未见异常，医生：贴的模版忘删了,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715014-15561686_adpkg-ad_hd.mp4
   1715025,监控画面曝光！甘肃天水一公交车与救护车相撞后坠桥,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715025-15561875_adpkg-ad_hd.mp4
   1715010,男子称退伍后发现被贷款100万：征信逾期数十次，非自己签名,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715010-15561845_adpkg-ad_hd.mp4
   1715007,东北老交警零下43度执勤落下老寒腿:穿2斤重棉裤,已习以为常,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715007-15561958_adpkg-ad_hd.mp4
   1715011,女教师公寓熟睡被同事弟弟连砍数刀：全身刀疤，不敢告诉父母,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715011-15561664_adpkg-ad_hd.mp4
   1714970,网曝江西一村庄现两千平违建，房主回应：建给村里当文化中心,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714970-15561752_adpkg-ad_hd.mp4
   1715006,河南一新建足球场内惊现坟墓，官方：会尽快迁坟,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715006-15561679_adpkg-ad_hd.mp4
   1715009,老师收到毕业24年学生送的定制台历：他高考失利，我开导过,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715009-15561658_adpkg-ad_hd.mp4
   1715000,尚德机构回应未兑现宝马奖励：名单仍在确认中，会负责到底,https://video.pearvideo.com/mp4/adshort/20210105/cont-1715000-15561545_adpkg-ad_hd.mp4
   1714993,沈阳重点管控区日常产90吨生活垃圾，重点疫点垃圾由专人运走,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714993-15561434_adpkg-ad_hd.mp4
   1714995,消费者称遭移动外呼10088套路换套餐，客服致歉：口径有问题,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714995-1427-174135_adpkg-ad_hd.mp4
   1714979,泪流满面！武警相隔两千公里与妻子隔屏举行婚礼,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714979-15561542_adpkg-ad_hd.mp4
   1714992,村民结婚两男子拄拐上门要钱：给少了不走，反问"咋拿得出手",https://video.pearvideo.com/mp4/adshort/20210105/cont-1714992-15561429_adpkg-ad_hd.mp4
   1714457,36年嫌疑人：儿女被骂“杀人犯的孩子”，不想把骂名带进棺材,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714457-1491-170515_adpkg-ad_hd.mp4
   1714981,男子偷手机被发现挣脱失主逃跑，执勤辅警狂追八百米擒获,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714981-99-172939_adpkg-ad_hd.mp4
   1714977,八旬老太捡拾垃圾成瘾，堆满楼道院子漫进邻居家,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714977-15561306_adpkg-ad_hd.mp4
   1714972,昆明一楼盘消防喷淋离地仅2米1，业主吐槽：直接当喷头用,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714972-15561247_adpkg-ad_hd.mp4
   1714973,居民家浓烟弥漫邻居敲门不应，民警赶来一看是屋主在熏腊肉,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714973-15561249_adpkg-ad_hd.mp4
   1714966,石家庄有超市停业，学校紧急放假，学生：下午考试被临时取消,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714966-15561248_adpkg-ad_hd.mp4
   1714902,杭州地铁7号线施工大揭秘：940天完成近40公里地铁线,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714902-15561394_adpkg-ad_hd.mp4
   1714928,沈阳已设置重点管控区域，大连志愿者挨家挨户配送生活物资,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714928-15561018_adpkg-ad_hd.mp4
   1714950,女孩考第一溺亡双胞胎姐姐不吃不喝，家属诉求：给予心理疏导,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714950-15561100_adpkg-ad_hd.mp4
   1714924,70万1针特效药降价，2岁患儿母亲哽咽：会拼全力救孩子,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714924-58-162201_adpkg-ad_hd.mp4
   1714930,贵州大叔嫁女陪嫁28万现金和一套房：儿子结婚只花了十几万,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714930-15561017_adpkg-ad_hd.mp4
   1714927,张家口云顶滑雪场通报一滑雪者摔倒身亡：警方已介入,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714927-15560963_adpkg-ad_hd.mp4
   1714926,邢台全面进入战时状态，小区进出需要健康码,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714926-15560829_adpkg-ad_hd.mp4
   1714918,石家庄多个小区采取封闭管理：发现阳性检测者，全员核酸检测,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714918-15560835_adpkg-ad_hd.mp4
   1714693,兰大女生当兵2年后重返校园：学会自律，珍惜在校时光,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714693-15560791_adpkg-ad_hd.mp4
   1714920,猴哥尝到投喂甜头赖老太家不走，逗鸡毁菜气到村民报警,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714920-15560793_adpkg-ad_hd.mp4
   1714916,沈阳确诊出车司机搭载的抚顺3名乘客全部找到，核酸均为阴性,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714916-15560758_adpkg-ad_hd.mp4
   1714894,轿车被48米建筑垃圾围堵三个月，车主无法用车叫苦不迭,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714894-15560731_adpkg-ad_hd.mp4
   1714861,考第一被质疑后溺亡女孩同学：她自尊心强，曾说被怀疑作弊,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714861-15560701_adpkg-ad_hd.mp4
   1714886,东北汉子冲进火场救人被熏成黑脸：差几秒，我就倒在里面了,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714886-15560659_adpkg-ad_hd.mp4
   1714908,探访石家庄疫情高风险地区：部分村庄封村，外村人一律不让进,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714908-15560638_adpkg-ad_hd.mp4
   1714906,“北京时间”产生于西安，科学家解读选址考量因素,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714906-15560549_adpkg-ad_hd.mp4
   1714907,16人聚餐吃了800元无人结账，老板询问反遭怼：多大点事儿,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714907-15560637_adpkg-ad_hd.mp4
   1714892,重庆一地铁站出口建在坡顶，居民：期待未来的变化,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714892-15560550_adpkg-ad_hd.mp4
   1714900,河北南宫一小区发现高度疑似密接人员，小区全面封闭只进不出,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714900-15560548_adpkg-ad_hd.mp4
   1714901,杭州运河边8平米小书摊开了13年，店主兼职拉货补贴,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714901-15560544_adpkg-ad_hd.mp4
   1714877,河南商丘鹦鹉卖家被追刑责，养殖户：不敢卖不敢放，放也犯法,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714877-15560499_adpkg-ad_hd.mp4
   1714895,石家庄小果庄村1天增加8例确诊病例，为全国唯一高风险地区,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714895-15560459_adpkg-ad_hd.mp4
   1714801,48岁女教师重新高考学法律：直接进入老年生活是种损失,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714801-15560352_adpkg-ad_hd.mp4
   1714873,不认失散聋哑儿夫妻已接走儿子，养父：两验DNA，归属没说清,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714873-15560356_adpkg-ad_hd.mp4
   1714846,7岁男童煤气中毒脑死亡，父母含泪为其捐器官救同龄人,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714846-15560326_adpkg-ad_hd.mp4
   1714875,连夜出发！衡水110名护士紧急集结支援中风险地区,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714875-15560268_adpkg-ad_hd.mp4
   1713843,打满全场丨院感专家李素英回忆援鄂：90后00后医护最让我感动,https://video.pearvideo.com/mp4/adshort/20210104/cont-1713843-15559433_adpkg-ad_hd.mp4
   1714869,河北新增14例确诊30例无症状，石家庄一村庄调整为高风险地区,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714869-15560218_adpkg-ad_hd.mp4
   1714862,应急部披露襄汾饭店坍塌致29死细节：8次违规扩建，监管不严,https://video.pearvideo.com/mp4/adshort/20210105/cont-1714862-15560157_adpkg-ad_hd.mp4
   ```

   ```sql
   create table news(
   	id int not null auto_increment primary key,
       nid int not null,
       title varchar(128) not null,
       url char(128) not null
   )default charset=utf8;
   ```

   ```python
   import datetime
   import pymysql
   
   
   def insert_db(*args):
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
   
       # 单独增加数据
       sql = 'insert into news(nid,title,url) values(%s,%s,%s);'
       cursor.execute(sql, args)
       conn.commit()
   
       # 关闭数据库连接
       cursor.close()
       conn.close()
   
   
   def run():
       with open('data.csv', mode='rt', encoding='utf-8') as file_object:
           for line in file_object:
               nid, others = line.strip().split(",", maxsplit=1)
               title, url = others.rsplit(',', maxsplit=1)
               insert_db(nid, title, url)
   
   
   if __name__ == '__main__':
       run()
   
   ```

   ```python
   import datetime
   import pymysql
   
   
   def insert_db(multi_row_list):
       # 连接指定数据
       conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', charset="utf8", db="day25db")
       cursor = conn.cursor()
   
       # 单独增加数据
       sql = 'insert into news(nid,title,url) values(%s,%s,%s);'
       cursor.executemany(sql, multi_row_list)
       conn.commit()
   
       # 关闭数据库连接
       cursor.close()
       conn.close()
   
   
   def run():
       with open('data.csv', mode='rt', encoding='utf-8') as file_object:
           # 批量在数据库中插入，每次最多插入10条
           part_list = []
           for line in file_object:
               nid, others = line.strip().split(",", maxsplit=1)
               title, url = others.rsplit(',', maxsplit=1)
               part_list.append([nid, title, url])
               if len(part_list) == 10:
                   insert_db(part_list)
                   part_list.clear()
           if part_list:
               insert_db(part_list)
   
   
   if __name__ == '__main__':
       run()
   
   ```

   









