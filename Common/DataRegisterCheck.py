'''
登簿数据检查
'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.BusinessRelation import relation
from Common.LogFunc import loggerConf
import sys

logger = loggerConf().getLogger()
rs = relation()

class registerCheck():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    '''>>>>>>>>>>>>产权类<<<<<<<<<<<<'''
    # 净地产权登簿检查
    def getLandCqRegisterRes(self,bdcdyh,data):
        sfcd = data.get('initdata').get('params', None).get('sfcd', None)

        resList = []
        try:
            res_cqbid, res_djbid, res_zsbid = rs.getCqRealtionData(bdcdyh, data)
            res_cqbid = str(res_cqbid)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and id='" + res_cqbid + "'"
            res_dj_jsydsyq = self.djObj.fetchone(sql_dj_jsydsyq)
            resList.append(res_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and djbid='" + res_djbid + "'"
            res_dj_tdxx = self.djObj.fetchone(sql_dj_tdxx)
            resList.append(res_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.djObj.fetchone(sql_dj_zdjbxx)
            resList.append(res_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            # 考虑司法裁定流程，dj_djben检查条件有点不同
            if sfcd == 1:  # 司法裁定
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and sfcf = 0 and sfsfcd=0 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)
            else:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            if not sfcd:
                sql_dj_djb = "select count(1) from dj_djb  where  zt='1'and sfyx=1 and id in(select djbuid from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_djbid + "')"
                res_dj_djb = self.djObj.fetchone(sql_dj_djb)
                resList.append(res_dj_djb)
                logger.debug("dj_djb表查询sql：%s" % sql_dj_djb)
                logger.debug("dj_djb表查询记录数：%d" % res_dj_djb)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            resList.append(res_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_cqbid + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_cqbid + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            resList.append(res_dj_qlr)
            logger.debug("dj_qlr表查询sql：%s" % sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 净地产权注销登簿检查
    def getLandCqCancelRegisterRes(self,bdcdyh,data):
        resList = []
        try:
            res_cqbid, res_djbid, res_zsbid = rs.getCqCancelRealtionData(bdcdyh, data)
            res_cqbid = str(res_cqbid)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)

            sql_dj_jsydsyq = "select count(1) from dj_jsydsyq where zt='2' and sfyx=1 and id='" + res_cqbid + "'"
            res_dj_jsydsyq = self.djObj.fetchone(sql_dj_jsydsyq)
            resList.append(res_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询sql：%s" % sql_dj_jsydsyq)
            logger.debug("dj_jsydsyq表查询记录数：%d" % res_dj_jsydsyq)

            sql_dj_tdxx = "select count(1) from dj_tdxx where zt='2' and sfyx=1 and djbid='" + res_djbid + "'"
            res_dj_tdxx = self.djObj.fetchone(sql_dj_tdxx)
            resList.append(res_dj_tdxx)
            logger.debug("dj_tdxx表查询sql：%s" % sql_dj_tdxx)
            logger.debug("dj_tdxx表查询记录数：%d" % res_dj_tdxx)

            sql_dj_zdjbxx = "select count(1) from dj_zdjbxx where zt='2' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_zdjbxx = self.djObj.fetchone(sql_dj_zdjbxx)
            resList.append(res_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询sql：%s" % sql_dj_zdjbxx)
            logger.debug("dj_zdjbxx表查询记录数：%d" % res_dj_zdjbxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfzx=1 and sfysczql=0 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            resList.append(res_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录数：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_cqbid + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_cqbid + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            resList.append(res_dj_qlr)
            logger.debug("dj_qlr表查询sql：%s" % sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 房地产权登簿检查
    def getHouseCqRegisterRes(self,bdcdyh,data):
        sfcd = data.get('initdata').get('params', None).get('sfcd', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)

        resList = []
        try:
            res_cqbid, res_djbid, res_zsbid = rs.getCqRealtionData(bdcdyh, data)
            res_cqbid = str(res_cqbid)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)

            # 项目类多幢（整体发证）
            if sfztfz == 1:
                sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and sfdz=1 and sfdh =1 and id='" + res_cqbid + "'"
                res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
                resList.append(res_dj_fdcq2)
                logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
                logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

                sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and sfdz=1 and sfdh=1 and cqbid =" + res_cqbid + ""
                res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
                resList.append(res_dj_hxx)
                logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
                logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)
            # 项目类多幢（按幢发证） 或 一般房地流程
            else:
                sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and id='" + res_cqbid + "'"
                res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
                resList.append(res_dj_fdcq2)
                logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
                logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

                sql_dj_hxx = "select count(1) from dj_hxx where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "'"
                res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
                resList.append(res_dj_hxx)
                logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
                logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            # 考虑司法裁定流程，dj_djben检查条件有点不同
            if sfcd == 1:  # 司法裁定
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and sfcf = 0 and sfsfcd=0 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

                sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfsfcd=0 and qlbid='" + res_cqbid + "'"
                res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                resList.append(res_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)
            else:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

                sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and qlbid='" + res_cqbid + "'"
                res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                resList.append(res_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_zs = "select count(1) from dj_zs where zt='1' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            resList.append(res_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_cqbid + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_cqbid + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            resList.append(res_dj_qlr)
            logger.debug("dj_qlr表查询sql：%s" % sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 房地产权注销登簿检查
    def getHouseCqCancelRegisterRes(self,bdcdyh,data):
        resList = []
        try:
            res_cqbid, res_djbid, res_zsbid = rs.getCqCancelRealtionData(bdcdyh, data)
            res_cqbid = str(res_cqbid)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)

            sql_dj_fdcq2 = "select count(1) from dj_fdcq2 where zt='2' and sfyx=1 and id='" + res_cqbid + "'"
            res_dj_fdcq2 = self.djObj.fetchone(sql_dj_fdcq2)
            resList.append(res_dj_fdcq2)
            logger.debug("dj_fdcq2表查询sql：%s" % sql_dj_fdcq2)
            logger.debug("dj_fdcq2表查询记录为：%d" % res_dj_fdcq2)

            sql_dj_hxx = "select count(1) from dj_hxx where zt='2' and sfyx=1 and cqbid='" + res_cqbid + "'"
            res_dj_hxx = self.djObj.fetchone(sql_dj_hxx)
            resList.append(res_dj_hxx)
            logger.debug("dj_hxx表查询sql：%s" % sql_dj_hxx)
            logger.debug("dj_hxx表查询记录为：%d" % res_dj_hxx)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=0 and sfzx=1 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_zs = "select count(1) from dj_zs where zt='2' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zs = self.djObj.fetchone(sql_dj_zs)
            resList.append(res_dj_zs)
            logger.debug("dj_zs表查询sql：%s" % sql_dj_zs)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_cqbid + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_qlr = "select count(1) from dj_qlr where zt='1' and sfyx=1 and id in (select ryqkid from dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_cqbid + "')"
            res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
            resList.append(res_dj_qlr)
            logger.debug("dj_qlr表查询sql：%s" % sql_dj_qlr)
            logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 建筑物区分业务共有部分登簿检查
    def getJzwqfyzgybfCqRegisterRes(self,bdcdyh,data):
        res_ywh = rs.getYwh(bdcdyh,data)

        if res_ywh:
            resList = []
            try:
                sql_dj_jzwqfsyqyzgybf = "select count(1) from dj_jzwqfsyqyzgybf t where zt='1' and sfyx=1 and bz2='" + res_ywh + "'"
                res_dj_jzwqfsyqyzgybf = self.djObj.fetchone(sql_dj_jzwqfsyqyzgybf)
                resList.append(res_dj_jzwqfsyqyzgybf)
                logger.debug("dj_jzwqfsyqyzgybf表查询sql：%s" % sql_dj_jzwqfsyqyzgybf)
                logger.debug("dj_jzwqfsyqyzgybf表查询记录为：%d" % res_dj_jzwqfsyqyzgybf)

                sql_dj_fsssxx = "select count(1) from dj_fsssxx where zt='1' and sfyx=1 and bz2='" + res_ywh + "'"
                res_dj_fsssxx = self.djObj.fetchone(sql_dj_fsssxx)
                resList.append(res_dj_fsssxx)
                logger.debug("dj_fsssxx表查询sql：%s" % sql_dj_fsssxx)
                logger.debug("dj_fsssxx表查询记录为：%d" % res_dj_fsssxx)

                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and bdcdyh='" + bdcdyh + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

                sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_ywh + "'"
                res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
                resList.append(res_dj_qlrgl)
                logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
                logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

                sql_dj_qlr = "select count(1) from dj_qlr where id in(select ryqkid from dj_qlrgl where zt='1' and sfyx=1 and  ywh='" + res_ywh + "')"
                res_dj_qlr = self.djObj.fetchone(sql_dj_qlr)
                resList.append(res_dj_qlr)
                logger.debug("dj_qlr表查询sql：%s" % sql_dj_qlr)
                logger.debug("dj_qlr表查询记录为：%d" % res_dj_qlr)

                if not resList:
                    logger.error("查询结果为空，请检查！")
                    sys.exit(-1)
                return resList

            except Exception as e:
                logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
                sys.exit(-1)
        else:
            logger.error("未查询到YWH，请检查SQL语法是否正确。")
            sys.exit(-1)

    '''>>>>>>>>>>>>抵押类<<<<<<<<<<<<'''
    # 抵押登簿检查
    def getDyRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_cqbid = rs.getDyRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_cqbid = str(res_cqbid)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=1 and id ='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            if sfpl == 1:
                # 整体发证
                if sfztfz == 1:
                    sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and sfztfz=1 and id='" + res_id + "'"
                    res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                    resList.append(res_dj_dy)
                    logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                    logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and sfztfz=1 and qlbid='" + res_id + "'"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)
                # 按单元发证
                else:
                    sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and sfztfz=0 and id='" + res_id + "'"
                    res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                    resList.append(res_dj_dy)
                    logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                    logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and sfztfz=0 and qlbid='" + res_id + "'"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)
            else:
                sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and id='" + res_id + "'"
                res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                resList.append(res_dj_dy)
                logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

                sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and qlbid='" + res_id + "'"
                res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                resList.append(res_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

            # 房地流程需检查产权宽表，净地不涉及
            if cqType == 1:
                sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdy=1 and qlbid='" + res_cqbid + "'"
                res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                resList.append(res_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='1' and sfyx=1 and qlbid='" + res_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 抵押注销登簿检查
    def getDyCancelRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_cqbid = rs.getDyCancelRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_cqbid = str(res_cqbid)

            # 判断抵押数量
            sql_dj_dy_count = "select count(1) from dj_dy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_dy_count = self.djObj.fetchone(sql_dj_dy_count)
            logger.debug("dj_dy表查询sql：%s" % sql_dj_dy_count)
            logger.debug("该单元共存在%d条现势抵押。" % res_dj_dy_count)

            if sfpl == 1:
                # 整体发证
                if sfztfz == 1:
                    sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and sfztfz=1 and id='" + res_id + "'"
                    res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                    resList.append(res_dj_dy)
                    logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                    logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and sfztfz=1 and qlbid='" + res_id + "'"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)
                # 按单元发证
                else:
                    sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and sfztfz=0 and id='" + res_id + "'"
                    res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                    resList.append(res_dj_dy)
                    logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                    logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfdy=1 and sfztfz=0 and qlbid='" + res_id + "'"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)
            else:
                sql_dj_dy = "select count(1) from dj_dy where zt='2' and sfyx=1 and id='" + res_id + "'"
                res_dj_dy = self.djObj.fetchone(sql_dj_dy)
                resList.append(res_dj_dy)
                logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
                logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

            if res_dj_dy_count >=1:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=1 and id ='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

                # 房地流程需检查产权宽表，净地不涉及
                if cqType == 1:
                    sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdy=1 and qlbid='" + res_cqbid + "'"
                    res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                    resList.append(res_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)
            else:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfdy=0 and id ='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

                # 房地流程需检查产权宽表，净地不涉及
                if cqType == 1:
                    sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfdy=0 and qlbid='" + res_cqbid + "'"
                    res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                    resList.append(res_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)


            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>预告类<<<<<<<<<<<<'''
    # 预告登簿检查
    def getYgRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_hid = rs.getYgRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_hid = str(res_hid) if res_hid else None

            sql_dj_yg = "select count(1) from dj_yg where zt='1' and sfyx=1 and id='" + res_id + "'"
            res_dj_yg = self.djObj.fetchone(sql_dj_yg)
            resList.append(res_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfyg=1 and id =" + res_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            if res_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='1' and sfyx=1 and id =" + res_hid + ""
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                resList.append(res_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and id =" + res_zsbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 预告抵押登簿检查
    def getYdyRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_hid = rs.getYdyRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_hid = str(res_hid) if res_hid else None

            sql_dj_ydy = "select count(1) from dj_ydy where zt='1' and sfyx=1 and id='" + res_id + "'"
            res_dj_ydy = self.djObj.fetchone(sql_dj_ydy)
            resList.append(res_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录数：%d" % res_dj_ydy)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfyg=1 and sfydy=1 and id =" + res_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='1' and sfyx=1 and qlbid =" + res_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            if res_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='1' and sfyx=1 and id =" + res_hid + ""
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                resList.append(res_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            sql_dj_zm = "select count(1) from dj_zm where zt='1' and sfyx=1 and id =" + res_zsbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 预告注销登簿检查
    def getYgCancelRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_hid = rs.getYgRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_hid = str(res_hid) if res_hid else None

            sql_dj_yg = "select count(1) from dj_yg where zt='2' and sfyx=1 and id='" + res_id + "'"
            res_dj_yg = self.djObj.fetchone(sql_dj_yg)
            resList.append(res_dj_yg)
            logger.debug("dj_yg表查询sql：%s" % sql_dj_yg)
            logger.debug("dj_yg表查询记录数：%d" % res_dj_yg)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfyg=0 and id =" + res_djbid + ""
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from dj_qlrgl where zt='2' and sfyx=1 and qlbid =" + res_id + ""
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录数：%d" % res_dj_qlrgl)

            if res_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='2' and sfyx=1 and id =" + res_hid + ""
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                resList.append(res_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            # 证明类型（2）-->预告证明
            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and id =" + res_zsbid + ""
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zm表查询记录数：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 预告抵押注销登簿检查
    def getYdyCancelRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)

        resList = []
        try:
            res_id, res_djbid, res_zsbid,res_hid = rs.getYdyRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_zsbid = str(res_zsbid)
            res_hid = str(res_hid) if res_hid else None

            # 判断抵押数量
            sql_dj_ydy_count = "select count(1) from dj_ydy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ydy_count = self.djObj.fetchone(sql_dj_ydy_count)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy_count)
            logger.debug("该单元共存在%d条现势抵押。" % res_dj_ydy_count)

            sql_dj_ydy = "select count(1) from dj_ydy where zt='2' and sfyx=1 and id='" + res_id + "'"
            res_dj_ydy = self.djObj.fetchone(sql_dj_ydy)
            resList.append(res_dj_ydy)
            logger.debug("dj_ydy表查询sql：%s" % sql_dj_ydy)
            logger.debug("dj_ydy表查询记录为：%d" % res_dj_ydy)

            if res_dj_ydy_count >= 1:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=1 and id ='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)
            else:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfydy=0 and id ='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            sql_dj_qlrgl = "select count(1) from  dj_qlrgl where zt='2' and sfyx=1 and qlbid='" + res_id + "'"
            res_dj_qlrgl = self.djObj.fetchone(sql_dj_qlrgl)
            resList.append(res_dj_qlrgl)
            logger.debug("dj_qlrgl表查询sql：%s" % sql_dj_qlrgl)
            logger.debug("dj_qlrgl表查询记录为：%d" % res_dj_qlrgl)

            if res_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='2' and sfyx=1 and id =" + res_hid + ""
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                resList.append(res_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录数：%d" % res_dj_ychxx)

            sql_dj_zm = "select count(1) from dj_zm where zt='2' and sfyx=1 and id='" + res_zsbid + "'"
            res_dj_zm = self.djObj.fetchone(sql_dj_zm)
            resList.append(res_dj_zm)
            logger.debug("dj_zm表查询sql：%s" % sql_dj_zm)
            logger.debug("dj_zs表查询记录为：%d" % res_dj_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>查封类<<<<<<<<<<<<'''
    # 查封登簿检查
    def getCfRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        resList = []
        try:
            res_id, res_djbid, res_cqbid = rs.getCfRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_cqbid = str(res_cqbid)

            # 判断查封数量，如果查封数据只有1条，查询到是首封；如果查封数据大于1条，则是轮候查封。
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("该单元共存在%d条现势查封。" % res_dj_cf_count)
            # 轮候查封
            if res_dj_cf_count > 1:
                sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and cflx='2' and id='" + res_id + "'"
                res_dj_cf = self.djObj.fetchone(sql_dj_cf)
                resList.append(res_dj_cf)
                logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
                logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            # 首封
            elif res_dj_cf_count == 1:
                sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and cflx='1' and id='" + res_id + "'"
                res_dj_cf = self.djObj.fetchone(sql_dj_cf)
                resList.append(res_dj_cf)
                logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
                logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            else:
                logger.error("dj_cf表查询数据为空，请检查")
                sys.exit(-1)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id ='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            # 房地流程需检查产权宽表，净地不涉及
            if cqType == 1:
                sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=1 and qlbid='" + res_cqbid + "'"
                res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                resList.append(res_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            # 抵押宽表验证，若原产权有抵押，查封过后需检查抵押宽表
            sql_dj_dy = "select count(1) from dj_dy where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "'"
            res_dj_dy = self.djObj.fetchone(sql_dj_dy)
            logger.debug("dj_dy表查询sql：%s" % sql_dj_dy)
            logger.debug("dj_dy表查询记录为：%d" % res_dj_dy)

            # 根据dj_dy表qlbid检查dj_dy_djben_zm表
            if res_dj_dy:
                sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and qlbid in (select id from dj_dy where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "')"
                res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)
                if res_dj_dy_djben_zm:
                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfcf=1 and sfdy=1 and qlbid in (select id from dj_dy where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "')"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 预查封登簿检查
    def getYcfRegisterRes(self,bdcdyh,data):
        resList = []
        try:
            res_id, res_djbid, res_cqbid,res_hid = rs.getYcfRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            if res_cqbid:
                res_cqbid = str(res_cqbid)
            if res_hid:
                res_hid = str(res_hid)

            # 判断查封数量，如果查封数据只有1条，查询到是首封；如果查封数据大于1条，则是轮候查封。
            sql_dj_ycf_count = "select count(1) from dj_ycf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_ycf_count = self.djObj.fetchone(sql_dj_ycf_count)
            logger.debug("dj_ycf表查询sql：%s" % sql_dj_ycf_count)
            logger.debug("该单元共存在%d条现势查封。" % res_dj_ycf_count)
            # 轮候查封
            if res_dj_ycf_count > 1:
                sql_dj_ycf = "select count(1) from dj_ycf where zt='1' and sfyx=1 and cflx='4' and id='" + res_id + "'"
                res_dj_ycf = self.djObj.fetchone(sql_dj_ycf)
                resList.append(res_dj_ycf)
                logger.debug("dj_ycf表查询sql：%s" % sql_dj_ycf)
                logger.debug("dj_ycf表查询记录为：%d" % res_dj_ycf)
            # 首封
            elif res_dj_ycf_count == 1:
                sql_dj_ycf = "select count(1) from dj_ycf where zt='1' and sfyx=1 and cflx='3' and id='" + res_id + "'"
                res_dj_ycf = self.djObj.fetchone(sql_dj_ycf)
                resList.append(res_dj_ycf)
                logger.debug("dj_ycf表查询sql：%s" % sql_dj_ycf)
                logger.debug("dj_ycf表查询记录为：%d" % res_dj_ycf)
            else:
                logger.error("dj_ycf表查询数据为空，请检查")
                sys.exit(-1)

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfycf=1 and id ='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            # 目前发现续预查封，dj_ychxx表没数据也可以办理
            if res_hid:
                sql_dj_ychxx = "select count(1) from dj_ychxx where zt='1' and sfyx=1 and id ='" + res_hid + "'"
                res_dj_ychxx = self.djObj.fetchone(sql_dj_ychxx)
                resList.append(res_dj_ychxx)
                logger.debug("dj_ychxx表查询sql：%s" % sql_dj_ychxx)
                logger.debug("dj_ychxx表查询记录为：%d" % res_dj_ychxx)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 司法裁定登簿检查
    def getSfcdRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        resList = []
        try:
            res_id, res_djbid, res_cqbid = rs.getSfcdRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_cqbid = str(res_cqbid)

            sql_dj_qtxz = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and id='" + res_id + "'"
            res_dj_qtxz = self.djObj.fetchone(sql_dj_qtxz)
            resList.append(res_dj_qtxz)
            logger.debug("dj_qtxz表查询sql：%s" % sql_dj_qtxz)
            logger.debug("dj_qtxz表查询记录为：%d" % res_dj_qtxz)

            #无抵押
            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and and sfsfcd=1 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            #有抵押(抵押不解)
            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and sfdy=0 and sfsfcd=1 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            # 后期加上抵押判断
            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0  and sfsfcd=1 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 小证查封登簿检查
    def getXzcfRegisterRes(self,bdcdyh,data):
        ywh = rs.getYwh(bdcdyh,data)
        resList = []

        try:
            sql_dj_cf_zszbid = "select zszbid from dj_cf where ywh='" + ywh + "'"
            res_dj_cf_zszbid = str(self.djObj.fetchone(sql_dj_cf_zszbid))
            logger.debug("dj_cf表查询zszbid为：%s" % res_dj_cf_zszbid)

            # 判断查封数量，如果查封数据只有1条，查询到是首封；如果查封数据大于1条，则是轮候查封。
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and zszbid is not null and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("该单元共存在%d条现势查封。" % res_dj_cf_count)
            # 轮候查封
            if res_dj_cf_count > 1:
                sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and cflx='2' and ywh='" + ywh + "'"
                res_dj_cf = self.djObj.fetchone(sql_dj_cf)
                resList.append(res_dj_cf)
                logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
                logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            # 首封
            elif res_dj_cf_count == 1:
                sql_dj_cf = "select count(1) from dj_cf where zt='1' and sfyx=1 and cflx='1' and ywh='" + ywh + "'"
                res_dj_cf = self.djObj.fetchone(sql_dj_cf)
                resList.append(res_dj_cf)
                logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
                logger.debug("dj_cf表查询记录为：%d" % res_dj_cf)
            else:
                logger.error("dj_cf表查询数据为空，请检查")
                sys.exit(-1)

            sql_dj_zszb = "select count(1) from dj_zszb where zt='1' and sfyx=1 and sfcf=1 and id='" + res_dj_cf_zszbid + "'"
            res_dj_zszb = self.djObj.fetchone(sql_dj_zszb)
            resList.append(res_dj_zszb)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_zszb)
            logger.debug("dj_djben表查询记录为：%d" % res_dj_zszb)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList
        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 房、地解封登簿检查
    def getJfRegisterRes(self,bdcdyh,data):
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        resList = []

        try:
            res_id, res_djbid, res_cqbid = rs.getJfRealtionData(bdcdyh, data)
            res_id = str(res_id)
            res_djbid = str(res_djbid)
            res_cqbid = str(res_cqbid)

            # 判断查封数量
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("该单元共存在%d条现势查封。" % res_dj_cf_count)

            # 判断抵押数量
            sql_dj_dy_count = "select count(1) from dj_dy where zt='1' and sfyx=1 and bdcdyh='" + bdcdyh + "'"
            res_dj_dy_count = self.djObj.fetchone(sql_dj_dy_count)
            logger.debug("dj_dy表查询sql：%s" % sql_dj_dy_count)
            logger.debug("该单元共存在%d条现势抵押。" % res_dj_dy_count)

            sql_dj_cf = "select count(1) from dj_cf where zt='2' and sfyx=1 and id='" + res_id + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            resList.append(res_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("该单元查询到解封历史数据%d条" % res_dj_cf)

            # 解封后单元上还有其他查封
            if res_dj_cf_count >= 1:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=1 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

                # 有抵押
                if res_dj_dy_count:
                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfcf=1 and sfdy=1 and qlbid in (select id from dj_dy where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "')"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

                if cqType == 1:
                    sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=1 and qlbid='" + res_cqbid + "'"
                    res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                    resList.append(res_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)
            # 解封后单元上无其他查封
            else:
                sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfcf=0 and id='" + res_djbid + "'"
                res_dj_djben = self.djObj.fetchone(sql_dj_djben)
                resList.append(res_dj_djben)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_djben)

                # 有抵押，抵押宽表sfcf需置为0
                if res_dj_dy_count:
                    sql_dj_dy_djben_zm = "select count(1) from dj_dy_djben_zm where sfyx=1 and sfcf=0 and qlbid in (select id from dj_dy where zt='1' and sfyx=1 and cqbid='" + res_cqbid + "')"
                    res_dj_dy_djben_zm = self.djObj.fetchone(sql_dj_dy_djben_zm)
                    resList.append(res_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询sql：%s" % sql_dj_dy_djben_zm)
                    logger.debug("dj_dy_djben_zm表查询记录为：%d" % res_dj_dy_djben_zm)

                if cqType == 1:
                    sql_dj_fdcq2_djben_zs = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and sfcf=0 and qlbid='" + res_cqbid + "'"
                    res_dj_fdcq2_djben_zs = self.djObj.fetchone(sql_dj_fdcq2_djben_zs)
                    resList.append(res_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询sql：%s" % sql_dj_fdcq2_djben_zs)
                    logger.debug("dj_fdcq2_djben_zs表查询记录为：%d" % res_dj_fdcq2_djben_zs)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList

        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

    # 小证解封登簿检查
    def getXzjfRegisterRes(self,bdcdyh,data):
        ywh = rs.getYwh(bdcdyh, data)
        resList = []

        try:
            sql_dj_cf_zszbid = "select zszbid from dj_cf where jfywh='" + ywh + "'"
            res_dj_cf_zszbid = str(self.djObj.fetchone(sql_dj_cf_zszbid))
            logger.debug("dj_cf表查询zszbid为：%s" % res_dj_cf_zszbid)

            # 判断查封数量。
            sql_dj_cf_count = "select count(1) from dj_cf where zt='1' and sfyx=1 and zszbid is not null and bdcdyh='" + bdcdyh + "'"
            res_dj_cf_count = self.djObj.fetchone(sql_dj_cf_count)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf_count)
            logger.debug("该单元共存在%d条现势查封。" % res_dj_cf_count)

            sql_dj_cf = "select count(1) from dj_cf where zt='2' and sfyx=1 and zszbid is not null and jfywh='" + ywh + "'"
            res_dj_cf = self.djObj.fetchone(sql_dj_cf)
            resList.append(res_dj_cf)
            logger.debug("dj_cf表查询sql：%s" % sql_dj_cf)
            logger.debug("dj_cf表查询解封记录为：%d" % res_dj_cf)

            if res_dj_cf_count >= 1:
                sql_dj_zszb = "select count(1) from dj_zszb where zt='1' and sfyx=1 and sfcf=1 and id='" + res_dj_cf_zszbid + "'"
                res_dj_zszb = self.djObj.fetchone(sql_dj_zszb)
                resList.append(res_dj_zszb)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_zszb)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_zszb)
            else:
                sql_dj_zszb = "select count(1) from dj_zszb where zt='1' and sfyx=1 and sfcf=0 and id='" + res_dj_cf_zszbid + "'"
                res_dj_zszb = self.djObj.fetchone(sql_dj_zszb)
                resList.append(res_dj_zszb)
                logger.debug("dj_djben表查询sql：%s" % sql_dj_zszb)
                logger.debug("dj_djben表查询记录为：%d" % res_dj_zszb)

            if not resList:
                logger.error("查询结果为空，请检查！")
                sys.exit(-1)
            return resList
        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)


        except Exception as e:
            logger.error("登簿入库检查异常，请检查SQL语法，具体详见：%s" % e)
            sys.exit(-1)

if __name__ == '__main__':
    bdcdyh = '321322100112GB00003F00280015'
    # data = {'initdata': {'lcInfo': {'djlx': '注销登记', 'qllx': '国有建设用地使用权及房屋所有权', 'ywlxID': '7C936E3656FA459DA3EE2F767A18C62F'}, 'params': {'cqType': 1}}}
    data = {'initdata': {
        'lcInfo': {'djlx': '首次登记', 'qllx': '国有建设用地使用权及房屋所有权', 'ywlxID': '608286609F5C429CB32BA42C56F7C7F7'},
        'params': {'cqType': 1, 'sffz': 1, 'sfpl': 1, 'sfztfz': 1}}}

    obj = registerCheck()
    res = obj.getHouseCqRegisterRes(bdcdyh, data)
    print(res,type(res))

