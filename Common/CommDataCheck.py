'''公共数据登簿后检查'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.LogFunc import loggerConf
import sys

logger = loggerConf().getLogger()

class verificator():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    # 获取业务号
    def getYwh(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        try:
            # 批量业务
            if sfpl == 1:
                sql_yw_sqxxzb_ywh = "select ywh from yw_sqxxzb where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxxzb_ywh = self.djObj.fetchone(sql_yw_sqxxzb_ywh)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxxzb_ywh)
                return res_yw_sqxxzb_ywh
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx where ajzt='2' and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                print('sql:',sql_yw_sqxx_ywh)
                # sql_yw_sqxx_ywh = "select ywh from yw_sqxx t where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
                logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)
                return res_yw_sqxx_ywh
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取产权关联数据（主要是id,djbid,zsbid）
    def getCqRealtionData(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        ywh = self.getYwh(bdcdyh,data)

        try:
            # 净地
            if cqType == 0:
                sql_dj_jsydsyq_data = "select id,djbid,zsbid from dj_jsydsyq where zt='1' and sfyx=1 and ywh='" + ywh + "'"
                res_dj_jsydsyq_data = self.djObj.fetchone2(sql_dj_jsydsyq_data)
                logger.debug("dj_jsydsyq表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_jsydsyq_data)
                return  res_dj_jsydsyq_data
            elif cqType == '1':
                sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where zt='1' and sfyx=1 and ywh='" + ywh + "'"
                res_dj_fdcq2_data = self.djObj.fetchone2(sql_dj_fdcq2_data)
                logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
                return res_dj_fdcq2_data
            else:
                logger.error("缺少cqType参数，请检查yml文件")
                sys.exit(-1)
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 净地产权登簿检查
    def getLandRegisterRes(self,bdcdyh,data):
        resList = []
        try:
            res_cqbid, res_djbid, res_zsbid = self.getCqRealtionData(bdcdyh, data)
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

            sql_dj_djben = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and id='" + res_djbid + "'"
            res_dj_djben = self.djObj.fetchone(sql_dj_djben)
            resList.append(res_dj_djben)
            logger.debug("dj_djben表查询sql：%s" % sql_dj_djben)
            logger.debug("dj_djben表查询记录数：%d" % res_dj_djben)

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



if __name__ == '__main__':
    bdcdyh = '321322100021GB00022W00000000'
    data={
        "initdata":{
            "lcInfo":{
                "qllx":"国有建设用地使用权",
                "djlx":"首次登记",
                "ywlxID":"C49536D5C50F4F609FACAAAE805EC510"
            },
            "params":{
                "ywxl":"",
                "cqType":""
            }
        }
    }

    obj = verificator()
    res = obj.getLandRegisterRes(bdcdyh, data)
    print(res,type(res))

