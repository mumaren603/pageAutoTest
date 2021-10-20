'''
用于业务登簿后数据库结果检查
'''
from dbAction.db import DBAction
from Common.logFunc import loggerConf

logger = loggerConf().getLogger()

class dataResCheck():
    def __init__(self,dbInfo):
        self.db_qj_conn = DBAction(dbInfo.get('qj'))
        self.db_dj_conn = DBAction(dbInfo.get('dj'))

    #----------------------------------净地产权登记-------------------------------------#
    # 净地登记
    def landRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" %res_yw_sqxx_ywh)

            sql_dj_jsydsyq_id = "select id from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_id = str(self.db_dj_conn.SqlExecute(sql_dj_jsydsyq_id))
            logger.debug("dj_jsydsyq表id：%s" %res_dj_jsydsyq_id)

            sql_dj_jsydsyq_djbid = "select djbid from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_jsydsyq_djbid))
            logger.debug("dj_jsydsyq表djbid：%s" %res_dj_jsydsyq_djbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq = self.db_dj_conn.SqlExecute(sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and djbid='" + res_dj_jsydsyq_djbid + "'"
            res_dj_tdxx = self.db_dj_conn.SqlExecute(sql_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.db_dj_conn.SqlExecute(sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_dj_jsydsyq_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_djb = "select count(1) from dj_djb  where  zt='1'and sfyx=1 and id in(select djbuid from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_dj_jsydsyq_djbid + "')"
            res_dj_djb = self.db_dj_conn.SqlExecute(sql_dj_djb)
            logger.debug("dj_djb表查询sql：%s" % sql_dj_djb)
            logger.debug("dj_djb表查询记录数：%d" % res_dj_djb)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and djbid='"+ res_dj_jsydsyq_djbid +"'"
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='"+ res_dj_jsydsyq_id + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='"+ res_dj_jsydsyq_id + "')"
            res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" %res_dj_qlr)

            if res_dj_jsydsyq and res_dj_tdxx and res_dj_zdjbxx and res_dj_djb and sql_dj_djben and res_dj_qlrgl and res_dj_qlr and res_dj_zs:
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
                logger.error("数据库数据归档错误。")
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 净地注销登记
    def landCancelRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_jsydsyq_id = "select id from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_id = str(self.db_dj_conn.SqlExecute(sql_dj_jsydsyq_id))
            logger.debug("dj_jsydsyq表id：%s" % res_dj_jsydsyq_id)

            sql_dj_jsydsyq_djbid = "select djbid from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_jsydsyq_djbid))
            logger.debug("dj_jsydsyq表djbid：%s" % res_dj_jsydsyq_djbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq = self.db_dj_conn.SqlExecute(sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='2' and sfyx=1 and cqbid='" + res_dj_jsydsyq_id + "'"
            res_dj_tdxx = self.db_dj_conn.SqlExecute(sql_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='2' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.db_dj_conn.SqlExecute(sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfzx=1 and sfysczql=0  and id =" + res_dj_jsydsyq_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_jsydsyq_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and cqbid =" + res_dj_jsydsyq_id + ""
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" % res_dj_zs)

            if res_dj_jsydsyq  and res_dj_djben and res_dj_qlrgl and res_dj_tdxx and res_dj_zdjbxx and res_dj_zs :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # ----------------------------------房屋产权登记-------------------------------------#
    # 房屋登记
    def houseRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" %res_dj_fdcq2_id)

            sql_dj_hxx_djbid = "select djbid from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_hxx_djbid))
            logger.debug("dj_hxx表查询djbid为：%s" %res_dj_hxx_djbid)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_hxx_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" %res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
            res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if res_dj_fdcq2_id and res_dj_hxx_djbid and res_dj_fdcq2_djben_zs and res_dj_djben and sql_dj_zs and res_dj_qlrgl and res_dj_qlr :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" %e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

        # try:
        #     sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
        #     res_dj_fdcq2 = self.db_dj_conn.SqlExecute(sql_dj_fdcq2)
        #     print("dj_fdcq2:", res_dj_fdcq2,type(res_dj_fdcq2))
        #
        #     sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
        #     res_dj_hxx = self.db_dj_conn.SqlExecute(sql_dj_hxx)
        #     print("dj_hxx:", res_dj_hxx,type(res_dj_hxx))
        #
        #     sql_dj_djben = "select count(1) from dj_djben t where zt='1' and sfyx=1 and sfysczql=1 and id in(select djbid from dj_fdcq2 where bdcdyh='" + bdcdyh + "')"
        #     res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
        #     print("dj_djben:", res_dj_djben,type(res_dj_djben))
        #
        #     sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and bdcdyh='" + bdcdyh + "'and qlrmc='" + qlrmc + "'"
        #     res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
        #     print("dj_fdcq2_djben_zs:", res_dj_fdcq2_djben_zs,type(res_dj_fdcq2_djben_zs))
        #
        #     sql_dj_qlrgl ="select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "'"
        #     res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
        #     print("dj_qlrgl:", res_dj_qlrgl,type(res_dj_qlrgl))
        #
        #     sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "')"
        #     res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
        #     print("dj_qlr:", res_dj_qlr,type(res_dj_qlr))
        #
        #     sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'and qlr = '" + qlrmc + "'"
        #     res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
        #     print("dj_zs:", res_dj_zs,type(res_dj_zs))
        #
        #     if res_dj_fdcq2 and res_dj_hxx and res_dj_fdcq2_djben_zs and res_dj_djben and res_dj_djben and res_dj_qlrgl and res_dj_qlr and res_dj_zs:
        #         print("数据库数据归档正确!")
        #         return True
        #     else:
        #         print("数据库数据归档错误!")
        #         return False
        #
        # except Exception as e:
        #         print(e)
        # finally:
        #     # 关闭数据库连接
        #     self.db_dj_conn.closeConn()
        #     self.db_qj_conn.closeConn()

    # 分户转移
    # def fhTransferRegisterDataCheck(self,bdcdyh,data):
    #     ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
    #     sfpl = data.get('initdata').get('params', None).get('sfpl', None)
    #     cqType = data.get('initdata').get('params', None).get('cqType', None)
    #     try:
    #         # 批量业务
    #         if sfpl == 1:
    #             sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #             res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
    #             logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
    #         else:
    #             sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #             res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
    #             logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)
    #
    #
    #     ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
    #     try:
    #         sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #         res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
    #         logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)
    #
    #         sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
    #         res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
    #         logger.debug("dj_fdcq2表查询id为：%s" %res_dj_fdcq2_id)
    #
    #         sql_dj_hxx_djbid = "select djbid from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_hxx_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_hxx_djbid))
    #         logger.debug("dj_hxx表查询djbid为：%s" %res_dj_hxx_djbid)
    #
    #         sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
    #         logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" %res_dj_fdcq2_djben_zs)
    #
    #         sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_hxx_djbid + "'"
    #         res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
    #         logger.debug("dj_djben表查询记录为：%d" %res_dj_djben)
    #
    #         sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
    #         logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)
    #
    #         sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
    #         logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)
    #
    #         sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
    #         res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
    #         logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)
    #
    #         if res_dj_fdcq2_id and res_dj_fdcq2_id and res_dj_fdcq2_djben_zs and res_dj_djben and sql_dj_zs and res_dj_qlrgl and res_dj_qlr :
    #             logger.debug("数据库数据归档正确。")
    #             return True
    #         else:
    #             logger.error("数据库数据归档错误。")
    #             return False
    #     except Exception as e:
    #         logger.error("数据库数据归档错误,错误信息为：%s" %e)
    #     finally:
    #         # 关闭数据库连接
    #         self.db_dj_conn.closeConn()
    #         self.db_qj_conn.closeConn()
    #
    #     # try:
    #     #     sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
    #     #     res_dj_fdcq2 = self.db_dj_conn.SqlExecute(sql_dj_fdcq2)
    #     #     print("dj_fdcq2:", res_dj_fdcq2,type(res_dj_fdcq2))
    #     #
    #     #     sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
    #     #     res_dj_hxx = self.db_dj_conn.SqlExecute(sql_dj_hxx)
    #     #     print("dj_hxx:", res_dj_hxx,type(res_dj_hxx))
    #     #
    #     #     sql_dj_djben = "select count(1) from dj_djben t where zt='1' and sfyx=1 and sfysczql=1 and id in(select djbid from dj_fdcq2 where bdcdyh='" + bdcdyh + "')"
    #     #     res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
    #     #     print("dj_djben:", res_dj_djben,type(res_dj_djben))
    #     #
    #     #     sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and bdcdyh='" + bdcdyh + "'and qlrmc='" + qlrmc + "'"
    #     #     res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
    #     #     print("dj_fdcq2_djben_zs:", res_dj_fdcq2_djben_zs,type(res_dj_fdcq2_djben_zs))
    #     #
    #     #     sql_dj_qlrgl ="select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "'"
    #     #     res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
    #     #     print("dj_qlrgl:", res_dj_qlrgl,type(res_dj_qlrgl))
    #     #
    #     #     sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "')"
    #     #     res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
    #     #     print("dj_qlr:", res_dj_qlr,type(res_dj_qlr))
    #     #
    #     #     sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'and qlr = '" + qlrmc + "'"
    #     #     res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
    #     #     print("dj_zs:", res_dj_zs,type(res_dj_zs))
    #     #
    #     #     if res_dj_fdcq2 and res_dj_hxx and res_dj_fdcq2_djben_zs and res_dj_djben and res_dj_djben and res_dj_qlrgl and res_dj_qlr and res_dj_zs:
    #     #         print("数据库数据归档正确!")
    #     #         return True
    #     #     else:
    #     #         print("数据库数据归档错误!")
    #     #         return False
    #     #
    #     # except Exception as e:
    #     #         print(e)
    #     # finally:
    #     #     # 关闭数据库连接
    #     #     self.db_dj_conn.closeConn()
    #     #     self.db_qj_conn.closeConn()

    # 裁定过户（房）
    def cdghHouseRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" %res_dj_fdcq2_id)

            sql_dj_hxx_djbid = "select djbid from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_hxx_djbid))
            logger.debug("dj_hxx表查询djbid为：%s" %res_dj_hxx_djbid)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfsfcd=0 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfsfcd =0 and id='" + res_dj_hxx_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" %res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
            res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if res_dj_fdcq2_id and res_dj_fdcq2_id and res_dj_fdcq2_djben_zs and res_dj_djben and sql_dj_zs and res_dj_qlrgl and res_dj_qlr :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" %e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 公建配套登记
    def jzwqfyzgybfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        bdcdyh = bdcdyh[:19]+'W00000000'
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)

            sql_dj_jzwqfsyqyzgybf = "select count(1) from dj_jzwqfsyqyzgybf t where zt='1' and sfyx=1 and bz2='" + res_yw_sqxx_ywh + "'"
            res_dj_jzwqfsyqyzgybf = self.db_dj_conn.SqlExecute(sql_dj_jzwqfsyqyzgybf)
            logger.debug("dj_jzwqfsyqyzgybf表查询记录为：%d" % res_dj_jzwqfsyqyzgybf)

            sql_dj_fsssxx = "select count(1) from dj_fsssxx where zt='1' and sfyx=1 and bz2='" + res_yw_sqxx_ywh + "'"
            res_dj_fsssxx = self.db_dj_conn.SqlExecute(sql_dj_fsssxx)
            logger.debug("dj_fsssxx表查询记录为：%d" % res_dj_fsssxx)

            sql_dj_qlrgl ="select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if res_dj_jzwqfsyqyzgybf and res_dj_fsssxx and res_dj_qlrgl and res_dj_qlr:
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 项目类多幢登记(整体发证)
    def xmldzRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
            logger.debug("cqbid为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djbid))
            logger.debug("djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.db_dj_conn.SqlExecute(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询为：%d" %res_dj_fdcq2)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询为：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id =" + res_dj_fdcq2_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询为：%d" %res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询为：%d" %res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询为：%d" %res_dj_zs)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and sfdz=1 and sfdh=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_hxx = self.db_dj_conn.SqlExecute(sql_dj_hxx)
            logger.debug("dj_hxx表查询为：%d" %res_dj_hxx)

            if res_dj_fdcq2 and res_dj_fdcq2_djben_zs and res_dj_djben and res_dj_qlrgl and res_dj_zs and res_dj_hxx:
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 项目类多幢登记(按幢发证)
    def xmldzRegisterDataCheck2(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
        try:
            if sfztfz == 0:
                sql_yw_sqxxzb_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxxzb_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxxzb_ywh)
                logger.debug("yw_sqxxzb表ywh：%s" % res_yw_sqxxzb_ywh)
            else:
                logger.error("非按幢发证，请检查yml配置文件sfztfz参数是否配置正确。")
                return

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表id：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zt='1' and sfyx=1  and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表djbid：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and sfdz is null and sfdh is null and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2 = self.db_dj_conn.SqlExecute(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % res_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录数：%d" %res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and sfdz is null and sfdh is null and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_hxx = self.db_dj_conn.SqlExecute(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录数：%d" %res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdh is null and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录数：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id =" + res_dj_fdcq2_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" %res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" %res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" %res_dj_zs)

            if res_dj_fdcq2 and res_dj_fdcq2_djben_zs and res_dj_djben and res_dj_qlrgl and res_dj_zs and res_dj_hxx:
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 房屋注销登记
    def houseCancelRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表查询djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.db_dj_conn.SqlExecute(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='2' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx = self.db_dj_conn.SqlExecute(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfzx=1 and sfysczql=0 and id='" + res_dj_fdcq2_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.db_dj_conn.SqlExecute(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and ryzl in (1,2) and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            if res_dj_fdcq2 and res_dj_djben and res_dj_qlrgl and res_dj_hxx and res_dj_zs and res_dj_fdcq2_djben_zs == 0 :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # ---------------------------------抵押登记-----------------------------------------#
    # 抵押(土地、房屋)登记
    def dyRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)

            sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_dy = self.db_dj_conn.SqlExecute(sql_dj_dy)
            logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=1 and sfysczql=1 and id in(select djbid from dj_dy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_dy_djben_zm = self.db_dj_conn.SqlExecute(sql_dj_dy_djben_zm)
            logger.debug("dj_dy_djben_zm表查询记录为：%d"  % res_dj_dy_djben_zm)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_qlr = self.db_dj_conn.SqlExecute(sql_dj_qlr)
            logger.debug("dj_qlr：%d" % res_dj_qlr)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            logger.debug("dj_zm：%d" % res_dj_zm)

            if res_dj_dy and res_dj_dy_djben_zm and res_dj_djben and res_dj_qlrgl and res_dj_qlr and res_dj_zm:
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误。")
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 不动产抵押注销
    def dyCancelDataCheck(self, bdcdyh, lcinfo):
        try:
            sql_fdcq2_id = "select id from DJJGK.dj_fdcq2 t where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_fdcq2_id = self.db_dj_conn.SqlExecute(sql_fdcq2_id)
            res_fdcq2_id = str(res_fdcq2_id)
            print("fdcq2_id:", res_fdcq2_id,type(res_fdcq2_id))

            sql_fdcq2_djbid = "select djbid from DJJGK.dj_fdcq2 t where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_fdcq2_djbid = self.db_dj_conn.SqlExecute(sql_fdcq2_djbid)
            res_fdcq2_djbid = str(res_fdcq2_djbid)
            print("fdcq2_djbid:", res_fdcq2_djbid,type(res_fdcq2_djbid))

            sql_dj_dy_id = "select id from DJJGK.DJ_DY where zt='2' and sfyx=1 and cqbid='" + res_fdcq2_id + "'"
            res_dj_dy_id = self.db_dj_conn.SqlExecute(sql_dj_dy_id)
            res_dj_dy_id = str(res_dj_dy_id)
            print("dj_dy_id:", res_dj_dy_id)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=0 and sfysczql=1 and id = '" + res_fdcq2_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            print("dj_djben:", res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdy=0 and qlbid='" + res_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            print("dj_fdcq2_djben_zs:", res_dj_fdcq2_djben_zs)

            sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where  qlbid='" + res_fdcq2_id + "'"
            res_dj_dy_djben_zm = self.db_dj_conn.SqlExecute(sql_dj_dy_djben_zm)
            print("dj_dy_djben_zm:", res_dj_dy_djben_zm)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_dj_dy_id + "'"
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            print("dj_qlrgl:", res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and djbid='" + res_fdcq2_djbid + "'"
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            print("dj_zm:", res_dj_zm)

            if res_dj_dy_id and res_dj_fdcq2_djben_zs and res_dj_djben and res_dj_qlrgl and res_dj_zm and(not res_dj_dy_djben_zm):
                print("数据库数据归档正确!")
                return True
            else:
                print("数据库数据归档错误!")
                return False
        except Exception as e:
            print(e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # ---------------------------------预告登记-----------------------------------------#
    # 商品房预告登记
    def spfYgRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_yg_id = "select id from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_id = str(self.db_dj_conn.SqlExecute(sql_dj_yg_id))
            logger.debug("dj_yg表id：%s" % res_dj_yg_id)

            sql_dj_yg_djbid = "select djbid from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_yg_djbid))
            logger.debug("dj_yg表djbid：%s" % res_dj_yg_djbid)

            sql_dj_yg_hid = "select hid from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_hid = str(self.db_dj_conn.SqlExecute(sql_dj_yg_hid))
            logger.debug("dj_yg表hid：%s" % res_dj_yg_hid)

            sql_dj_yg = "select count(1) from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg = self.db_dj_conn.SqlExecute(sql_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and id =" + res_dj_yg_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_yg_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_ychxx = "select count(1) from dj_ychxx where zt='1' and sfyx=1 and id =" + res_dj_yg_hid + ""
            res_dj_ychxx = self.db_dj_conn.SqlExecute(sql_dj_ychxx)
            logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
            logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and djbid =" + res_dj_yg_djbid + ""
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if res_dj_yg  and res_dj_djben and res_dj_qlrgl and res_dj_ychxx and res_dj_zm :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 商品房预抵押
    def spfYdyRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            # sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(zhxgsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_ydy_id = "select id from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_id = str(self.db_dj_conn.SqlExecute(sql_dj_ydy_id))
            logger.debug("dj_ydy表id：%s" % res_dj_ydy_id)

            sql_dj_ydy_djbid = "select djbid from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_ydy_djbid))
            logger.debug("dj_ydy表djbid：%s" % res_dj_ydy_djbid)

            sql_dj_ydy = "select count(1) from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy = self.db_dj_conn.SqlExecute(sql_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录数：%d" % res_dj_ydy)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql is null and id =" + res_dj_ydy_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_ydy_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and djbid =" + res_dj_ydy_djbid + ""
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if res_dj_ydy  and res_dj_djben and res_dj_qlrgl and res_dj_zm :
                logger.debug("数据库数据归档正确。")
                return True
            else:
                logger.error("数据库数据归档错误。")
                return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 预告注销登记
    def ygCancelRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_yg_id = "select id from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_id = str(self.db_dj_conn.SqlExecute(sql_dj_yg_id))
            logger.debug("dj_yg表id：%s" % res_dj_yg_id)

            sql_dj_yg_djbid = "select djbid from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_yg_djbid))
            logger.debug("dj_yg表djbid：%s" % res_dj_yg_djbid)

            sql_dj_yg_hid = "select hid from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_hid = self.db_dj_conn.SqlExecute(sql_dj_yg_hid)
            logger.debug("dj_yg表hid：%s" % res_dj_yg_hid)

            sql_dj_yg = "select count(1) from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg = self.db_dj_conn.SqlExecute(sql_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfyg = 0 and id =" + res_dj_yg_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_yg_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            if res_dj_yg_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='2' and sfyx=1 and id =" + str(res_dj_yg_hid) + ""
                res_dj_ychxx = self.db_dj_conn.SqlExecute(sql_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            # 证明类型（2）-->预告证明
            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and zmlx='2' and djbid =" + res_dj_yg_djbid + ""
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if res_dj_yg_hid:
                if res_dj_yg  and res_dj_djben and res_dj_qlrgl and res_dj_ychxx and res_dj_zm :
                    logger.debug("数据库数据归档正确。")
                    return True
                else:
                    logger.error("数据库数据归档错误。")
                    return False
            else:
                if res_dj_yg  and res_dj_djben and res_dj_qlrgl  and res_dj_zm :
                    logger.debug("数据库数据归档正确。")
                    return True
                else:
                    logger.error("数据库数据归档错误。")
                    return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 预抵押注销登记
    def ydyCancelRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_ydy_id = "select id from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_id = str(self.db_dj_conn.SqlExecute(sql_dj_ydy_id))
            logger.debug("dj_ydy表id：%s" % res_dj_ydy_id)

            sql_dj_ydy_djbid = "select djbid from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_ydy_djbid))
            logger.debug("dj_ydy表djbid：%s" % res_dj_ydy_djbid)

            sql_dj_ydy = "select count(1) from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy = self.db_dj_conn.SqlExecute(sql_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录数：%d" % res_dj_ydy)

            # 查询该单元上是否存在其他现势抵押信息
            sql_dj_ydy_count = "select count(1) from dj_ydy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ydy_count = self.db_dj_conn.SqlExecute(sql_dj_ydy_count)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy_count)
            logger.debug("dj_ydy表查询抵押条数：%d" % res_dj_ydy_count)

            # 该单元只有一条抵押信息，登簿后sfydy=0
            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=0 and id =" + res_dj_ydy_djbid + ""
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            # 该单元有其他抵押信息，登簿后sfydy=1
            sql_dj_djben2 = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=1 and id =" + res_dj_ydy_djbid + ""
            res_dj_djben2 = self.db_dj_conn.SqlExecute(sql_dj_djben2)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben2)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben2)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_ydy_id + ""
            res_dj_qlrgl = self.db_dj_conn.SqlExecute(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            # 证明类型（3）-->预告抵押证明
            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and zmlx='3' and djbid =" + res_dj_ydy_djbid + ""
            res_dj_zm = self.db_dj_conn.SqlExecute(sql_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)


            # 无其他预抵押信息
            if not res_dj_ydy_count:
                if res_dj_ydy  and res_dj_djben and res_dj_qlrgl and res_dj_zm :
                    logger.debug("数据库数据归档正确。")
                    return True
                else:
                    logger.error("数据库数据归档错误。")
                    return False
            else:
                if res_dj_ydy and res_dj_djben2 and res_dj_qlrgl and res_dj_zm:
                    logger.debug("数据库数据归档正确。")
                    return True
                else:
                    logger.error("数据库数据归档错误。")
                    return False
        except Exception as e:
            logger.error("数据库数据归档错误,错误信息为：%s" % e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # -----------------------------------查封登记----------------------------------------#
    # 查封登记
    def cfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf = self.db_dj_conn.SqlExecute(sql_dj_cf)
            logger.debug("dj_cf表查询到该笔业务数据：%s" %res_dj_cf)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id in(select djbid from dj_cf where bdcdyh='" + bdcdyh + "')"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=1 and  bdcdyh='" + bdcdyh + "'"
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询到该笔业务数据：%s" %res_dj_fdcq2_djben_zs)

            # 房屋校验逻辑
            if cqType == 1:
                if res_dj_cf and res_dj_djben and res_dj_fdcq2_djben_zs:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
            # 净地校验逻辑
            else:
                if res_dj_cf and res_dj_djben:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 解封登记
    def jfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # 过滤小证目前不考虑，因为转数据时会将大小证都刷 即大证dj_cf表中zszbid也可能有值
            # sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and zszbid is null and bdcdyh='" + bdcdyh + "'"
            sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_cf = self.db_dj_conn.SqlExecute(sql_dj_cf)
            logger.debug("当前单元在dj_cf表数据条数为：%s" %res_dj_cf)

            sql_dj_cf2 = "select count(1) from dj_cf where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf2 = self.db_dj_conn.SqlExecute(sql_dj_cf2)
            logger.debug("通过解封业务号查询到当前数据条数为：%s" %res_dj_cf2)

            sql_dj_djben = "select sfcf from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务sfcf状态为数据：%d" %res_dj_djben)

            if res_dj_cf >= 1:
                if res_dj_cf2 and res_dj_djben == 1:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
            else:
                if res_dj_cf2 and res_dj_djben == 0:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 预查封登记
    def ycfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # 首查封，查封顺序cfsx=1,cflx=3(预查封)
            sql_dj_ycf = "select count(1) from dj_ycf t where cflx=3 and cfsx=1 and zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ycf = self.db_dj_conn.SqlExecute(sql_dj_ycf)
            logger.debug("dj_ycf表查询到该笔业务数据：%s" %res_dj_ycf)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfycf=1 and id in(select djbid from dj_ycf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "')"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            if res_dj_ycf and res_dj_djben:
                logger.debug("数据库数据归档正确")
                return True
            else:
                logger.error("数据库数据归档错误")
                return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 预查封登记（轮候）
    def lhycfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # 判断dj_ycf有几条现势数据
            sql_dj_ycf_count = "select count(1) from dj_ycf t where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ycf_count = self.db_dj_conn.SqlExecute(sql_dj_ycf_count)
            logger.debug("dj_ycf表查询到共%s条现势数据" %res_dj_ycf_count)

            if res_dj_ycf_count > 1:
                # 轮候查封  cflx=4(轮候查封)，cfsx根据dj_ycf现势数据计算
                sql_dj_ycf = "select count(1) from dj_ycf t where cflx=4 and zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "' and  cfsx='" + res_dj_ycf_count + "'"
                res_dj_ycf = self.db_dj_conn.SqlExecute(sql_dj_ycf)
                logger.debug("dj_ycf表查询到该笔业务数据：%s" % res_dj_ycf)


            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfycf=1 and id in(select djbid from dj_ycf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "')"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            if res_dj_ycf and res_dj_djben:
                logger.debug("数据库数据归档正确")
                return True
            else:
                logger.error("数据库数据归档错误")
                return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 查封登记(续查封)
    # def xcfRegisterDataCheck(self, bdcdyh):
    #     try:
    #         sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
    #         res_dj_cf = self.db_dj_conn.SqlExecute(sql_dj_cf)
    #         print("dj_cf:", res_dj_cf)
    #
    #         sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id in(select djbid from dj_cf where bdcdyh='" + bdcdyh + "')"
    #         res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
    #         print("dj_djben:", res_dj_djben)
    #
    #         if res_dj_cf and res_dj_djben:
    #             print("数据库数据归档正确!")
    #             return True
    #         else:
    #             print("数据库数据归档错误!")
    #             return False
    #     except Exception as e:
    #         raise e
    #     finally:
    #         # 关闭数据库连接
    #         self.db_dj_conn.closeConn()
    #         self.db_qj_conn.closeConn()

    #------------------------------------其他登记------------------------------------------#
    #冻结登记
    def djRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_qtxz_id = "select id from dj_qtxz where zt='1' and sfyx=1 and xzlx='5' and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_id = str(self.db_dj_conn.SqlExecute(sql_dj_qtxz_id))
            logger.debug("cqbid为：%s" % res_dj_qtxz_id)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_qtxz_djbid))
            logger.debug("djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and xzlx='5' and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.db_dj_conn.SqlExecute(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询到该笔业务数据：%s" %res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdj=1 and sfqtxz =1 and  id ='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdj=1 and qlbid =" + res_dj_qtxz_id + ""
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询为：%d" %res_dj_fdcq2_djben_zs)

            # 房屋校验逻辑
            if cqType == 1:
                if res_dj_qtxz and res_dj_djben and res_dj_fdcq2_djben_zs:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
            # 净地校验逻辑
            else:
                if res_dj_qtxz and res_dj_djben:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    #解冻登记
    def jdRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.db_dj_conn.SqlExecute(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # sql_dj_qtxz_id = "select id from dj_qtxz where zt='2' and sfyx=1 and xzlx='5' and jfywh='" + res_yw_sqxx_ywh + "'"
            # res_dj_qtxz_id = str(self.db_dj_conn.SqlExecute(sql_dj_qtxz_id))
            # logger.debug("cqbid为：%s" % res_dj_qtxz_id)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.db_dj_conn.SqlExecute(sql_dj_qtxz_djbid))
            logger.debug("djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.db_dj_conn.SqlExecute(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询到该笔业务数据：%s" %res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdj=0 and sfqtxz =0 and sfnbxz=0  and  id ='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.db_dj_conn.SqlExecute(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdj=0 and bdcdyh =" + bdcdyh + ""
            res_dj_fdcq2_djben_zs = self.db_dj_conn.SqlExecute(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询为：%d" %res_dj_fdcq2_djben_zs)

            # 房屋校验逻辑
            if cqType == 1:
                if res_dj_qtxz and res_dj_djben and res_dj_fdcq2_djben_zs:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
            # 净地校验逻辑
            else:
                if res_dj_qtxz and res_dj_djben:
                    logger.debug("数据库数据归档正确")
                    return True
                else:
                    logger.error("数据库数据归档错误")
                    return False
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()


if __name__ == '__main__':
    dbInfo={
        'qj': 'KJK/KJK@172.16.17.247:1521/tzkjk',
        'dj': 'djpt/djpt@172.16.17.241:1521/orcl'
    }

    # dataResCheck(dbInfo).xmldzRegisterDataCheck('321202050004GB00089F00040807','1')

