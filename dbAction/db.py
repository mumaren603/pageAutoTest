#Author: ls Liu
'''已废弃 改用数据池'''
import cx_Oracle as Oracle
from Common.LogFunc import loggerConf
import sys

logger = loggerConf().getLogger()

class DBAction():
    def __init__(self,dbConnInfo):
        self.conn = None
        try:
            self.conn = Oracle.connect(dbConnInfo)
        except Exception as e:
            logger.error("数据库连接失败!失败信息为：%s" % e)
            sys.exit(-1)

    def SqlExecute(self,sql):
        cursor = self.conn.cursor()      #获取操作游标
        try:
            res = cursor.execute(sql)
            queryResult = res.fetchone()
            # 会出现查不到数据情况，这里需要判断
            if queryResult:
                queryResult = queryResult[0]
                return queryResult
            return
        except Exception as e:
            logger.error("数据库异常，异常信息为：%s" %e)
            sys.exit(-1)
        finally:
            cursor.close()


    #单独写一个关闭连接操作而不是放在SqlExecute()里，是因为建立一次连接后可能会执行多次查询，最后统一关闭数据库连接。
    def closeConn(self):
        self.conn.close()

