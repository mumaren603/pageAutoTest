'''
用于业务登簿后数据库结果检查
'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.LogFunc import loggerConf
from Common.DataRegisterCheck import registerCheck

logger = loggerConf().getLogger()

class dataResCheck():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    '''>>>>>>>>>>>>产权类<<<<<<<<<<<<'''
    # 净地登记
    def landRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getLandCqRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 净地注销登记
    def landCancelRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getLandCqCancelRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 房屋登记
    def houseRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getHouseCqRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

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

    # 建筑物区分业主共有部分
    def jzwqfyzgybfRegisterDataCheck(self,bdcdyh,data):
        # 传参BDCDYH是幢BDCDYH,YW_SQXX查询的是净地BDCDYH，故需转换
        bdcdyh = bdcdyh.replace(bdcdyh[19:], 'W00000000')
        res = registerCheck().getJzwqfyzgybfCqRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 项目类多幢登记(整体发证)
    def xmldzRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getHouseCqRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    def xmldzRegisterDataCheck2(self,bdcdyh,data):
        res = registerCheck().getHouseCqRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 房屋注销登记
    def houseCancelRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getHouseCqCancelRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    '''>>>>>>>>>>>>抵押类<<<<<<<<<<<<'''
    # 抵押(土地、房屋)登记
    def dyRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getDyRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 不动产抵押注销
    def dyCancelRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getDyCancelRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    '''>>>>>>>>>>>>预告类<<<<<<<<<<<<'''
    # 预告登记
    def ygRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getYgRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 预告抵押
    def ydyRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getYdyRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 预告注销
    def ygCancelRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getYgCancelRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 预抵押注销
    def ydyCancelRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getYdyCancelRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    '''>>>>>>>>>>>>查封类<<<<<<<<<<<<'''
    # 查封(土地、房屋)登记
    def cfRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getCfRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 预查封，批量预查封
    def ycfRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getYcfRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 司法裁定（逻辑包括净地和房地）
    def sfcdRegisterDataCheck(self, bdcdyh, data):
        res = registerCheck().getSfcdRegisterRes(bdcdyh,data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 司法裁定(房屋)(改造完作废)
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

    # 司法裁定(净地)(改造完作废)
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

    # 土地小证查封
    def xzcfRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getXzcfRegisterRes(bdcdyh, data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 解封登记(净地和房地)
    def jfRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getJfRegisterRes(bdcdyh, data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    # 解封登记(小证)
    def xzJfRegisterDataCheck(self,bdcdyh,data):
        res = registerCheck().getXzjfRegisterRes(bdcdyh, data)
        for i in res:
            if not i:
                logger.error("数据库数据归档错误。")
                return False
        logger.debug("数据库数据归档正确。")
        return True

    '''>>>>>>>>>>>>其他类<<<<<<<<<<<<'''
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

    # 解冻登记
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


