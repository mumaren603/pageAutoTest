"""
数据初始化，即我们测试用例在运行过程中需要使用到数据预先准备好
"""
from Common.LogFunc import loggerConf
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.CommVerficate import verificator
import sys

logger = loggerConf().getLogger()

class dataInit():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    '''国有建设用地使用权'''
    # 净地未登记
    def getLandCqNotRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select bdcdyh from dc_djdcbxx where zt='1' and sfyx='0' and tdzl>'0' and qllx='3' and bdcdyh >'0' and qlxz>'0'  and zdmj > '0' and pzmj >'0' and pzytdlbm > '0' and qlrmc > '0' and rownum < 30 order by dbms_random.value()"
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否在登记平台做过登记,若已登记，发起流程会校验住，确保数据在权藉存在，在登记平台未做过登记
            verifyRes = verificator().landIsRegisterVerify(queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getLandCqNotRegisterData()
        else:
            logger.error("未查询到权籍有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 净地已登记
    def getLandCqRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
                   "and b.sfyg=0 " \
                   "and b.sfnbxz=0 " \
                   "and b.sfqtxz=0 " \
                   "and b.sfysczql=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
             # 多条产权检查
             verifyRes1 = verificator().tooManyCqResultVerify(0,queryRes)
             # 在办件检查
             verifyRes2 = verificator().processVerify(queryRes)
             if verifyRes1 and verifyRes2:
                 logger.debug("待登记办件数据-->%s" % queryRes)
                 logger.debug("<--------查询入参数据end-------->")
                 return queryRes
             return dataInit().getLandCqRegisterData()
        else:
            logger.error("未查询到登记有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 净地裁定过户
    def getLandCdghRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_jsydsyq a,dj_djben b,dj_qtxz c " \
                   "where a.djbid = b.id  " \
                   "and b.id = c.djbid " \
                   "and a.id = c.cqbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfysczql=1 " \
                   "and b.sfcf=0 " \
                   "and b.sfsfcd=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and c.srrmc > '0' " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getLandCdghRegisterData()
        else:
            logger.error("未查询到登记有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    '''国有建设用地使用权及房屋所有权'''
    # 房地未登记
    def getHouseCqNotRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 是否已登记检查
            verifyRes1 = verificator().houseIsRegisterVerify(queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getSpfFirstRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 建筑物区分业主共有部分
    def getJzwqfyzgybfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权检查
            verifyRes1 = verificator().tooManyCqResultVerify(0, queryRes)
            # 检查该宗地是否做过登记，未登记不予办理
            zddm = queryRes[:19]
            verifyRes2 = verificator().landIsRegisterVerify(zddm)
            if verifyRes1 and not verifyRes2:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getJzwqfyzgybfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 项目类多幢
    def getXmldzFirstRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select bdcdyh from dc_h_fwzk where zt='1' and sfyx='0' and  lszfwbh in(" \
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
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 是否已登记检查
            verifyRes1 = verificator().houseIsRegisterVerify(queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getXmldzFirstRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 项目类多幢2(根据进入流程数据zddm查询另一条数据，在业务办理过程中不动产基本信息页面添加)
    def getXmldzFirstRegisterData2(self, bdcdyh):
        logger.debug("<--------查询入参数据start-------->")
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
                   "and c.zddm ='" + zddm + "'"
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询入参ZDDM为：%s" % zddm)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            if queryRes != bdcdyh:
                # 是否已登记检查
                verifyRes1 = verificator().houseIsRegisterVerify(queryRes)
                # 在办件检查
                verifyRes2 = verificator().processVerify(queryRes)
                if verifyRes1 and verifyRes2:
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug("<--------查询入参数据end-------->")
                    return queryRes
                return dataInit().getXmldzFirstRegisterData()
            else:
                logger.warning("查询到数据与主产权数据重复，重新获取数据。")
                return dataInit().getXmldzFirstRegisterData2(bdcdyh)
        else:
            logger.error("根据ZDDM未查询到其他户数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 商品房/存量房首次转移登记
    def getHouseCqRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes1 = verificator().tooManyCqResultVerify(1,queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            # 附属设施检查
            verifyRes3 = verificator().fsssIsExistsVerify(queryRes)

            if verifyRes1 and verifyRes2 and verifyRes3:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseCqRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预转现
    def getYzxRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL="select distinct a.bdcdyh " \
                 "from dj_yg a ,dj_djben b,dj_fdcq2 c " \
                 "where a.djbid = b.id " \
                 "and b.id = c.djbid " \
                 "and a.zt='1' and a.sfyx=1 and b.zt='1' and b.sfyx=1 " \
                 "and b.sfysczql=1 and b.sfyg=1 and b.sfcf=0 and b.sfycf=0 " \
                 "and b.sfdy=0 and b.sfydy=0 and sfdj=0" \
                 "and c.zt='1' and c.sfyx=1 " \
                 "and rownum < 50" \
                 "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            # 多条产权宽表检查
            verifyRes2 = verificator().tooManyCqFdcq2DjbenZsResultVerify(queryRes)
            if verifyRes and verifyRes2:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getYzxRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 裁定过户（房屋）
    def getCdghChangeRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes1 = verificator().tooManyCqResultVerify(1,queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            # 附属设施检查
            verifyRes3 = verificator().fsssIsExistsVerify(queryRes)
            if verifyRes1 and verifyRes2 :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getSpfOrClfChangeRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 分户转移
    def getFhTransferRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_fdcq2_djben_zs a ,dj_fdcq2 b " \
                   "where a.qlbid = b.id " \
                   "and b.id in " \
                   "(select cqbid  from dj_hxx where zt='1' and sfyx=1  and sfdz=1 and sfdh=1 group by cqbid having count(cqbid) < 4)" \
                   "and a.sfdh = 1 " \
                   "and a.sfyx = 1 " \
                   "and b.sfdz = 1 " \
                   "and b.sfdh = 1 " \
                   "and b.zt = '1' " \
                   "and b.sfyx = 1 " \
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
            querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit().getFhTransferRegisterData()
            else:
                queryHxxSQL = "select count(1) from dj_hxx where zt='1' and sfyx=1 and cqbid=(select id from dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "')"
                queryHxxSQLRes = self.djObj.fetchone(queryHxxSQL)
                if queryHxxSQLRes:
                    logger.debug("查询到该主产权关联的dj_hxx表数据条数为-->%d" % queryHxxSQLRes)
                    logger.debug("待登记办件数据-->%s" % queryRes)
                    logger.debug("<--------查询入参数据end-------->")
                    return queryRes, queryHxxSQLRes
                else:
                    logger.error("查询dj_fsssxx表数据条数为0,请检查sql语句正确性或数据库是否存在符合条件数据。")
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # '''抵押登记'''
    # # 土地首次抵押查询数据
    # def getLandDyNotRegisterData(self):
    #     logger.debug("<--------查询入参数据start-------->")
    #     querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from dj_djben where sfdy = 0 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id and rownum < 50 order by dbms_random.value()"
    #     queryRes = self.djObj.fetchone(querySQL)
    #     logger.debug("查询sql为：%s" % querySQL)
    #     logger.debug("查询办件数据-->%s" % queryRes)
    #     if queryRes:
    #         # 在办件检查
    #         verifyRes = verificator().processVerify(queryRes)
    #         if verifyRes :
    #             logger.debug("待登记办件数据-->%s" % queryRes)
    #             logger.debug("<--------查询入参数据end-------->")
    #             return queryRes
    #         return dataInit().getLandFirstDyData()
    #     else:
    #         logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
    #         sys.exit(-1)
    #
    # # 不动产首次抵押查询数据
    # def getHouseDyNotRegisterData(self):
    #     logger.debug("<--------查询入参数据start-------->")
    #     querySQL = "select a.bdcdyh from (select djbid,bdcdyh from dj_fdcq2 a where a.zt='1' and a.sfyx=1 and a.bdcdyh not like '%9999%' and a.fwxz='0' and a.tdsyqmj>'0') a inner join (select id from dj_djben b where b.sfdy=0 and b.sfcf=0 and b.sfyy=0 and b.sfyg=0 and b.sfysczql=1 and b.zt='1' and b.sfyx=1) b on a.djbid=b.id and rownum <50 order by dbms_random.value()"
    #     queryRes = self.djObj.fetchone(querySQL)
    #     logger.debug("查询sql为：%s" % querySQL)
    #     logger.debug("查询办件数据-->%s" % queryRes)
    #     if queryRes:
    #         # 在办件检查
    #         verifyRes = verificator().processVerify(queryRes)
    #         if verifyRes :
    #             logger.debug("待登记办件数据-->%s" % queryRes)
    #             logger.debug("<--------查询入参数据end-------->")
    #             return queryRes
    #         return dataInit().getHouseDyNotRegisterData()
    #     else:
    #         logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
    #         sys.exit(-1)

    # 在建房地产抵押首次查询数据
    def getZjfdcFirstDyRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct(c.bdcdyh) from （select fwbh,lszfwbh from kjk.dc_ych_fwzk where zt = '1' and sfyx = '0') a left join (select fwbh from kjk.dc_ych where zt = '1'and bdcdyh > '0') b on a.fwbh = b.fwbh left join （select fwbh,zddm,bdcdyh from kjk.dc_ycz where zt = '1') c on a.lszfwbh = c.fwbh left join (select zddm from kjk.dc_djdcbxx where zt = '1'and sfyx = '1') d on c.zddm = d.zddm where c.bdcdyh > '0' order by dbms_random.value "
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from ywbdk.yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from YWBDK.yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from ywbdk.yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
            querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit().getHousePlDyRegisterData()
            if queryRes == '' or queryRes == None:
                logger.warning("该数据BDCDYH为空，重新获取数据！")
                return dataInit().getHousePlDyRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
            return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 土地抵押转移查询数据
    def getLandDyChangeRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh from (select djbid,bdcdyh from djjgk.dj_jsydsyq where qllx = '3' and zt = '1' and sfyx = 1 and bdcdyh not like '%9999%') a inner join (select id,bdcdyh from djjgk.dj_djben where sfdy = 1 and sfcf = 0 and sfzzdj = 0 and sfysczql = 1 and zt = '1' and sfyx = 1) b on a.djbid = b.id inner join(select djbid from djjgk.dj_dy_djben_zm where sfyx=1 and sfdy=1 )c on a.djbid = c.djbid and rownum < 50 order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getLandDyChangeRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

            return queryRes

    # 做过抵押（房屋）
    def getHouseDyRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_dy a,dj_djben b,dj_dy_djben_zm c " \
                   "where a.djbid = b.id " \
                   "and a.id =c.qlbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.dybdclx='2' " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfdy=1 " \
                   "and b.sfcf=0 " \
                   "and c.sfyx=1 " \
                   "and c.bdclx='0、1' " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseDyRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预抵押转现查询数据
    def getYdyzxRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select bdcdyh " \
                   "from " \
                   "(select bdcdyh,djbid from dj_ydy where zt='1' and sfyx=1 and fcdymj>'0')a " \
                   "inner join " \
                   "(select id from dj_djben " \
                   "where sfyg=1 and sfydy=1 and sfycf=0 and sfyx=1 and sfysczql=1)b " \
                   "on a.djbid = b.id where bdcdyh > '0' " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getYdyzxRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    '''预告登记'''
    # 商品房预告首次登记
    def getSpfYgRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
                   "and a.bdcdyh > '0' " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.qjObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getSpfYgRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 商品房预告抵押首次登记
    def getSpfYgDyRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条现势的登记本校验
            verifyRes1 = verificator().tooManyDjbenResultVerify(queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2 :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getSpfYgRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预告注销登记
    def getYgCancelRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getYgCancelRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预告抵押注销登记
    def getYdyCancelRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条现势土地信息校验
            verifyRes1 = verificator().tooManyDjbenResultVerify(queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2 :
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getSpfYgRegisterData()

        #
        #     # 存在多条现势土地信息校验
        #     zddm = queryRes[:19]
        #     queryTdxxSQL = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and zddm='" + zddm + "'"
        #     queryTdxxSQLRes = self.djObj.fetchone(queryTdxxSQL)
        #     if queryTdxxSQLRes == 1:
        #         # # 存在多条现势的登记本记录校验
        #         # queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        #         # queryDjbenSQLRes = self.djObj.fetchone(queryDjbenSQL)
        #         # if queryDjbenSQLRes == 1:
        #         # 存在待办件校验
        #         querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
        #         querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
        #         querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
        #         querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
        #         if querySqxxSQLRes or querySqxxzbSQLRes:
        #             logger.warning("该数据已在办理中，重新获取数据！")
        #             return dataInit().getYdyCancelRegisterData()
        #         else:
        #             logger.debug("待登记办件数据-->%s" % queryRes)
        #             logger.debug("<--------查询入参数据end-------->")
        #
        #             return queryRes
        #     # else:
        #     #     logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
        #     #     return dataInit().getYdyCancelRegisterData()
        #     else:
        #         logger.warning("查询单元存在多条现势土地信息记录或不存在现势记录")
        #         return dataInit().getYdyCancelRegisterData()
        # else:
        #     logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
        #     sys.exit(-1)

    '''查封登记'''
    # 查封登记（净地）
    def getLandCfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
                   "from dj_jsydsyq a,dj_djben b,dj_tdxx c " \
                   "where a.djbid = b.id " \
                   "and a.id = c.cqbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.bdcdyh > '0' " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes= verificator().tooManyCqResultVerify(0, queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getLandCfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 查封登记（房屋）
    def getHouseCfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
                   "from dj_fdcq2 a,dj_djben b,dj_fdcq2_djben_zs c " \
                   "where a.djbid = b.id " \
                   "and a.id = c.qlbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.bdcdyh > '0' " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and c.sfyx=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes = verificator().tooManyCqResultVerify(1, queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseCqRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 续查封登记（房屋）
    def getHouseXcfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
                   "from dj_cf a,dj_fdcq2 b,dj_djben c,dj_fdcq2_djben_zs d " \
                   "where a.cqbid = b.id " \
                   "and b.djbid = c.id " \
                   "and b.id =d.qlbid " \
                   "and a.zt='1' and a.sfyx=1 and a.bdcdyh > '0'" \
                   "and b.zt='1'and b.sfyx=1  " \
                   "and c.zt='1' and c.sfyx=1 and c.sfcf=1 " \
                   "and d.sfyx=1 and d.sfcf=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes = verificator().tooManyCqResultVerify(1, queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseXcfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 续查封登记（净地）
    def getLandXcfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
                   "from dj_cf a,dj_jsydsyq b,dj_djben c " \
                   "where a.cqbid = b.id " \
                   "and b.djbid = c.id " \
                   "and a.zt='1' and a.sfyx=1 and a.bdcdyh > '0'" \
                   "and b.zt='1'and b.sfyx=1  " \
                   "and c.zt='1' and c.sfyx=1 and c.sfcf=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes = verificator().tooManyCqResultVerify(0, queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseXcfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 预查封登记（房屋 ）
    def getHouseYcfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_yg a,dj_djben b,dj_ychxx c " \
                   "where a.djbid = b.id " \
                   "and a.hid = c.id " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfyg=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql语句-->%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        # 检查净地是否已登记（已登记才可办理）
        if queryRes:
            return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 批量续预查封登记（房屋 ）
    def getHousePlxycfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select a.bdcdyh " \
                   "from dj_ycf a,dj_djben b " \
                   "where a.djbid = b.id " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and a.cfwh is not null " \
                   "and a.cfwj is not null " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql语句-->%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHousePlxycfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 司法裁定（房屋）
    def getHouseSfcdRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL =  "select distinct a.bdcdyh " \
                    "from dj_cf a,dj_fdcq2 b,dj_djben c,dj_fdcq2_djben_zs d " \
                    "where a.cqbid = b.id " \
                    "and b.djbid = c.id " \
                    "and b.id = d.qlbid " \
                    "and a.zt='1' and a.sfyx=1 and a.bdcdyh > '0' " \
                    "and b.zt='1' and b.sfyx=1 " \
                    "and c.zt='1' and c.sfyx=1 and c.sfcf=1 and c.sfsfcd = 0 " \
                    "and d.sfyx=1 and d.sfcf=1 and d.sfsfcd = 0 " \
                    "and rownum <50 " \
                    "order by dbms_random.value("
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes1 = verificator().tooManyCqResultVerify(1,queryRes)
            # 在办件检查
            verifyRes2 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseSfcdRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 小证查封登记
    def getXzcfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_zszb a " \
                   "where zt='1' " \
                   "and sfyx=1 " \
                   "and sfcf=0 " \
                   "and sfgj=0 " \
                   "and not exists  " \
                   "(select 1 from dj_jsydsyq b where zt='1' and sfyx=1 and a.ywh = b.ywh)" \
                   " and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getXzcfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 小证续查封登记
    def getXzxcfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_cf a,dj_zszb b " \
                   "where a.zszbid = b.id " \
                   "and a.bdcdyh= b.bdcdyh  " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and a.zszbid is not null " \
                   "and a.cfjg is not null "\
                   "and a.cfwh is not null " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfcf = 1 " \
                   "and rownum < 50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 在办件检查
            verifyRes = verificator().processVerify(queryRes)
            if verifyRes:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getXzxcfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 司法裁定（净地）
    def getLandSfcdRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and djlx='800' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
            querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit().getLandSfcdRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 解封登记（土地）
    def getLandJfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_cf a,dj_djben b,dj_jsydsyq c " \
                   "where a.djbid = b.id " \
                   "and b.id = c.djbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfcf=1 " \
                   "and c.zt='1' " \
                   "and c.sfyx=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and djlx='800' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
            querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit().getLandXcfRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    # 解封登记（房屋）
    def getHouseJfRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
        querySQL = "select distinct a.bdcdyh " \
                   "from dj_cf a,dj_djben b,dj_fdcq2_djben_zs c " \
                   "where a.djbid = b.id " \
                   "and a.cqbid = c.qlbid " \
                   "and a.zt='1' " \
                   "and a.sfyx=1 " \
                   "and b.zt='1' " \
                   "and b.sfyx=1 " \
                   "and b.sfcf=1 " \
                   "and c.sfcf=1 " \
                   "and c.sfyx=1 " \
                   "and rownum <50 " \
                   "order by dbms_random.value()"
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 多条产权校验
            verifyRes1 = verificator().tooManyCqResultVerify(1,queryRes)
            # 多条登记本校验
            verifyRes2 = verificator().tooManyDjbenResultVerify(queryRes)
            # 在办件检查
            verifyRes3 = verificator().processVerify(queryRes)
            if verifyRes1 and verifyRes2 and verifyRes3:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")
                return queryRes
            return dataInit().getHouseJfRegisterData()
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)

    '''其他登记'''
    # 冻结登记（房屋 ）
    def getHouseDjRegisterData(self):
        logger.debug("<--------查询入参数据start-------->")
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
        queryRes = self.djObj.fetchone(querySQL)
        logger.debug("查询sql为：%s" % querySQL)
        logger.debug("查询办件数据-->%s" % queryRes)
        if queryRes:
            # 检查该数据是否存在待办件
            querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
            querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
            querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
            querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
            if querySqxxSQLRes or querySqxxzbSQLRes:
                logger.warning("该数据已在办理中，重新获取数据！")
                return dataInit().getHouseDjRegisterData()
            else:
                logger.debug("待登记办件数据-->%s" % queryRes)
                logger.debug("<--------查询入参数据end-------->")

                return queryRes
        else:
            logger.error("未查询到有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
            sys.exit(-1)


# aa = DJ_DB()
# def getLandChangeRegisterData():
#     querySQL = "select distinct a.bdcdyh " \
#                "from dj_jsydsyq a,dj_djben b,dj_tdxx c " \
#                "where a.djbid = b.id  " \
#                "and a.id = c.cqbid " \
#                "and a.zt='1' " \
#                "and a.sfyx=1 " \
#                "and b.zt='1' " \
#                "and b.sfyx=1 " \
#                "and b.sfsfcd=0 " \
#                "and b.sfcf=0 " \
#                "and b.sfdy=0 " \
#                "and b.sfnbxz=0 " \
#                "and b.sfqtxz=0 " \
#                "and b.sfysczql=1 " \
#                "and c.zt='1' " \
#                "and c.sfyx=1 " \
#                "and a.bdcdyh > '0' " \
#                "and rownum < 50 " \
#                "order by dbms_random.value()"
#     queryRes = aa.fetchone(querySQL)
#     logger.debug("查询sql为：%s" % querySQL)
#     logger.debug("查询办件数据-->%s" % queryRes)
#     print("查询办件数据-->%s" % queryRes,type(queryRes))
#     if queryRes:
#         # 检查该数据是否存在多条产权（内蒙古允许）
#         queryJsydsyqSQL = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
#         queryjsydsyqSQLRes = aa.fetchone(queryJsydsyqSQL)
#         print('queryjsydsyqSQLRes',queryjsydsyqSQLRes)
#         if queryjsydsyqSQLRes > 1:
#             logger.error("该单元存在多条现势数据，请检查！")
#             return getLandChangeRegisterData()
#         # 检查该数据是否存在待办件
#         querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryRes + "'"
#         querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryRes + "')"
#         querySqxxSQLRes = aa.fetchone(querySqxxSQL)
#         querySqxxzbSQLRes = aa.fetchone(querySqxxzbSQL)
#         if querySqxxSQLRes or querySqxxzbSQLRes:
#             logger.warning("该数据已在办理中，重新获取数据！")
#             return getLandChangeRegisterData()
#         else:
#             logger.debug("待登记办件数据-->%s" % queryRes)
#             logger.debug("<--------查询入参数据end-------->")
#             return queryRes
#     else:
#         logger.error("未查询到登记有效数据，请检查sql语句正确性或数据库是否存在符合条件数据。")
#         sys.exit(-1)
#
#
# getLandChangeRegisterData()

# print(dataInit().getCdghChangeRegisterData())
