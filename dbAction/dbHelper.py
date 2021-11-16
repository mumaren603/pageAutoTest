from dbAction.DBPool import DJ_POOL,QJ_POOL

# 登记库数据池操作
class DJ_DB():
    # 从数据池取连接
    def createConn(self):
        conn = DJ_POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    # 将连接放回数据池
    def closeConn(self,conn, cursor):
        cursor.close()
        conn.close()

    # 查询一条(单个值)
    def fetchone(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        result = cursor.fetchone()    # return tuple
        self.closeConn(conn, cursor)
        if result:
            return result[0]
        return

    # 查询一条(多个值)
    def fetchone2(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        result = cursor.fetchone()    # return tuple
        self.closeConn(conn, cursor)
        return result

    # 查询所有
    def fetchall(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeConn(conn, cursor)
        return result

    # 插入数据
    def insertData(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        conn.commit()
        self.closeConn(conn, cursor)

# 权籍库数据池操作
class QJ_DB():
    # 从数据池取连接
    def createConn(self):
        conn = QJ_POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    # 将连接放回数据池
    def closeConn(self,conn, cursor):
        cursor.close()
        conn.close()

    # 查询一条
    def fetchone(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        result = cursor.fetchone()    # return tuple
        self.closeConn(conn, cursor)
        if result:
            return result[0]
        return

    # 查询所有
    def fetchall(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeConn(conn, cursor)
        return result

    # 插入数据
    def insertData(self,sql):
        conn, cursor = self.createConn()
        cursor.execute(sql)
        conn.commit()
        self.closeConn(conn, cursor)

if __name__ == '__main__':
    obj = DJ_DB()
    sql="select ywh from yw_sqxx where  ywlx = 'C49536D5C50F4F609FACAAAE805EC510' and bdcdyh='321202403598GB00266W00000000'"
    # sql="select id from dj_tdxx where  bdcdyh='321202403598GB00266W00000000'"

    aa = obj.fetchone(sql)
    print('查询结果：',aa)
