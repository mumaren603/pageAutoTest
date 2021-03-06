'''
用于业务登簿后数据库结果检查
'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

class dataResCheck():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    '''净地产权登记'''
    # 净地登记
    def landRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" %res_yw_sqxx_ywh)

            sql_dj_jsydsyq_id = "select id from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_id = str(self.djObj.fetchone(sql_dj_jsydsyq_id))
            logger.debug("dj_jsydsyq表id：%s" %res_dj_jsydsyq_id)

            sql_dj_jsydsyq_djbid = "select djbid from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_djbid = str(self.djObj.fetchone(sql_dj_jsydsyq_djbid))
            logger.debug("dj_jsydsyq表djbid：%s" %res_dj_jsydsyq_djbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq = self.djObj.fetchone(sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and djbid='" + res_dj_jsydsyq_djbid + "'"
            res_dj_tdxx = self.djObj.fetchone(sql_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.djObj.fetchone(sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_dj_jsydsyq_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_djb = "select count(1) from dj_djb  where  zt='1'and sfyx=1 and id in(select djbuid from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_dj_jsydsyq_djbid + "')"
            res_dj_djb = self.djObj.fetchone(sql_dj_djb)
            logger.debug("dj_djb表查询sql：%s" % sql_dj_djb)
            logger.debug("dj_djb表查询记录数：%d" % res_dj_djb)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and djbid='"+ res_dj_jsydsyq_djbid +"'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='"+ res_dj_jsydsyq_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='"+ res_dj_jsydsyq_id + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_jsydsyq_id = "select id from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_id = str(self.djObj.fetchone(sql_dj_jsydsyq_id))
            logger.debug("dj_jsydsyq表id：%s" % res_dj_jsydsyq_id)

            sql_dj_jsydsyq_djbid = "select djbid from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq_djbid = str(self.djObj.fetchone(sql_dj_jsydsyq_djbid))
            logger.debug("dj_jsydsyq表djbid：%s" % res_dj_jsydsyq_djbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_jsydsyq = self.djObj.fetchone(sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='2' and sfyx=1 and cqbid='" + res_dj_jsydsyq_id + "'"
            res_dj_tdxx = self.djObj.fetchone(sql_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='2' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.djObj.fetchone(sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfzx=1 and sfysczql=0  and id =" + res_dj_jsydsyq_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_jsydsyq_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and cqbid =" + res_dj_jsydsyq_id + ""
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
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

    '''房屋产权登记'''
    # 房屋登记
    def houseRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.djObj.fetchone(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表查询djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and  qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_dj_fdcq2_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if res_dj_fdcq2 and res_dj_hxx and res_dj_fdcq2_djben_zs and res_dj_djben and sql_dj_zs and res_dj_qlrgl and res_dj_qlr :
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

    # 分户转移
    # def fhTransferRegisterDataCheck(self,bdcdyh,data):
    #     ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
    #     sfpl = data.get('initdata').get('params', None).get('sfpl', None)
    #     cqType = data.get('initdata').get('params', None).get('cqType', None)
    #     try:
    #         # 批量业务
    #         if sfpl == 1:
    #             sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #             res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
    #             logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
    #         else:
    #             sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #             res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
    #             logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)
    #
    #
    #     ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
    #     try:
    #         sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
    #         res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
    #         logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)
    #
    #         sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
    #         res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
    #         logger.debug("dj_fdcq2表查询id为：%s" %res_dj_fdcq2_id)
    #
    #         sql_dj_hxx_djbid = "select djbid from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_hxx_djbid = str(self.djObj.fetchone(sql_dj_hxx_djbid))
    #         logger.debug("dj_hxx表查询djbid为：%s" %res_dj_hxx_djbid)
    #
    #         sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
    #         logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" %res_dj_fdcq2_djben_zs)
    #
    #         sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_hxx_djbid + "'"
    #         res_dj_djben = self.djObj.fetchone(sql_dj_djben)
    #         logger.debug("dj_djben表查询记录为：%d" %res_dj_djben)
    #
    #         sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_zs = self.djObj.fetchone(sql_dj_zs)
    #         logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)
    #
    #         sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
    #         res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
    #         logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)
    #
    #         sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
    #         res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
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
    #     #     res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
    #     #     print("dj_fdcq2:", res_dj_fdcq2,type(res_dj_fdcq2))
    #     #
    #     #     sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
    #     #     res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
    #     #     print("dj_hxx:", res_dj_hxx,type(res_dj_hxx))
    #     #
    #     #     sql_dj_djben = "select count(1) from dj_djben t where zt='1' and sfyx=1 and sfysczql=1 and id in(select djbid from dj_fdcq2 where bdcdyh='" + bdcdyh + "')"
    #     #     res_dj_djben = self.djObj.fetchone(sql_dj_djben)
    #     #     print("dj_djben:", res_dj_djben,type(res_dj_djben))
    #     #
    #     #     sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and bdcdyh='" + bdcdyh + "'and qlrmc='" + qlrmc + "'"
    #     #     res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
    #     #     print("dj_fdcq2_djben_zs:", res_dj_fdcq2_djben_zs,type(res_dj_fdcq2_djben_zs))
    #     #
    #     #     sql_dj_qlrgl ="select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "'"
    #     #     res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
    #     #     print("dj_qlrgl:", res_dj_qlrgl,type(res_dj_qlrgl))
    #     #
    #     #     sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and ryzl='1'and bdcdyh='"+ bdcdyh +"'and qlrmc='" + qlrmc + "')"
    #     #     res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
    #     #     print("dj_qlr:", res_dj_qlr,type(res_dj_qlr))
    #     #
    #     #     sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'and qlr = '" + qlrmc + "'"
    #     #     res_dj_zs = self.djObj.fetchone(sql_dj_zs)
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
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.djObj.fetchone(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表查询djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfsfcd=0 and  qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and sfsfcd=0 and id='" + res_dj_fdcq2_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if res_dj_fdcq2 and res_dj_hxx and res_dj_fdcq2_djben_zs and res_dj_djben and sql_dj_zs and res_dj_qlrgl and res_dj_qlr :
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)

            sql_dj_jzwqfsyqyzgybf = "select count(1) from dj_jzwqfsyqyzgybf t where zt='1' and sfyx=1 and bz2='" + res_yw_sqxx_ywh + "'"
            res_dj_jzwqfsyqyzgybf = self.djObj.fetchone(sql_dj_jzwqfsyqyzgybf)
            logger.debug("dj_jzwqfsyqyzgybf表查询记录为：%d" % res_dj_jzwqfsyqyzgybf)

            sql_dj_fsssxx = "select count(1) from dj_fsssxx where zt='1' and sfyx=1 and bz2='" + res_yw_sqxx_ywh + "'"
            res_dj_fsssxx = self.djObj.fetchone(sql_dj_fsssxx)
            logger.debug("dj_fsssxx表查询记录为：%d" % res_dj_fsssxx)

            sql_dj_qlrgl ="select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
            logger.debug("cqbid为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.djObj.fetchone(sql_dj_fdcq2_djbid))
            logger.debug("djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询为：%d" %res_dj_fdcq2)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询为：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id =" + res_dj_fdcq2_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询为：%d" %res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询为：%d" %res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            logger.debug("dj_zs表查询为：%d" %res_dj_zs)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and sfdz=1 and sfdh=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
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
                res_yw_sqxxzb_ywh = self.djObj.fetchone(sql_yw_sqxxzb_ywh)
                logger.debug("yw_sqxxzb表ywh：%s" % res_yw_sqxxzb_ywh)
            else:
                logger.error("非按幢发证，请检查yml配置文件sfztfz参数是否配置正确。")
                return

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表id：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zt='1' and sfyx=1  and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2_djbid = str(self.djObj.fetchone(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表djbid：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and sfdz is null and sfdh is null and ywh='" + res_yw_sqxxzb_ywh + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % res_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录数：%d" %res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and sfdz is null and sfdh is null and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录数：%d" %res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdh is null and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录数：%d" %res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id =" + res_dj_fdcq2_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" %res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_fdcq2_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" %res_dj_qlrgl)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and cqbid =" + res_dj_fdcq2_id + ""
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_fdcq2_id = "select id from dj_fdcq2 where zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_id = str(self.djObj.fetchone(sql_dj_fdcq2_id))
            logger.debug("dj_fdcq2表查询id为：%s" % res_dj_fdcq2_id)

            sql_dj_fdcq2_djbid = "select djbid from dj_fdcq2 where zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2_djbid = str(self.djObj.fetchone(sql_dj_fdcq2_djbid))
            logger.debug("dj_fdcq2表查询djbid为：%s" % res_dj_fdcq2_djbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='2' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfzx=1 and sfysczql=0 and id='" + res_dj_fdcq2_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and cqbid='" + res_dj_fdcq2_id + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_dj_fdcq2_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
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

    '''抵押登记'''
    # 抵押(土地、房屋)登记
    def dyRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)

            sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_dy = self.djObj.fetchone(sql_dj_dy)
            logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=1 and sfysczql=1 and id in(select djbid from dj_dy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
            logger.debug("dj_dy_djben_zm表查询记录为：%d"  % res_dj_dy_djben_zm)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            logger.debug("dj_qlr：%d" % res_dj_qlr)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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
            res_fdcq2_id = self.djObj.fetchone(sql_fdcq2_id)
            res_fdcq2_id = str(res_fdcq2_id)
            print("fdcq2_id:", res_fdcq2_id,type(res_fdcq2_id))

            sql_fdcq2_djbid = "select djbid from DJJGK.dj_fdcq2 t where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_fdcq2_djbid = self.djObj.fetchone(sql_fdcq2_djbid)
            res_fdcq2_djbid = str(res_fdcq2_djbid)
            print("fdcq2_djbid:", res_fdcq2_djbid,type(res_fdcq2_djbid))

            sql_dj_dy_id = "select id from DJJGK.DJ_DY where zt='2' and sfyx=1 and cqbid='" + res_fdcq2_id + "'"
            res_dj_dy_id = self.djObj.fetchone(sql_dj_dy_id)
            res_dj_dy_id = str(res_dj_dy_id)
            print("dj_dy_id:", res_dj_dy_id)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=0 and sfysczql=1 and id = '" + res_fdcq2_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            print("dj_djben:", res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdy=0 and qlbid='" + res_fdcq2_id + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            print("dj_fdcq2_djben_zs:", res_dj_fdcq2_djben_zs)

            sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where  qlbid='" + res_fdcq2_id + "'"
            res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
            print("dj_dy_djben_zm:", res_dj_dy_djben_zm)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_dj_dy_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            print("dj_qlrgl:", res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and djbid='" + res_fdcq2_djbid + "'"
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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

    '''预告登记'''
    # 商品房预告登记
    def spfYgRegisterDataCheck(self, bdcdyh, data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        try:
            sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_yg_id = "select id from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_id = str(self.djObj.fetchone(sql_dj_yg_id))
            logger.debug("dj_yg表id：%s" % res_dj_yg_id)

            sql_dj_yg_djbid = "select djbid from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_djbid = str(self.djObj.fetchone(sql_dj_yg_djbid))
            logger.debug("dj_yg表djbid：%s" % res_dj_yg_djbid)

            sql_dj_yg_hid = "select hid from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_hid = str(self.djObj.fetchone(sql_dj_yg_hid))
            logger.debug("dj_yg表hid：%s" % res_dj_yg_hid)

            sql_dj_yg = "select count(1) from dj_yg where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg = self.djObj.fetchone(sql_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and id =" + res_dj_yg_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_yg_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_ychxx = "select count(1) from dj_ychxx where zt='1' and sfyx=1 and id =" + res_dj_yg_hid + ""
            res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
            logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
            logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and djbid =" + res_dj_yg_djbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_ydy_id = "select id from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_id = str(self.djObj.fetchone(sql_dj_ydy_id))
            logger.debug("dj_ydy表id：%s" % res_dj_ydy_id)

            sql_dj_ydy_djbid = "select djbid from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_djbid = str(self.djObj.fetchone(sql_dj_ydy_djbid))
            logger.debug("dj_ydy表djbid：%s" % res_dj_ydy_djbid)

            sql_dj_ydy = "select count(1) from dj_ydy where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy = self.djObj.fetchone(sql_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录数：%d" % res_dj_ydy)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql is null and id =" + res_dj_ydy_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_dj_ydy_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and djbid =" + res_dj_ydy_djbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_yg_id = "select id from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_id = str(self.djObj.fetchone(sql_dj_yg_id))
            logger.debug("dj_yg表id：%s" % res_dj_yg_id)

            sql_dj_yg_djbid = "select djbid from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_djbid = str(self.djObj.fetchone(sql_dj_yg_djbid))
            logger.debug("dj_yg表djbid：%s" % res_dj_yg_djbid)

            sql_dj_yg_hid = "select hid from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg_hid = self.djObj.fetchone(sql_dj_yg_hid)
            logger.debug("dj_yg表hid：%s" % res_dj_yg_hid)

            sql_dj_yg = "select count(1) from dj_yg where zt='2' and sfyx=1 and zxywh='" + res_yw_sqxx_ywh + "'"
            res_dj_yg = self.djObj.fetchone(sql_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfyg = 0 and id =" + res_dj_yg_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_yg_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            if res_dj_yg_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='2' and sfyx=1 and id =" + str(res_dj_yg_hid) + ""
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            # 证明类型（2）-->预告证明
            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and zmlx='2' and djbid =" + res_dj_yg_djbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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
            res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表查询sql：%s" % sql_yw_sqxx_ywh)
            logger.debug("yw_sqxx表ywh：%s" % res_yw_sqxx_ywh)

            sql_dj_ydy_id = "select id from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_id = str(self.djObj.fetchone(sql_dj_ydy_id))
            logger.debug("dj_ydy表id：%s" % res_dj_ydy_id)

            sql_dj_ydy_djbid = "select djbid from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy_djbid = str(self.djObj.fetchone(sql_dj_ydy_djbid))
            logger.debug("dj_ydy表djbid：%s" % res_dj_ydy_djbid)

            sql_dj_ydy = "select count(1) from dj_ydy where zt='2' and sfyx=1 and zxdyywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ydy = self.djObj.fetchone(sql_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录数：%d" % res_dj_ydy)

            # 查询该单元上是否存在其他现势抵押信息
            sql_dj_ydy_count = "select count(1) from dj_ydy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ydy_count = self.djObj.fetchone(sql_dj_ydy_count)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy_count)
            logger.debug("dj_ydy表查询抵押条数：%d" % res_dj_ydy_count)

            # 该单元只有一条抵押信息，登簿后sfydy=0
            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=0 and id =" + res_dj_ydy_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            # 该单元有其他抵押信息，登簿后sfydy=1
            sql_dj_djben2 = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=1 and id =" + res_dj_ydy_djbid + ""
            res_dj_djben2 = self.djObj.fetchone(sql_dj_djben2)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben2)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben2)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_dj_ydy_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            # 证明类型（3）-->预告抵押证明
            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and zmlx='3' and djbid =" + res_dj_ydy_djbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
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

    '''查封登记'''
    # 查封登记
    def cfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_cf_cqbid = "select cqbid from dj_cf where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_cqbid = str(self.djObj.fetchone(sql_dj_cf_cqbid))
            logger.debug("dj_cf表查询cqbid为：%s" % res_dj_cf_cqbid)

            sql_dj_cf_djbid = "select djbid from dj_cf where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_djbid = str(self.djObj.fetchone(sql_dj_cf_djbid))
            logger.debug("dj_cf表查询djbid为：%s" % res_dj_cf_djbid)

            sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=1 and  qlbid='" + res_dj_cf_cqbid + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id='" + res_dj_cf_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

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

    # 土地小证查封
    def landXzcfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_cf_zszbid = "select zszbid from dj_cf where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_zszbid = str(self.djObj.fetchone(sql_dj_cf_zszbid))
            logger.debug("dj_cf表查询zszbid为：%s" % res_dj_cf_zszbid)

            sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)

            sql_dj_zszb = "select count(1) from dj_zszb where zt='1' and sfyx=1 and sfcf=1 and id='" + res_dj_cf_zszbid + "'"
            res_dj_zszb = self.djObj.fetchone(sql_dj_zszb)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_zszb)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_zszb)

            if res_dj_cf and res_dj_zszb:
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

    # 解封登记(净地)
    def landJfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_cf_cqbid = "select cqbid from dj_cf where jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_cqbid = str(self.djObj.fetchone(sql_dj_cf_cqbid))
            logger.debug("dj_cf表查询cqbid为：%s" % res_dj_cf_cqbid)

            sql_dj_cf_djbid = "select djbid from dj_cf where jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_djbid = str(self.djObj.fetchone(sql_dj_cf_djbid))
            logger.debug("dj_cf表查询djbid为：%s" % res_dj_cf_djbid)

            # 过滤小证目前不考虑，因为转数据时会将大小证都刷 即大证dj_cf表中zszbid也可能有值
            # sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and zszbid is null and bdcdyh='" + bdcdyh + "'"
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("当前单元在dj_cf表数据条数为：%s" % res_dj_cf_count)

            sql_dj_dy_count = "select count(1) from dj_dy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_dy_count = self.djObj.fetchone(sql_dj_dy_count)
            logger.debug("dj_dy表查询sql：%s" % sql_dj_dy_count)
            logger.debug("当前单元在dj_dy表数据条数为：%s" % res_dj_dy_count)

            sql_dj_cf = "select count(1) from dj_cf where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            # logger.debug("通过解封业务号查询到当前数据条数为：%s" %res_dj_cf)

            sql_dj_djben_sfcf = "select sfcf from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_cf_djbid + "'"
            res_dj_djben_sfcf = self.djObj.fetchone(sql_dj_djben_sfcf)
            logger.debug("dj_djben表查询查封状态sql：%s" % sql_dj_djben_sfcf)
            logger.debug("dj_djben表查询到该笔业务sfcf状态为数据：%d" % res_dj_djben_sfcf)

            sql_dj_djben_sfdy = "select sfdy from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_cf_djbid + "'"
            res_dj_djben_sfdy = self.djObj.fetchone(sql_dj_djben_sfdy)
            logger.debug("dj_djben表查询抵押状态sql：%s" % sql_dj_djben_sfdy)
            logger.debug("dj_djben表查询到该笔业务sfdy状态为数据：%d" % res_dj_djben_sfdy)

            if res_dj_dy_count:
                sql_dj_dy_djben_zm_sfcf = "select sfcf from dj_dy_djben_zm where sfyx=1 and djbid='" + res_dj_cf_djbid + "'"
                res_dj_dy_djben_zm_sfcf = self.djObj.fetchone(sql_dj_dy_djben_zm_sfcf)
                logger.debug("dj_dy_djben_zm表查询查封状态sql：%s" % sql_dj_dy_djben_zm_sfcf)
                logger.debug("dj_dy_djben_zm表查询到该笔业务sfcf状态为数据：%d" % res_dj_dy_djben_zm_sfcf)

                sql_dj_dy_djben_zm_sfdy = "select sfdy from dj_dy_djben_zm where sfyx=1 and djbid='" + res_dj_cf_djbid + "'"
                res_dj_dy_djben_zm_sfdy = self.djObj.fetchone(sql_dj_dy_djben_zm_sfdy)
                logger.debug("dj_dy_djben_zm表查询抵押状态sql：%s" % sql_dj_dy_djben_zm_sfdy)
                logger.debug("dj_dy_djben_zm表查询到该笔业务sfdy状态为数据：%d" % res_dj_dy_djben_zm_sfdy)

            if res_dj_cf_count >= 1:
                # 存在抵押，多条查封 -->解封后dj_djben,dj_dy_djben_zm表sfdy=1，sfcf=1
                if res_dj_dy_count:
                    if res_dj_cf and res_dj_djben_sfcf ==1 and res_dj_djben_sfdy ==1 and res_dj_dy_djben_zm_sfcf == 1 and res_dj_dy_djben_zm_sfdy == 1:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 不存在抵押，多条查封 -->解封后dj_djben表sfdy=0，sfcf=1
                else:
                    if res_dj_cf and res_dj_djben_sfcf ==1 and res_dj_djben_sfdy ==0 :
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
            else:
                # 存在抵押，1条查封 -->解封后dj_djben,dj_dy_djben_zm表sfdy=1，sfcf=0
                if res_dj_dy_count:
                    if res_dj_cf and res_dj_djben_sfcf == 0 and res_dj_djben_sfdy == 1  and res_dj_dy_djben_zm_sfcf == 0 and res_dj_dy_djben_zm_sfdy == 1:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 不存在抵押，1条查封 -->解封后dj_djben表sfdy=0，sfcf=0
                else:
                    if res_dj_cf and res_dj_djben_sfcf == 0 and res_dj_djben_sfdy == 0:
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

    # 解封登记(房地)
    def houseJfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_cf_cqbid = "select cqbid from dj_cf where jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_cqbid = str(self.djObj.fetchone(sql_dj_cf_cqbid))
            logger.debug("dj_cf表查询cqbid为：%s" % res_dj_cf_cqbid)

            sql_dj_cf_djbid = "select djbid from dj_cf where jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf_djbid = str(self.djObj.fetchone(sql_dj_cf_djbid))
            logger.debug("dj_cf表查询djbid为：%s" % res_dj_cf_djbid)

            # 过滤小证目前不考虑，因为转数据时会将大小证都刷 即大证dj_cf表中zszbid也可能有值
            # sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and zszbid is null and bdcdyh='" + bdcdyh + "'"
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("当前单元在dj_cf表数据条数为：%s" % res_dj_cf_count)

            sql_dj_dy_count = "select count(1) from dj_dy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_dy_count = self.djObj.fetchone(sql_dj_dy_count)
            logger.debug("dj_dy表查询sql：%s" % sql_dj_dy_count)
            logger.debug("当前单元在dj_dy表数据条数为：%s" % res_dj_dy_count)

            sql_dj_cf = "select count(1) from dj_cf where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            # logger.debug("通过解封业务号查询到当前数据条数为：%s" %res_dj_cf)

            sql_dj_djben_sfcf = "select sfcf from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_cf_djbid + "'"
            res_dj_djben_sfcf = self.djObj.fetchone(sql_dj_djben_sfcf)
            logger.debug("dj_djben表查询查封状态sql：%s" % sql_dj_djben_sfcf)
            logger.debug("dj_djben表查询到该笔业务sfcf状态为数据：%d" % res_dj_djben_sfcf)

            sql_dj_djben_sfdy = "select sfdy from dj_djben where zt='1' and sfyx=1 and id='" + res_dj_cf_djbid + "'"
            res_dj_djben_sfdy = self.djObj.fetchone(sql_dj_djben_sfdy)
            logger.debug("dj_djben表查询抵押状态sql：%s" % sql_dj_djben_sfdy)
            logger.debug("dj_djben表查询到该笔业务sfdy状态为数据：%d" % res_dj_djben_sfdy)

            sql_dj_fdcq2_djben_zs_sfcf = "select sfcf from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_dj_cf_cqbid + "'"
            res_dj_fdcq2_djben_zs_sfcf = self.djObj.fetchone(sql_dj_fdcq2_djben_zs_sfcf)
            logger.debug("dj_fdcq2_djben_zs表查询查封状态sql：%s" % sql_dj_fdcq2_djben_zs_sfcf)
            logger.debug("dj_fdcq2_djben_zs表查询到该笔业务sfcf状态为数据：%d" % res_dj_fdcq2_djben_zs_sfcf)

            sql_dj_fdcq2_djben_zs_sfdy = "select sfdy from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_dj_cf_cqbid + "'"
            res_dj_fdcq2_djben_zs_sfdy = self.djObj.fetchone(sql_dj_fdcq2_djben_zs_sfdy)
            logger.debug("dj_fdcq2_djben_zs表查询抵押状态sql：%s" % sql_dj_fdcq2_djben_zs_sfdy)
            logger.debug("dj_fdcq2_djben_zs表查询到该笔业务sfdy状态为数据：%d" % res_dj_fdcq2_djben_zs_sfdy)

            if res_dj_dy_count:
                sql_dj_dy_djben_zm_sfcf = "select sfcf from dj_dy_djben_zm where sfyx=1 and djbid='" + res_dj_cf_djbid + "'"
                res_dj_dy_djben_zm_sfcf = self.djObj.fetchone(sql_dj_dy_djben_zm_sfcf)
                logger.debug("dj_dy_djben_zm表查询查封状态sql：%s" % sql_dj_dy_djben_zm_sfcf)
                logger.debug("dj_dy_djben_zm表查询到该笔业务sfcf状态为数据：%d" % res_dj_dy_djben_zm_sfcf)

                sql_dj_dy_djben_zm_sfdy = "select sfdy from dj_dy_djben_zm where sfyx=1 and djbid='" + res_dj_cf_djbid + "'"
                res_dj_dy_djben_zm_sfdy = self.djObj.fetchone(sql_dj_dy_djben_zm_sfdy)
                logger.debug("dj_dy_djben_zm表查询抵押状态sql：%s" % sql_dj_dy_djben_zm_sfdy)
                logger.debug("dj_dy_djben_zm表查询到该笔业务sfdy状态为数据：%d" % res_dj_dy_djben_zm_sfdy)

            if res_dj_cf_count >= 1:
                # 存在抵押，多条查封 -->解封后dj_djben,dj_fdcq2_djben_zs,dj_dy_djben_zm表sfdy=1，sfcf=1
                if res_dj_dy_count:
                    if res_dj_cf and res_dj_djben_sfcf ==1 and res_dj_djben_sfdy ==1 and res_dj_fdcq2_djben_zs_sfcf ==1 and res_dj_fdcq2_djben_zs_sfdy ==1 and res_dj_dy_djben_zm_sfcf == 1 and res_dj_dy_djben_zm_sfdy == 1:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 不存在抵押，多条查封 -->解封后dj_djben,dj_fdcq2_djben_zs表sfdy=0，sfcf=1
                else:
                    if res_dj_cf and res_dj_djben_sfcf ==1 and res_dj_djben_sfdy ==0 and res_dj_fdcq2_djben_zs_sfcf ==1 and res_dj_fdcq2_djben_zs_sfdy ==0:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
            else:
                # 存在抵押，1条查封 -->解封后dj_djben,dj_fdcq2_djben_zs,dj_dy_djben_zm表sfdy=1，sfcf=0
                if res_dj_dy_count:
                    if res_dj_cf and res_dj_djben_sfcf == 0 and res_dj_djben_sfdy == 1 and res_dj_fdcq2_djben_zs_sfcf == 0 and res_dj_fdcq2_djben_zs_sfdy == 1 and res_dj_dy_djben_zm_sfcf == 0 and res_dj_dy_djben_zm_sfdy == 1:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 不存在抵押，1条查封 -->解封后dj_djben,dj_fdcq2_djben_zs表sfdy=0，sfcf=0
                else:
                    if res_dj_cf and res_dj_djben_sfcf == 0 and res_dj_djben_sfdy == 0 and res_dj_fdcq2_djben_zs_sfcf == 0 and res_dj_fdcq2_djben_zs_sfdy == 0:
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

    # 预查封登记/预售合同查封/续预查封（针对首封）
    def ycfRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_ycf_djbid = "select djbid from dj_ycf where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ycf_djbid = str(self.djObj.fetchone(sql_dj_ycf_djbid))
            logger.debug("dj_ycf表查询djbid为：%s" % res_dj_ycf_djbid)

            # 首查封(包括首查封续查封)，查封顺序cfsx=1,cflx=3(预查封)
            sql_dj_ycf = "select count(1) from dj_ycf t where cflx=3 and cfsx=1 and zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_ycf = self.djObj.fetchone(sql_dj_ycf)
            logger.debug("dj_ycf表查询sql：%s" % sql_dj_ycf)
            logger.debug("dj_ycf表查询记录为：%d" % res_dj_ycf)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfycf=1 and id='" + res_dj_ycf_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

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
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # 判断dj_ycf有几条现势数据
            sql_dj_ycf_count = "select count(1) from dj_ycf t where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ycf_count = self.djObj.fetchone(sql_dj_ycf_count)
            logger.debug("dj_ycf表查询到共%s条现势数据" %res_dj_ycf_count)

            if res_dj_ycf_count > 1:
                # 轮候查封  cflx=4(轮候查封)，cfsx根据dj_ycf现势数据计算
                sql_dj_ycf = "select count(1) from dj_ycf t where cflx=4 and zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "' and  cfsx='" + res_dj_ycf_count + "'"
                res_dj_ycf = self.djObj.fetchone(sql_dj_ycf)
                logger.debug("dj_ycf表查询到该笔业务数据：%s" % res_dj_ycf)


            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfycf=1 and id in(select djbid from dj_ycf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "')"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
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

    # 司法裁定(房屋)
    def houseSfcdRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        ywxl = data.get('initdata').get('params', None).get('ywxl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_qtxz_cqbid = "select cqbid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_cqbid = str(self.djObj.fetchone(sql_dj_qtxz_cqbid))
            logger.debug("dj_qtxz表查询cqbid为：%s" % res_dj_qtxz_cqbid)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.djObj.fetchone(sql_dj_qtxz_djbid))
            logger.debug("dj_qtxz表查询djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz_cfid = "select cfid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_cfid = str(self.djObj.fetchone(sql_dj_qtxz_cfid))
            logger.debug("dj_qtxz表查询cfid为：%s" % res_dj_qtxz_cfid)

            sql_dj_qtxz_dyid = "select dyid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_dyid = str(self.djObj.fetchone(sql_dj_qtxz_dyid))
            logger.debug("dj_qtxz表查询dyid为：%s" % res_dj_qtxz_dyid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and xzlxmc='司法裁定'and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.djObj.fetchone(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询sql：%s" % sql_dj_qtxz)
            logger.debug("dj_qtxz表查询记录为：%d" % res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and sfdy=1  and sfsfcd=1 and id='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_djben2 = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and sfdy=0 and sfsfcd=1 and id='" + res_dj_qtxz_djbid + "'"
            res_dj_djben2 = self.djObj.fetchone(sql_dj_djben2)
            logger.debug("dj_djben2表查询sql：%s" % sql_dj_djben2)
            logger.debug("dj_djben2表查询记录为：%d" % res_dj_djben2)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=0  and sfdy=1 and sfsfcd=1 and  qlbid='" + res_dj_qtxz_cqbid + "'"
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_fdcq2_djben_zs2 = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=0 and  sfdy=0 and sfsfcd=1 and qlbid='" + res_dj_qtxz_cqbid + "'"
            res_dj_fdcq2_djben_zs2 = self.djObj.fetchone(sql_dj_fdcq2_djben_zs2)
            logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs2)
            logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs2)

            if ywxl == '法院拍卖解封':
                sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfcf=0 and  djbid='" + res_dj_qtxz_djbid + "'"
                res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

            if res_dj_qtxz_cfid:
                # 抵押和查封都需解除
                if ywxl == '司法裁定':
                    if res_dj_qtxz and res_dj_djben2 and res_dj_fdcq2_djben_zs2:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 只解查封，抵押不解
                elif ywxl == '法院拍卖解封':
                    # 无抵押，无需查询抵押宽表
                    if not res_dj_dy_djben_zm:
                        if res_dj_qtxz and res_dj_djben2 and res_dj_fdcq2_djben_zs2:
                            logger.debug("数据库数据归档正确")
                            return True
                        else:
                            logger.error("数据库数据归档错误")
                            return False
                    # 有抵押 ，需查询抵押宽表
                    else:
                        if res_dj_qtxz and res_dj_djben and res_dj_fdcq2_djben_zs and res_dj_dy_djben_zm:
                            logger.debug("数据库数据归档正确")
                            return True
                        else:
                            logger.error("数据库数据归档错误")
                            return False
                else:
                    logger.error("业务小类（ywxl）未获取到，请检查！")
                    return
            else:
                logger.error("dj_qtxz表cfid字段为空，该业务办件数据不符合要求，请检查！")
        except Exception as e:
                logger.error("数据检查异常",e)
        finally:
            # 关闭数据库连接
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()

    # 司法裁定(净地)
    def landSfcdRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        ywxl = data.get('initdata').get('params', None).get('ywxl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_qtxz_cqbid = "select cqbid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_cqbid = str(self.djObj.fetchone(sql_dj_qtxz_cqbid))
            logger.debug("dj_qtxz表查询cqbid为：%s" % res_dj_qtxz_cqbid)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.djObj.fetchone(sql_dj_qtxz_djbid))
            logger.debug("dj_qtxz表查询djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz_cfid = "select cfid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_cfid = str(self.djObj.fetchone(sql_dj_qtxz_cfid))
            logger.debug("dj_qtxz表查询cfid为：%s" % res_dj_qtxz_cfid)

            sql_dj_qtxz_dyid = "select dyid from dj_qtxz where ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_dyid = str(self.djObj.fetchone(sql_dj_qtxz_dyid))
            logger.debug("dj_qtxz表查询dyid为：%s" % res_dj_qtxz_dyid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and xzlxmc='司法裁定（净地）'and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.djObj.fetchone(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询sql：%s" % sql_dj_qtxz)
            logger.debug("dj_qtxz表查询记录为：%d" % res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and sfdy=1  and sfsfcd=1 and id='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_djben2 = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and sfdy=0 and sfsfcd=1 and id='" + res_dj_qtxz_djbid + "'"
            res_dj_djben2 = self.djObj.fetchone(sql_dj_djben2)
            logger.debug("dj_djben2表查询sql：%s" % sql_dj_djben2)
            logger.debug("dj_djben2表查询记录为：%d" % res_dj_djben2)

            if ywxl == '法院拍卖解封':
                sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfcf=0 and  djbid='" + res_dj_qtxz_djbid + "'"
                res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

            if res_dj_qtxz_cfid:
                # 抵押和查封都需解除
                if ywxl == '司法裁定':
                    if res_dj_qtxz and res_dj_djben2:
                        logger.debug("数据库数据归档正确")
                        return True
                    else:
                        logger.error("数据库数据归档错误")
                        return False
                # 只解查封，抵押不解
                elif ywxl == '法院拍卖解封':
                    # 无抵押，无需查询抵押宽表
                    if not res_dj_dy_djben_zm:
                        if res_dj_qtxz and res_dj_djben2 :
                            logger.debug("数据库数据归档正确")
                            return True
                        else:
                            logger.error("数据库数据归档错误")
                            return False
                    # 有抵押 ，需查询抵押宽表
                    else:
                        if res_dj_qtxz and res_dj_djben and res_dj_dy_djben_zm:
                            logger.debug("数据库数据归档正确")
                            return True
                        else:
                            logger.error("数据库数据归档错误")
                            return False
                else:
                    logger.error("业务小类（ywxl）未获取到，请检查！")
                    return
            else:
                logger.error("dj_qtxz表cfid字段为空，该业务办件数据不符合要求，请检查！")
                return
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
    #         res_dj_cf = self.djObj.fetchone(sql_dj_cf)
    #         print("dj_cf:", res_dj_cf)
    #
    #         sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id in(select djbid from dj_cf where bdcdyh='" + bdcdyh + "')"
    #         res_dj_djben = self.djObj.fetchone(sql_dj_djben)
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
    '''其他登记'''
    # 冻结登记
    def djRegisterDataCheck(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxxzb t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            sql_dj_qtxz_id = "select id from dj_qtxz where zt='1' and sfyx=1 and xzlx='5' and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_id = str(self.djObj.fetchone(sql_dj_qtxz_id))
            logger.debug("cqbid为：%s" % res_dj_qtxz_id)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where zt='1' and sfyx=1 and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.djObj.fetchone(sql_dj_qtxz_djbid))
            logger.debug("djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and xzlx='5' and ywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.djObj.fetchone(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询到该笔业务数据：%s" %res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdj=1 and sfqtxz =1 and  id ='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdj=1 and qlbid =" + res_dj_qtxz_id + ""
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
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
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxx_ywh)
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" %res_yw_sqxx_ywh)

            # sql_dj_qtxz_id = "select id from dj_qtxz where zt='2' and sfyx=1 and xzlx='5' and jfywh='" + res_yw_sqxx_ywh + "'"
            # res_dj_qtxz_id = str(self.djObj.fetchone(sql_dj_qtxz_id))
            # logger.debug("cqbid为：%s" % res_dj_qtxz_id)

            sql_dj_qtxz_djbid = "select djbid from dj_qtxz where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz_djbid = str(self.djObj.fetchone(sql_dj_qtxz_djbid))
            logger.debug("djbid为：%s" % res_dj_qtxz_djbid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='2' and sfyx=1 and jfywh='" + res_yw_sqxx_ywh + "'"
            res_dj_qtxz = self.djObj.fetchone(sql_dj_qtxz)
            logger.debug("dj_qtxz表查询到该笔业务数据：%s" %res_dj_qtxz)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdj=0 and sfqtxz =0 and sfnbxz=0  and  id ='" + res_dj_qtxz_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            logger.debug("dj_djben表查询到该笔业务数据：%s" %res_dj_djben)

            sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdj=0 and bdcdyh =" + bdcdyh + ""
            res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
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


