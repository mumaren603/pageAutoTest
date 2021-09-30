'''
数据初始化，即我们测试用例在运行过程中需要使用到数据预先准备好
'''
from Common.logFunc import loggerConf
from dbAction.db import DBAction
import sys

logger = loggerConf().getLogger()

class dataInit():
    def __init__(self,dbInfo):
        self.dbInfo = dbInfo
        self.db_qj_conn = DBAction(self.dbInfo.get('qj'))
        self.db_dj_conn = DBAction(self.dbInfo.get('dj'))

    ####################国有建设用地使用权##################
    # 净地首次登记
    def getLandFirstRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select bdcdyh from dc_djdcbxx where zt='1' and sfyx='0' and tdzl>'0' and qllx='3' and bdcdyh >'0' and qlxz>'0'  and zdmj > '0' and pzmj >'0' and pzytdlbm > '0' and qlrmc > '0' and rownum < 30 order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否在登记平台做过登记,如果做过登记，发起流程会校验住，确保数据在权藉存在，在登记平台未做过登记
            queryJsydsyqSQL = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            queryJsydsyqSQLRes = self.db_dj_conn.SqlExecute(queryJsydsyqSQL)
            if queryJsydsyqSQLRes:
                logger.warning("登记平台该土地信息已登记，重新获取数据！")
                return dataInit(self.dbInfo).getLandFirstRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到权籍有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 净地转移/变更登记
    '''
    def getLandChangeRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_jsydsyq where qllx = '3' and ywh >'0' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh,djbuid from dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id inner join ( select id from dj_djb where zt='1' and sfyx=1) c  on b.djbuid = c.id and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("登记平台该土地信息已登记，重新获取数据！")
            return dataInit(self.dbInfo).getLandChangeRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes
    '''

    # 净地转移/变更登记
    def getLandChangeRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_jsydsyq a,dj_djben b,dj_tdxx c " \
                   "where a.djbid = b.id  " \
                   "and a.id = c.cqbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfsfcd=0 " \
                   "and b.sfcf=0 " \
                   "and b.sfdy=0 " \
                   "and b.sfnbxz=0 " \
                   "and b.sfqtxz=0 " \
                   "and b.sfysczql=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getLandChangeRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到登记有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("登记平台该土地信息已登记，重新获取数据！")
            return dataInit(self.dbInfo).getLandChangeRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 净地裁定过户
    def getLandCdghTransferRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_jsydsyq a,dj_djben b,dj_qtxz c " \
                   "where a.djbid = b.id  " \
                   "and b.id = c.djbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfcf=0 " \
                   "and b.sfsfcd=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and c.srrmc > '0' " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否有多条限制信息
            queryQtxzSQL = "select count(1) from dj_qtxz where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            queryQtxzSQLRes = self.db_dj_conn.SqlExecute(queryQtxzSQL)
            if queryQtxzSQLRes > 1:
                logger.error("根据产权表id查询到多条其他限制信息")
                return dataInit(self.dbInfo).getLandCdghTransferRegisterData()
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getLandCdghTransferRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到登记有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("登记平台该土地信息已登记，重新获取数据！")
            return dataInit(self.dbInfo).getLandChangeRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 土地注销登记数据（没有房屋）
    def getLandCancleRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from djjgk.dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该土地上是否存在现势房产
        queryHouseSQL = "select count(1) from djjgk.dj_fdcq2 where zt='1' and sfyx=1 and zddm='" + queryRes[:19] + "'"
        queryHouseSQLRes = self.db_dj_conn.SqlExecute(queryHouseSQL)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if queryHouseSQLRes:
            logger.warning("该土地上存在现势房产，重新获取数据！")
            return dataInit(self.dbInfo).getLandCancleRegisterData()
        elif querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandCancleRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_dj_conn.closeConn()
            self.db_qj_conn.closeConn()
            return queryRes

    ####################国有建设用地使用权及房屋所有权##################
    # 商品房首次登记
    def getSpfFirstRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from " \
                   "(select bdcdyh, fwbh, lszfwbh " \
                   "from dc_h_fwzk " \
                   "where zt = '1' " \
                   "and sfyx = '0' " \
                   "and fwyt1 > '0' " \
                   "and scjzmj > '0' " \
                   "and bdcdyh like '%GB%' " \
                   "and (fwlx = '1' or fwlx = '2' or fwlx = '3' or fwlx = '4' or fwlx = '99'))a " \
                   "left join " \
                   "(select fwbh " \
                   "from dc_h " \
                   "where zt = '1' " \
                   "and bdcdyh > '0') b " \
                   "on a.fwbh = b.fwbh " \
                   "left join " \
                   "(select zddm, fwbh " \
                   "from dc_z " \
                   "where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh " \
                   "inner join " \
                   "(select zddm " \
                   "from dc_djdcbxx " \
                   "where zt = '1' " \
                   "and sfyx = '1') d " \
                   "on c.zddm = d.zddm  " \
                   "order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否已登记（脏数据检查）
            queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and bdcdyh='" + queryRes + "'"
            queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            if not queryDjbenSQLRes:
                # 检查该数据是否存在待办件
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            else:
                logger.warning("该户存在产权信息，不能做首次登记！重新查询数据")
                return dataInit(self.dbInfo).getSpfFirstRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 自建房屋首次登记
    def getzjfwFirstRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from （select * from dc_h_fwzk where zt = '1' and sfyx = '0' and fwlx = '1' or fwlx = '2' or fwlx = '3'  or fwlx = '4' or fwlx='5' or fwlx='99') a inner join (select * from dc_h where zt = '1') b on a.fwbh = b.fwbh inner join （select * from dc_z where zt = '1') c on a.lszfwbh = c.fwbh inner join (select * from dc_djdcbxx where zt = '1' and sfyx = '1') d on c.zddm = d.zddm where a.bdcdyh like '%GB%' order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        if querySqxxSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getzjfwFirstRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

        # # 检查该数据是否存在土地抵押情况
        # td_bdcdyh = queryRes.replace(queryRes[19:],'W00000000')
        # queryTdDySQL= "select count(1) from dj_dy where zt='1' and sfyx=1 and bdcdyh='"+td_bdcdyh +"'"
        # queryTdDySQLRes = self.db_dj_conn.SqlExecute(queryTdDySQL)
        # # 检查该数据是否存在待办件
        # querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        # querySqxxzbSQL = "select count(1) from ywbdk.yw_sqxxzb where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        # querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        # querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        # if querySqxxSQLRes or querySqxxzbSQLRes:
        #     print("该数据已在办理中，重新获取数据！")
        #     return dataInit(self.dbInfo).getzjfwFirstRegisterData()  # 递归
        # elif queryTdDySQLRes:
        #     print("该数据土地已被抵押，重新获取数据！")
        #     return dataInit(self.dbInfo).getzjfwFirstRegisterData()  # 递归
        # else:
        #     print("数据符合！数据为：%s" % queryRes)
        #     self.db_qj_conn.closeConn()
        #     self.db_dj_conn.closeConn()
        #     return queryRes

    # 公建配套首次登记
    def getJzwqfyzgybfFirstRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct c.bdcdyh " \
                   "from " \
                   "(select fwbh,lszfwbh from dc_h_fwzk " \
                   "where zt = '1' " \
                   "and sfyx = '0' " \
                   "and (fwlx = '9901' or fwlx = '99')) a " \
                   "left join " \
                   "(select fwbh from dc_h " \
                   "where zt = '1' " \
                   "and bdcdyh>'0') b " \
                   "on a.fwbh = b.fwbh " \
                   "left join " \
                   "(select bdcdyh,fwbh,zddm from dc_z where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh " \
                   "left join " \
                   "(select zddm from dc_djdcbxx where zt = '1' and sfyx = '1') d " \
                   "on c.zddm = d.zddm " \
                   "where c.bdcdyh > '0' " \
                   "order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该宗地是否做过登记，未登记不予办理
            zddm = queryRes[:19]
            queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and zddm='" + zddm + "'"
            queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            if queryDjbenSQLRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
            else:
                logger.warning("未查询到净地在登记库现势产权数据")
                return dataInit(self.dbInfo).getJzwqfyzgybfFirstRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 项目类多幢
    def getXmldzFirstRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select bdcdyh from dc_h_fwzk where zt='1' and sfyx='0' and  lszfwbh in("\
                   "select lszfwbh " \
                   "from " \
                   "(select bdcdyh,fwbh,lszfwbh,fwlx from dc_h_fwzk where zt = '1' and sfyx = '0') a " \
                   "left join " \
                   "(select fwbh from dc_h where zt = '1') b " \
                   "on a.fwbh = b.fwbh " \
                   "left join " \
                   "(select fwbh,zddm from dc_z where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh " \
                   "left join " \
                   "(select zddm from dc_djdcbxx where zt = '1' and sfyx = '1') d " \
                   "on c.zddm = d.zddm " \
                   "where  (a.fwlx = 1 or a.fwlx = 2 or a.fwlx = 3 or a.fwlx = 4 or a.fwlx = 5 or a.fwlx = 99) " \
                   "and a.bdcdyh > '0' " \
                   "group by lszfwbh " \
                   "having count(lszfwbh) >1)" \
                   "order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否已登记（脏数据检查）
            queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and bdcdyh='" + queryRes + "'"
            queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            if not queryDjbenSQLRes:
                # 检查该数据是否存在待办件
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getXmldzFirstRegisterData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")

                    # 第二条数据

                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            else:
                logger.warning("该户存在产权信息，不能做首次登记！重新查询数据")
                return dataInit(self.dbInfo).getXmldzFirstRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 项目类多幢2(根据进入流程数据zddm查询另一条数据，在业务办理过程中不动产基本信息页面添加)
    def getXmldzFirstRegisterData2(self,bdcdyh):
        logger.debug(">>>>>查询入参数据start<<<<<")
        zddm = bdcdyh[:19]
        querySQL = "select distinct a.bdcdyh " \
                   "from " \
                   "(select bdcdyh,fwbh,lszfwbh,fwlx from dc_h_fwzk where zt = '1' and sfyx = '0') a " \
                   "left join " \
                   "(select fwbh from dc_h where zt = '1' and bdcdyh>'0') b " \
                   "on a.fwbh = b.fwbh " \
                   "left join " \
                   "(select fwbh,zddm from dc_z where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh " \
                   "left join " \
                   "(select zddm from dc_djdcbxx where zt = '1' and sfyx = '1') d " \
                   "on c.zddm = d.zddm " \
                   "where  (a.fwlx = 1 or a.fwlx = 2 or a.fwlx = 3 or a.fwlx = 4 or a.fwlx = 5 or a.fwlx = 99) " \
                   "and c.zddm ='" + zddm +"'"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询入参ZDDM为：%s" % zddm)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否已登记（脏数据检查）
            queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and bdcdyh='" + queryRes + "'"
            queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            if not queryDjbenSQLRes:
                if queryRes != bdcdyh:
                    # 检查该数据是否存在待办件
                    querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                    querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                    querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                    querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                    if querySqxxSQLRes or querySqxxzbSQLRes:
                        logger.warning("该数据已在办理中，重新获取数据！")
                        return dataInit(self.dbInfo).getXmldzFirstRegisterData2(bdcdyh)
                    else:
                        logger.debug("待登记办件数据-->%s" % queryRes)
                        logger.debug(">>>>>查询入参数据end<<<<<")
                        self.db_qj_conn.closeConn()
                        self.db_dj_conn.closeConn()
                        return queryRes
                else:
                    logger.warning("查询到数据与朱产权数据重复，重新获取数据。")
                    return dataInit(self.dbInfo).getXmldzFirstRegisterData2(bdcdyh)
            else:
                logger.warning("该户存在产权信息，不能做首次登记！重新查询数据")
                return dataInit(self.dbInfo).getXmldzFirstRegisterData2(bdcdyh)
        else:
            logger.error("根据ZDDM未查询到其他户数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    #########################转移登记######################
    #商品房/存量房首次转移登记
    def getSpfOrClfChangeRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from " \
                   "(select * from dj_fdcq2 a " \
                   "where a.qllx=4 " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.bdcdyh not like '%9999%' " \
                   "and a.fwxz='0') a " \
                   "inner join " \
                   "(select * from dj_djben b " \
                   "where b.sfdy=0 " \
                   "and b.sfcf=0 " \
                   "and b.sfyg=0 " \
                   "and b.sfsfcd=0 " \
                   "and b.sfysczql=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1) b " \
                   "on a.djbid=b.id " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            #检查该数据是否有附属设施（3.0版本校验）
            queryFsssSQL = "select id from dj_fsss t where zt='1' and sfyx=1 and ssbdcdyh='" + queryRes + "'"
            queryFsssRes = self.db_dj_conn.SqlExecute(queryFsssSQL)
            if queryFsssRes:
                logger.debug("主产权下存在附属设施信息。")
                queryFsssxxSQL = "select count(1) from dj_fsssxx where cqbid='" + str(queryFsssRes) + "'"
                queryFsssxxRes = self.db_dj_conn.SqlExecute(queryFsssxxSQL)
                if not queryFsssxxRes:
                    logger.error("DJ_FSSSXX表数据为空，不符合业务办理条件，重新查找数据。。")
                    return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")


    # 预转现
    def getYzxRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select bdcdyh from (select bdcdyh,djbid from dj_yg where zt='1' and sfyx=1 and jzmj>'0')a inner join (select id from dj_djben where sfyg=1 and sfydy=0  and sfcf=0 and sfyx=1 and sfysczql=1 and zt='1')b on a.djbid = b.id where bdcdyh > '0' and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getYzxRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")

    # 裁定过户（房屋）
    def getCdghChangeRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL =  "select a.bdcdyh " \
                    "from dj_djben a,dj_fdcq2_djben_zs b,dj_qtxz c " \
                    "where a.id = c.djbid " \
                    "and a.bdcdyh = b.bdcdyh " \
                    "and a.zt='1' " \
                    "and a.sfyx =1 " \
                    "and a.sfsfcd =1 " \
                    "and b.sfyx=1 " \
                    "and b.sfsfcd =1 " \
                    "and c.zt='1' " \
                    "and c.sfyx=1 " \
                    "and rownum <50 " \
                    "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getCdghChangeRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")

    # 分户转移
    def getFhTransferRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        # querySQL =  "select a.bdcdyh " \
        #             "from dj_fdcq2_djben_zs  a,dj_fdcq2 b " \
        #             "where a.qlbid = b.id " \
        #             "and a.sfdh =1 " \
        #             "and a.sfyx = 1 " \
        #             "and b.sfdz = 1 " \
        #             "and b.zt = '1' " \
        #             "and b.sfyx=1  " \
        #             "and rownum <50 " \
        #             "order by dbms_random.value()"

        querySQL = "select distinct a.bdcdyh " \
                   "from dj_fdcq2_djben_zs a ,dj_fdcq2 b " \
                   "where a.qlbid = b.id " \
                   "and b.id in " \
                   "(select cqbid  from dj_fsssxx where zt='1' and sfyx=1  and fssslx='1' group by cqbid having count(cqbid) < 4)" \
                   "and a.sfdh = 1 " \
                   "and a.sfyx = 1 " \
                   "and b.sfdz = 1 " \
                   "and b.zt = '1' " \
                   "and b.sfyx = 1 " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"

        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getFhTransferRegisterData()
            else:
                queryFsssxxSQL = "select count(1) from dj_fsssxx where zt='1' and sfyx=1 and cqbid=(select id from dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "')"
                queryFsssxxSQLRes = self.db_dj_conn.SqlExecute(queryFsssxxSQL)
                if queryFsssxxSQLRes:
                    logger.debug("查询到该主产权关联的dj_fsssxx表数据条数为-->%d" % queryFsssxxSQLRes)
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes,queryFsssxxSQLRes
                else:
                    logger.error("查询dj_fsssxx表数据条数为0,请检查sql语句正确性或数据库是否存在符合条件数据。")
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")

    # 预转现登记查询数据
    # def getYzxRegisterData(self):
    #     querySQL = "select bdcdyh from (select bdcdyh,djbid from DJJGK.DJ_YG where zt='1' and sfyx=1 and bdcdyh>'0'and jzmj>'0')a inner join (select id from DJJGK.DJ_DJBEN where zt='1' and sfyx=1 and sfysczql=1)b on a.djbid = b.id and rownum <30 order by dbms_random.value()"
    #     queryRes = self.db_dj_conn.SqlExecute(querySQL)
    #     print("DJJGK查询数据：%s" % queryRes)
    #     # 检查数据是否有查封
    #     cfzt = xzZtQuery(self.dbInfo).cfZtQuery(queryRes)
    #     print('cfzt', cfzt)
    #     # 检查数据是否有异议
    #     yyzt = xzZtQuery(self.dbInfo).yyZtQuery(queryRes)
    #     print('yyzt', yyzt)
    #     # 检查数据是否有预抵押
    #     ydyzt = xzZtQuery(self.dbInfo).ydyZtQuery(queryRes)
    #     print('ydyzt', ydyzt)
    #     # 检查数据是否在办件
    #     zbzt = xzZtQuery(self.dbInfo).zbZtQuery(queryRes)
    #     zbzt1 =zbzt[0]
    #     zbzt2 = zbzt[1]
    #
    #     if zbzt1 or zbzt2:
    #         print("数据在办，重新选择选取数据！")
    #         return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()  # 递归
    #     if cfzt:
    #         print("数据查封，重新选择选取数据！")
    #         return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()  # 递归
    #     if yyzt:
    #         print("数据异议，重新选择选取数据！")
    #         return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()  # 递归
    #     if ydyzt:
    #         print("数据预抵押，重新选择选取数据！")
    #         return dataInit(self.dbInfo).getSpfOrClfChangeRegisterData()  # 递归
    #     else:
    #         print("数据符合！数据为：%s" % queryRes)
    #         self.db_qj_conn.closeConn()
    #         self.db_dj_conn.closeConn()
    #         return queryRes

    ##-------------------------抵押登记----------------------------##
    # 土地首次抵押查询数据
    def getLandFirstDyData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandFirstDyData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 不动产首次抵押查询数据
    def getHouseFirstDyRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_fdcq2 a where a.zt='1' and a.sfyx=1 and a.bdcdyh not like '%9999%' and a.fwxz='0' and a.tdsyqmj>'0') a inner join (select id from dj_djben b where b.sfdy=0 and b.sfcf=0 and b.sfyy=0 and b.sfyg=0 and b.sfysczql=1 and b.zt='1' and b.sfyx=1) b on a.djbid=b.id and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHouseFirstDyRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 在建房地产抵押首次查询数据
    def getZjfdcFirstDyRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct(c.bdcdyh) from （select fwbh,lszfwbh from kjk.dc_ych_fwzk where zt = '1' and sfyx = '0') a left join (select fwbh from kjk.dc_ych where zt = '1'and bdcdyh > '0') b on a.fwbh = b.fwbh left join （select fwbh,zddm,bdcdyh from kjk.dc_ycz where zt = '1') c on a.lszfwbh = c.fwbh left join (select zddm from kjk.dc_djdcbxx where zt = '1'and sfyx = '1') d on c.zddm = d.zddm where c.bdcdyh > '0' order by dbms_random.value "
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHousePlDyRegisterData()
        if queryRes == '' or queryRes == None:
            logger.warning("该数据BDCDYH为空，重新获取数据！")
            return dataInit(self.dbInfo).getHousePlDyRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 批量抵押（房屋）查询数据
    # def getHousePlDyRegisterData(self):
    #     querySQL = "select bdcdyh from DJ_FDCQ2_DJBEN_ZS where qlrmc = (select qlrmc from (select qlrmc,count(qlrmc) from DJ_FDCQ2_DJBEN_ZS where sfyx=1 and sfcf=0 and sfdy=0  and sfyy=0 and bdcdyh > '0' group by qlrmc  having count(qlrmc) > 2  order by dbms_random.value) where rownum < 2) and bdcdyh not like'%9999%'"
    #     queryRes = self.db_dj_conn.SqlExecute(querySQL)
    #     print("DJJGK查询数据：%s" % queryRes)
    #     # 检查该数据是否存在待办件
    #     querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
    #     querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
    #     querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
    #     querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
    #     if querySqxxSQLRes or querySqxxzbSQLRes:
    #         print("该数据已在办理中，重新获取数据！")
    #         return dataInit(self.dbInfo).getHousePlDyRegisterData()
    #     if queryRes =='' or queryRes == None:
    #         print("该数据BDCDYH为空，重新获取数据！")
    #         return dataInit(self.dbInfo).getHousePlDyRegisterData()
    #     else:
    #         print("数据符合！数据为：%s" % queryRes)
    #         self.db_qj_conn.closeConn()
    #         self.db_dj_conn.closeConn()
    #         return queryRes

    # 土地抵押转移查询数据
    def getLandDyChangeData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from djjgk.dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 1 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id inner join(select djbid from djjgk.dj_dy_djben_zm where sfyx=1 and sfdy=1 )c on a.djbid = c.djbid and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandDyChangeData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 不动产抵押转移查询数据
    def getHouseDyChangeRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select bdcdyh,djbid from dj_dy a where a.bdcdyh like '%F%' and a.zt = '1' and a.sfyx = 1 and a.sfdbdy is null and a.fcdymj>'0' group by bdcdyh,djbid having count(bdcdyh) = 1) a inner join (select id from dj_djben b where b.sfdy=1 and b.sfcf=0  and b.sfyy=0 and b.sfysczql=1 and b.zt=1 and b.sfyx=1) b on a.djbid=b.id and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHouseDyChangeRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 预抵押转现查询数据
    def getYdyzxRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select bdcdyh from (select bdcdyh,djbid from dj_ydy where zt='1' and sfyx=1 and fcdymj>'0')a inner join (select id from dj_djben where sfyg=1 and sfydy=1 and sfycf=0 and sfyx=1 and sfysczql=1)b on a.djbid = b.id where bdcdyh > '0' and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getYdyzxRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    ##-------------------------预告登记----------------------------##
    # 商品房预告首次登记
    def getSpfYgRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from " \
                   "(select bdcdyh,fwbh,lszfwbh " \
                   "from dc_h_fwzk where zt = '1' and sfyx = '0') a " \
                   "left join " \
                   "(select fwbh from dc_h where zt = '1') b " \
                   "on a.fwbh = b.fwbh " \
                   "left join " \
                   "(select fwbh,zddm from dc_z where zt = '1') c " \
                   "on a.lszfwbh = c.fwbh " \
                   "left join " \
                   "(select zddm from dc_djdcbxx where zt = '1' and sfyx = '1') d " \
                   "on c.zddm = d.zddm " \
                   "where 1 = 1 " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.db_qj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # # 存在多条现势的登记本记录校验
            # queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            # queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            # if queryDjbenSQLRes == 1:
                # 存在待办件校验
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getSpfYgRegisterData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            # else:
            #     logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
            #     return dataInit(self.dbInfo).getSpfYgDyRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 商品房预告抵押首次登记
    def getSpfYgDyRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh " \
                    "from dj_yg a,dj_djben b " \
                    "where a.djbid = b.id " \
                    "and a.zt='1' " \
                    "and a.sfyx=1 " \
                    "and a.fwdm >'0' " \
                    "and b.zt='1' " \
                    "and b.sfyx=1 " \
                    "and b.sfysczql is null " \
                    "and b.sfydy=0 " \
                    "and b.sfyg=1 " \
                    "and b.sfycf=0 " \
                    "and b.sfdy=0 " \
                    "and b.sfcf=0 " \
                    "and a.bdcdyh like '%F%'" \
                    "and rownum < 50 " \
                    "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 存在多条现势的登记本记录校验
            queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            if queryDjbenSQLRes == 1:
                # 存在待办件校验
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getSpfYgDyRegisterData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            else:
                logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
                return dataInit(self.dbInfo).getSpfYgDyRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预告注销登记
    def getYgCancelRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh " \
                   "from dj_yg a,dj_djben b " \
                   "where a.djbid = b.id " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.fwdm >'0' " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfyg=1 " \
                   "and b.sfycf=0 " \
                   "and a.bdcdyh like '%F%'" \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # # 存在多条现势的登记本记录校验
            # queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            # queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
            # if queryDjbenSQLRes == 1:
                # 存在待办件校验
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getSpfYgCancelData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            # else:
            #     logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
            #     return dataInit(self.dbInfo).getSpfYgDyRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预告抵押注销登记
    def getYdyCancelRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh " \
                    "from dj_ydy a,dj_djben b,dj_yg c " \
                    "where a.cqbid = c.id  and b.id = c.djbid " \
                    "and a.zt='1' " \
                    "and a.sfyx=1 " \
                    "and b.zt='1' " \
                    "and b.sfyx=1 " \
                    "and b.sfydy=1 " \
                    "and b.sfyg=1 " \
                    "and b.sfycf=0 " \
                    "and c.zt='1' " \
                    "and c.sfyx=1 " \
                    "and c.fwdm > '0'" \
                    "and a.bdcdyh like '%F%'" \
                    "and rownum < 50 " \
                    "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 存在多条现势土地信息校验
            zddm = queryRes[:19]
            queryTdxxSQL = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and zddm='" + zddm + "'"
            queryTdxxSQLRes = self.db_dj_conn.SqlExecute(queryTdxxSQL)
            if queryTdxxSQLRes ==1:
                # # 存在多条现势的登记本记录校验
                # queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                # queryDjbenSQLRes = self.db_dj_conn.SqlExecute(queryDjbenSQL)
                # if queryDjbenSQLRes == 1:
                # 存在待办件校验
                querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
                querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
                querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
                querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
                if querySqxxSQLRes or querySqxxzbSQLRes:
                    logger.warning("该数据已在办理中，重新获取数据！")
                    return dataInit(self.dbInfo).getYdyCancelRegisterData()
                else:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug(">>>>>查询入参数据end<<<<<")
                    self.db_qj_conn.closeConn()
                    self.db_dj_conn.closeConn()
                    return queryRes
            # else:
            #     logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
            #     return dataInit(self.dbInfo).getYdyCancelRegisterData()
            else:
                logger.warning("查询单元存在多条现势土地信息记录或不存在现势记录")
                return dataInit(self.dbInfo).getYdyCancelRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)


    ##-------------------------查封登记----------------------------##
    #查封登记（房屋 ）
    def getHouseCfRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select bdcdyh,djbid from dj_fdcq2 a where a.qllx=4 and a.zt=1 and a.sfyx=1 and a.bdcdyh not like '%9999%') a inner join (select id from dj_djben b where b.sfdy=0 and b.sfcf=0 and b.sfyg=0 and b.sfysczql=1 and b.zt=1 and b.sfyx=1) b on a.djbid=b.id and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHouseCfRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    #续查封登记（房屋 ）/解封登记（房屋）
    def getHouseXcfRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct a.bdcdyh from (select bdcdyh,djbid,id from dj_fdcq2  where zt='1' and sfyx=1) a inner join (select id from dj_djben b where sfdy=0 and sfcf=1 and sfyg=0 and zt='1'and sfyx=1) b on a.djbid=b.id inner join (select cqbid from dj_cf where cfwh>'0' and cflxmc = '查封' and zt='1' and sfyx=1 and zszbid is null) c on a.id = c.cqbid where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHouseXcfRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    #批量续查封登记（房屋 ）/解封登记（房屋）（单独写，查询条件没有bdcdyh）
    # def getHousePlxcfRegisterData(self):
    #     logger.debug(">>>查询入参数据start<<<")
    #     querySQL = "select distinct c.cfwh from (select bdcdyh,djbid,id from dj_fdcq2  where zt='1' and sfyx=1) a inner join (select id from dj_djben b where sfdy=0 and sfcf=1 and sfyg=0 and zt='1'and sfyx=1) b on a.djbid=b.id inner join (select cfwh,cqbid from dj_cf where cfwh>'0' and cflxmc = '查封' and zt='1' and sfyx=1 and zszbid is null) c on a.id = c.cqbid where a.bdcdyh > '0'and rownum <50 order by dbms_random.value()"
    #     queryRes = self.db_dj_conn.SqlExecute(querySQL)
    #     logger.debug("查询办件数据-->%s" % queryRes)
    #     # 检查该数据是否存在待办件
    #     querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
    #     querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
    #     querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
    #     querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
    #     if querySqxxSQLRes or querySqxxzbSQLRes:
    #         logger.error("该数据已在办理中，重新获取数据！")
    #         return dataInit(self.dbInfo).getHouseXcfRegisterData()
    #     else:
    #         logger.debug("待登记办件数据-->%s" % queryRes)
    #         logger.debug(">>>查询入参数据end<<<")
    #         self.db_qj_conn.closeConn()
    #         self.db_dj_conn.closeConn()
    #         return queryRes

    # 续查封登记（土地）/解封登记（土地）
    def getLandXcfRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select distinct a.bdcdyh from (select bdcdyh,cqbid,djbid from dj_cf where zt='1' and sfyx=1 and cfwh>'0' and zszbid is null)a inner join (select id from dj_jsydsyq where zt='1' and sfyx=1)b on a.cqbid=b.id inner join (select id from dj_djben where zt='1' and sfyx=1 and sfcf=1)c on a.djbid=c.id where a.bdcdyh > '0' and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and djlx='800' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandXcfRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 预查封登记（房屋 ）
    def getHouseYcfRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL="select a.bdcdyh from (select bdcdyh, djbid from dj_yg where zt = '1' and sfyx = 1  and bdcdyh not like '%9999%') a " \
                 "inner join (select id from dj_djben where sfyg = 1 and sfycf = 0 and sfysczql = 0 and zt = '1' and sfyx = 1) b " \
                 "on a.djbid = b.id " \
                 "inner join (select bdcdyh from dj_ychxx where zt = '1' and sfyx = 1) c " \
                 "on a.bdcdyh = c.bdcdyh " \
                 "and rownum < 50  " \
                 "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql语句-->%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查净地是否已登记（已登记才可办理）
        if queryRes:
            zddm = queryRes[:19]
            queryJsydsyqSQL="select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and zddm='" + zddm + "'"
            queryJsydsyqRes = self.db_dj_conn.SqlExecute(queryJsydsyqSQL)
        else:
            logger.error("未查询到任何数据。")
            return
        if not queryJsydsyqRes:
            return dataInit(self.dbInfo).getHouseYcfRegisterData()
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getHouseYcfRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    # 司法裁定（净地）
    def getLandSfcdRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL="select distinct a.bdcdyh " \
                 "from dj_cf a " \
                 "left join dj_djben b " \
                 "on a.djbid = b.id " \
                 "left join dj_jsydsyq c " \
                 "on b.id = c.djbid " \
                 "where c.qllx = '3'" \
                 "and a.zt = '1' " \
                 "and a.sfyx = 1 " \
                 "and b.zt = '1' " \
                 "and b.sfyx = 1 " \
                 "and b.sfcf = 1 " \
                 "and c.zt='1' " \
                 "and c.sfyx =1 " \
                 "and a.bdcdyh > '0' " \
                 "and rownum < 30 " \
                 "order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and djlx='800' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandSfcdRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    #--------------------------其他登记-----------------------------#
    #查封登记（土地）
    def getLandCfRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id and rownum < 50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查该数据是否存在待办件
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
        querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return dataInit(self.dbInfo).getLandCfRegisterData()
        else:
            logger.debug("待登记办件数据-->%s" % queryRes)
            logger.debug(">>>>>查询入参数据end<<<<<")
            self.db_qj_conn.closeConn()
            self.db_dj_conn.closeConn()
            return queryRes

    #冻结登记（房屋 ）
    def getHouseDjRegisterData(self):
        logger.debug(">>>>>查询入参数据start<<<<<")
        querySQL = "select a.bdcdyh " \
                   "from " \
                   "(select bdcdyh,djbid from dj_fdcq2 " \
                   "where zt='1' " \
                   "and sfyx=1 " \
                   "and bdcdyh not like '%9999%') a " \
                   "inner join " \
                   "(select id from dj_djben " \
                   "where sfdj=0 " \
                   "and sfcf=0 " \
                   "and sfysczql=1 " \
                   "and zt='1' " \
                   "and sfyx=1) b " \
                   "on a.djbid=b.id and rownum <50 order by dbms_random.value()"
        queryRes = self.db_dj_conn.SqlExecute(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.db_dj_conn.SqlExecute(querySqxxSQL)
            querySqxxzbSQLRes = self.db_dj_conn.SqlExecute(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit(self.dbInfo).getHouseDjRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug(">>>>>查询入参数据end<<<<<")
                self.db_qj_conn.closeConn()
                self.db_dj_conn.closeConn()
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)


if __name__ == '__main__':
    dbInfo={
        'qj': 'CGKGB/Cgk2021#@172.16.17.251:1521/orcl',
        'dj': 'DJPT/Djpt2021#@172.16.17.241:1521/orcl'
    }
    obj = dataInit(dbInfo)
    obj.getSpfYgDyRegisterData()
