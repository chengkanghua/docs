import pymysql


class MySQL(object):
    """数据库工具类"""
    def __init__(self , config):
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.charset = config['charset'] if config.get("charset", None) else "utf8mb4"
        self.port = int(config['port'])
        self.connect = None
        self.cursor = None

        try:
            self.connect = pymysql.connect(**config)
            self.connect.autocommit(1)
            # 所有的查询，都在连接 connect 的一个模块cursor上面运行的
            self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        except:
            print("MySQL数据库连接错误, 请检查数据连接配置!")

    # 关闭数据库连接
    def close(self):
        if not self.connect:
            self.connect.close()
        else:
            pass

    def create_database(self, db_name):
        """
        创建数据库
        :param db_name: 数据库名
        :param charset: 字符集
        :return:
        """
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        self.connect.select_db(db_name)
        print(f"新建数据库: {db_name}")

    def select_database(self,db_name):
        """
        选择数据库
        :param db_name:
        :return:
        """
        self.connect.select_db(db_name)

    def get_version(self):
        """
        获取数据库版本号
        :return:
        """
        self.cursor.exec("SELECT VERSION()")
        return self.get_one()

    def exist_table(self, table_name):
        """
        判断数据表是否存在
        :param table_name: 数据表名
        :return:
        """
        sql = f"SELECT * FROM information_schema.TABLES WHERE TABLE_NAME='{table_name}';"
        result = self.executeCommit(sql)
        print(f"result={result}")
        return not not result

    def get_one(self):
        """
        获取最后一次查询的结果
        :return:
        """
        # 取得上个查询的结果，是单个结果
        data = self.cursor.fetchone()
        return data

    # 创建数据库表
    def create_table(self, table_name, attr_dict, constraint):
        """创建数据库表
            args：
                tablename  ：表名字
                attrdict   ：属性键值对,{'book_name':'varchar(200) NOT NULL'...}
                constraint ：主外键约束, PRIMARY KEY(`id`)
        """
        #　判断表是否存在
        if self.isExistTable(table_name):
            print("%s is exit" % table_name)
            return
        sql = ''
        sql_mid = '`id` bigint(11) NOT NULL AUTO_INCREMENT,'
        for attr,value in attrdict.items():
            sql_mid = sql_mid + '`'+attr + '`'+' '+ value+','
        sql = sql + 'CREATE TABLE IF NOT EXISTS %s (' % table_name
        sql = sql + sql_mid
        sql = sql + constraint
        sql = sql + ') ENGINE=InnoDB DEFAULT CHARSET=utf8'
        print('creatTable:'+sql)
        self.executeCommit(sql)

    def exec(self,sql=""):
        """
        执行sql查询语句，针对读操作返回结果集
        :param sql: 要执行的SQL语句
        :return:
        """
        try:
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return records
        except pymysql.Error as e:
            error = 'SQL语句执行有误! ERROR (%s): %s' %(e.args[0],e.args[1])
            print(error)
            return error

    def commit(self,sql=""):
        """
        执行sql更新,删除,事务等操作语句，针对失败时回滚
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except pymysql.Error as e:
            self.connect.rollback()
            error = 'SQL语句执行有误! ERROR (%s): %s' %(e.args[0],e.args[1])
            print(error)
            return error

    def insert(self, table_name, params):
        """
        添加数据
        :param table_name: 表名字
        :param params: 属性键
        :return: 属性值
        """
        fields = []
        values = []
        for key, value in params.items():
            fields.append(key)
            if isinstance(value, str):
                values.append(f"'{value}'")
            else:
                values.append(value)

        attrs_sql = f"({','.join(fields)})"
        values_sql = f" VALUES ({','.join(values)})"
        sql = f"INSERT INTO {table_name} "
        sql = sql + attrs_sql + values_sql
        print('添加数据:'+sql)
        self.commit(sql)

    def select(self, table_name, cond_dict, order='', fields='*'):
        """
        查询数据
        :param table_name: 表名字
        :param cond_dict:  查询条件
        :param order:      排序条件
        :param fields:     查询字段
        :return:
        """
        consql = " "
        if cond_dict!='':
            for k, v in cond_dict.items():
                consql = consql+'`'+k +'`'+ '=' + '"'+v + '"' + ' and'
        consql = consql + ' 1=1 '
        if fields == "*":
            sql = "SELECT * FROM {table_name} WHERE "
        else:
            if isinstance(fields, list):
                fields = ",".join(fields)
                sql = f"SELECT {fields} FROM {table_name} WHERE "
            else:
                print("查询字段必须是list格式.")
                return None

        sql = sql + consql + order
        print('查询数据:' + sql)
        return self.exec(sql)

    def insertMany(self,table_name, attrs, values):
        """插入多条数据

            args：
                tablename  ：表名字
                attrs        ：属性键
                values      ：属性值

            example：
                table='test_mysqldb'
                key = ["id" ,"name", "age"]
                value = [[101, "liuqiao", "25"], [102,"liuqiao1", "26"], [103 ,"liuqiao2", "27"], [104 ,"liuqiao3", "28"]]
                mydb.insertMany(table, key, value)
        """
        values_sql = ['%s' for v in attrs]
        attrs_sql = '('+','.join(attrs)+')'
        values_sql = ' values('+','.join(values_sql)+')'
        sql = 'insert into %s'% table_name
        sql = sql + attrs_sql + values_sql
        print('insertMany:'+sql)
        try:
            print(sql)
            for i in range(0,len(values),20000):
                    self.cursor.executemany(sql,values[i:i+20000])
                    self.connect.commit()
        except pymysql.Error as e:
            self.connect.rollback()
            error = 'insertMany executemany failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print(error)

    def delete(self, tablename, cond_dict):
        """删除数据

            args：
                tablename  ：表名字
                cond_dict  ：删除条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                mydb.delete(table, params)

        """
        consql = ' '
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + tablename + "." + k + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "DELETE FROM %s where%s" % (tablename, consql)
        print(sql)
        return self.executeCommit(sql)

    def update(self, tablename, attrs_dict, cond_dict):
        """更新数据

            args：
                tablename  ：表名字
                attrs_dict  ：更新属性键值对字典
                cond_dict  ：更新条件字典

            example：
                params = {"name" : "caixinglong", "age" : "38"}
                cond_dict = {"name" : "liuqiao", "age" : "18"}
                mydb.update(table, params, cond_dict)

        """
        attrs_list = []
        consql = ' '
        for tmpkey, tmpvalue in attrs_dict.items():
            attrs_list.append("`" + tmpkey + "`" + "=" +"\'" + tmpvalue + "\'")
        attrs_sql = ",".join(attrs_list)
        print("attrs_sql:", attrs_sql)
        if cond_dict!='':
            for k, v in cond_dict.items():
                if isinstance(v, str):
                    v = "\'" + v + "\'"
                consql = consql + "`" + tablename +"`." + "`" + k + "`" + '=' + v + ' and '
        consql = consql + ' 1=1 '
        sql = "UPDATE %s SET %s where%s" % (tablename, attrs_sql, consql)
        print(sql)
        return self.executeCommit(sql)

    def dropTable(self, tablename):
        """删除数据库表

            args：
                tablename  ：表名字
        """
        sql = "DROP TABLE  %s" % tablename
        self.executeCommit(sql)

    def deleteTable(self, table_name):
        """清空数据库表

            args：
                tablename  ：表名字
        """
        sql = f"DELETE FROM {table_name}"
        self.exec(sql)

if __name__ == "__main__":

    # 定义数据库访问参数
    config = {
        'host': '127.0.0.1',
        'port': 33060,
        'user': 'root',
        'password': '123456',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    # 初始化打开数据库连接
    db = MySQL(config)

    # 打印数据库版本
    print(db.get_version())

    # 创建数据库
    db_name = input('输入要创建的数据库名：')
    db.create_database(db_name)

    # 选择数据库
    print("========= 选择数据库%s ===========" % db_name)
    db.selectDataBase(db_name)
    #
    # #创建表
    # TABLE_NAME = input('输入要创建的数据表名：')
    # print("========= 选择数据表%s ===========" % TABLE_NAME)
    # '''例如
    #     CREATE TABLE `lisi` (
    #       `id` bigint(11) NOT NULL auto_increment,
    #       `name` varchar(30) NOT NULL,
    #       PRIMARY KEY  (`id`)
    #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    # '''
    # print("========= 设置表的字段和属性 ===========" )
    # attrdict = {
    #     'name':'varchar(30) NOT NULL'
    # }
    # constraint = "PRIMARY KEY(`id`)"
    # mydb.creatTable(TABLE_NAME,attrdict,constraint)
    # print('首次创建以后，请手动刷新一下数据库表页面。')
    #
    # # 插入纪录
    # print("========= 单条数据插入 ===========")
    # params = {}
    # for i in range(5):
    #     params.update({"name":"testuser"+str(i)}) # 生成字典数据，循环插入
    #     print(params)
    #     mydb.insert(TABLE_NAME, params)
    #     print("")
    #
    # # 批量插入数据
    # print("========= 多条数据同时插入 ===========")
    # insert_values = []
    # for i in range(5):
    #     # values.append((i,"testuser"+str(i)))
    #     insert_values.append([u"测试用户"+str(i)]) # 插入中文数据
    # print(insert_values)
    # insert_attrs = ["name"]
    # mydb.insertMany(TABLE_NAME,insert_attrs, insert_values)
    #
    # # 数据查询
    # print("========= 数据查询 ===========")
    # print(mydb.select(TABLE_NAME, fields=["id", "name"]))
    # print(mydb.select(TABLE_NAME, cond_dict = {'name':'测试用户1'},fields=["id", "name"]))
    # print(mydb.select(TABLE_NAME, cond_dict = {'name':'测试用户2'},fields=["id", "name"],order="order by id desc"))
    #
    # # 删除数据
    # print("========= 删除数据 ===========")
    # delete_params = {"name": "测试用户2"}
    # mydb.delete(TABLE_NAME, delete_params)
    #
    # # 更新数据
    # print("========= 更新数据 ===========")
    # update_params = {"name": "测试用户99"}   # 需要更新为什么值
    # update_cond_dict = {"name": "测试用户3"}  # 更新执行的查询条件
    # mydb.update(TABLE_NAME, update_params, update_cond_dict)
    #
    # # 删除表数据
    # print("========= 删除表数据 ===========")
    # mydb.deleteTable(TABLE_NAME)
    #
    # # 删除表
    # print("========= 删除表===================")
    # mydb.dropTable(TABLE_NAME)

