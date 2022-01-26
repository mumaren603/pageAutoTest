'''
登簿后每个业务关联关系查询
'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.LogFunc import loggerConf
import sys

logger = loggerConf().getLogger()
djObj = DJ_DB()
qjObj = QJ_DB()

# class relation():
#     def __init__(self):
#         self.djObj = DJ_DB()
#         self.qjObj = QJ_DB()
#
#     # 获取业务号
#     def getYwh(self,bdcdyh,data):
#         ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
#         sfpl = data.get('initdata').get('params', None).get('sfpl', None)
#         sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
#
#         try:
#             # 批量业务
#             if sfpl == 1:
#                 # 整体发证
#                 ywlxList = [
#                     '608286609F5C429CB32BA42C56F7C7F7',  #项目类多幢首次
#                     '7772C3A4830C41C186336BD2E789E027',  # 项目类多幢转移
#                     '8B6FD2DF1F1C4750A80F64B591943A54',  # 项目类多幢变更
#                 ]
#                 # 项目类多幢 整体发证需要通过bz2查询
#                 if sfztfz == 1 and ywlxID in ywlxList:
#                     sql_yw_sqxxzb_bz2 = "select bz2 from yw_sqxxzb where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
#                     res_yw_sqxxzb_bz2 = self.djObj.fetchone(sql_yw_sqxxzb_bz2)
#                     if not res_yw_sqxxzb_bz2:
#                         logger.error("yw_sqxxzb表查询主业务号为空")
#                         sys.exit(-1)
#                     logger.debug("yw_sqxxzb表查询主业务号为：%s" % res_yw_sqxxzb_bz2)
#                     return res_yw_sqxxzb_bz2
#                 # 按幢发证 或 其他批量业务
#                 sql_yw_sqxxzb_ywh = "select ywh from yw_sqxxzb where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
#                 res_yw_sqxxzb_ywh = self.djObj.fetchone(sql_yw_sqxxzb_ywh)
#                 if not res_yw_sqxxzb_ywh:
#                     logger.error("yw_sqxxzb表查询子ywh为空")
#                     sys.exit(-1)
#                 logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxxzb_ywh)
#                 return res_yw_sqxxzb_ywh
#             else:
#                 sql_yw_sqxx_ywh = "select ywh from yw_sqxx where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
#                 res_yw_sqxx_ywh = self.djObj.fetchone(sql_yw_sqxx_ywh)
#                 if not res_yw_sqxx_ywh:
#                     logger.error("yw_sqxx表查询ywh为空")
#                     sys.exit(-1)
#                 logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)
#                 return res_yw_sqxx_ywh
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     '''>>>>>>>>>>>>产权类<<<<<<<<<<<<'''
#     # 获取产权关联数据（id,djbid,zsbid）
#     def getCqRealtionData(self,bdcdyh,data):
#         ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
#         sfpl = data.get('initdata').get('params', None).get('sfpl', None)
#         cqType = data.get('initdata').get('params', None).get('cqType', None)
#         sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
#
#         ywh = self.getYwh(bdcdyh,data)
#
#         try:
#             # 净地
#             if cqType == 0:
#                 sql_dj_jsydsyq_data = "select id,djbid,zsbid from dj_jsydsyq where ywh='" + ywh + "'"
#                 res_dj_jsydsyq_data = self.djObj.fetchone2(sql_dj_jsydsyq_data)
#                 logger.debug("dj_jsydsyq表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_jsydsyq_data)
#                 return  res_dj_jsydsyq_data
#             elif cqType == 1:
#                 # 整体发证 如项目类多幢
#                 if sfztfz == 1:
#                     sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where bz2='" + ywh + "'"
#                     res_dj_fdcq2_data = self.djObj.fetchone2(sql_dj_fdcq2_data)
#                     logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
#                     return res_dj_fdcq2_data
#
#                 sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where ywh='" + ywh + "'"
#                 res_dj_fdcq2_data = self.djObj.fetchone2(sql_dj_fdcq2_data)
#                 logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
#                 return res_dj_fdcq2_data
#             else:
#                 logger.error("产权类型【cqType】未传值，请检查yml文件")
#                 sys.exit(-1)
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取产权注销关联数据（id,djbid,zsbid）
#     def getCqCancelRealtionData(self,bdcdyh,data):
#         ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
#         sfpl = data.get('initdata').get('params', None).get('sfpl', None)
#         cqType = data.get('initdata').get('params', None).get('cqType', None)
#
#         ywh = self.getYwh(bdcdyh,data)
#
#         try:
#             # 净地
#             if cqType == 0:
#                 sql_dj_jsydsyq_data = "select id,djbid,zsbid from dj_jsydsyq where zxywh='" + ywh + "'"
#                 res_dj_jsydsyq_data = self.djObj.fetchone2(sql_dj_jsydsyq_data)
#                 logger.debug("dj_jsydsyq表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_jsydsyq_data)
#                 return  res_dj_jsydsyq_data
#             elif cqType == 1:
#                 sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where zxywh='" + ywh + "'"
#                 res_dj_fdcq2_data = self.djObj.fetchone2(sql_dj_fdcq2_data)
#                 logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
#                 return res_dj_fdcq2_data
#             else:
#                 logger.error("产权类型【cqType】未传值，请检查yml文件")
#                 sys.exit(-1)
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     '''>>>>>>>>>>>>抵押类<<<<<<<<<<<<'''
#     # 获取抵押关联数据（id,djbid,zsbid）
#     def getDyRealtionData(self, bdcdyh, data):
#         ywh = self.getYwh(bdcdyh, data)
#
#         try:
#             sql_dj_dy_data = "select id,djbid,zsbid,cqbid from dj_dy where ywh='" + ywh + "'"
#             res_dj_dy_data = self.djObj.fetchone2(sql_dj_dy_data)
#             logger.debug("dj_dy表id,djbid,zsbid,cqbid分别为：%s，%s，%s，%s" % res_dj_dy_data)
#             return res_dj_dy_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取抵押注销关联数据（id,djbid,zsbid）
#     def getDyCancelRealtionData(self, bdcdyh, data):
#         ywh = self.getYwh(bdcdyh, data)
#
#         try:
#             sql_dj_dy_data = "select id,djbid,zsbid,cqbid from dj_dy where zxdyywh='" + ywh + "'"
#             res_dj_dy_data = self.djObj.fetchone2(sql_dj_dy_data)
#             logger.debug("dj_dy表id,djbid,zsbid,cqbid分别为：%s，%s，%s，%s" % res_dj_dy_data)
#             return res_dj_dy_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     '''>>>>>>>>>>>>预告类<<<<<<<<<<<<'''
#     # 获取预告关联数据（id,djbid,zsbid，hid）
#     def getYgRealtionData(self, bdcdyh, data):
#         ywh = self.getYwh(bdcdyh, data)
#
#         try:
#             sql_dj_yg_data = "select id,djbid,zsbid,hid from dj_yg where ywh='" + ywh + "'"
#             res_dj_yg_data = self.djObj.fetchone2(sql_dj_yg_data)
#             logger.debug("dj_yg表id,djbid,zsbid,hid：%s，%s，%s，%s" % res_dj_yg_data)
#             return res_dj_yg_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取预告抵押关联数据（id,djbid,zsbid，hid）
#     def getYdyRealtionData(self, bdcdyh, data):
#         ywh = self.getYwh(bdcdyh, data)
#
#         try:
#             sql_dj_ydy_data = "select id,djbid,zsbid,hid from dj_yg where ywh='" + ywh + "'"
#             res_dj_ydy_data = self.djObj.fetchone2(sql_dj_ydy_data)
#             logger.debug("dj_ydy表id,djbid,zsbid,hid：%s，%s，%s，%s" % res_dj_ydy_data)
#             return res_dj_ydy_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     '''>>>>>>>>>>>>查封类<<<<<<<<<<<<'''
#     # 获取查封关联数据（id,djbid,zsbid）
#     def getCfRealtionData(self,bdcdyh,data):
#         ywh = self.getYwh(bdcdyh,data)
#         try:
#             sql_dj_cf_data = "select id,djbid,cqbid from dj_cf where ywh='" + ywh + "'"
#             res_dj_cf_data = self.djObj.fetchone2(sql_dj_cf_data)
#             logger.debug("dj_cf表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_cf_data)
#             return res_dj_cf_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取预查封关联数据（id,djbid,zsbid）
#     def getYcfRealtionData(self,bdcdyh,data):
#         ywh = self.getYwh(bdcdyh,data)
#         try:
#             sql_dj_ycf_data = "select id,djbid,cqbid,hid from dj_ycf where ywh='" + ywh + "'"
#             res_dj_ycf_data = self.djObj.fetchone2(sql_dj_ycf_data)
#             logger.debug("dj_ycf表id,djbid,cqbid,hid分别为：%s，%s，%s，%s" % res_dj_ycf_data)
#             return res_dj_ycf_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取司法裁定关联数据（id,djbid,zsbid）
#     def getSfcdRealtionData(self,bdcdyh,data):
#         ywh = self.getYwh(bdcdyh,data)
#         try:
#             sql_dj_qtxz_data = "select id,djbid,cqbid from dj_qtxz where ywh='" + ywh + "'"
#             res_dj_qtxz_data = self.djObj.fetchone2(sql_dj_qtxz_data)
#             logger.debug("dj_qtxz表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_qtxz_data)
#             return res_dj_qtxz_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)
#
#     # 获取解封关联数据（id,djbid,zsbid）
#     def getJfRealtionData(self,bdcdyh,data):
#         ywh = self.getYwh(bdcdyh,data)
#         try:
#             sql_dj_cf_data = "select id,djbid,cqbid from dj_cf where jfywh='" + ywh + "'"
#             res_dj_cf_data = self.djObj.fetchone2(sql_dj_cf_data)
#             logger.debug("dj_cf表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_cf_data)
#             return res_dj_cf_data
#         except Exception as e:
#             logger.error("数据查询异常,具体详见：%s" % e)
#             sys.exit(-1)

class relation():
    # 获取业务号
    def getYwh(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)

        try:
            # 批量业务
            if sfpl == 1:
                # 整体发证
                ywlxList = [
                    '608286609F5C429CB32BA42C56F7C7F7',  #项目类多幢首次
                    '7772C3A4830C41C186336BD2E789E027',  # 项目类多幢转移
                    '8B6FD2DF1F1C4750A80F64B591943A54',  # 项目类多幢变更
                ]
                # 项目类多幢 整体发证需要通过bz2查询
                if sfztfz == 1 and ywlxID in ywlxList:
                    sql_yw_sqxxzb_bz2 = "select bz2 from yw_sqxxzb where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                    res_yw_sqxxzb_bz2 = djObj.fetchone(sql_yw_sqxxzb_bz2)
                    if not res_yw_sqxxzb_bz2:
                        logger.error("yw_sqxxzb表查询主业务号为空")
                        sys.exit(-1)
                    logger.debug("yw_sqxxzb表查询主业务号为：%s" % res_yw_sqxxzb_bz2)
                    return res_yw_sqxxzb_bz2
                # 按幢发证 或 其他批量业务
                sql_yw_sqxxzb_ywh = "select ywh from yw_sqxxzb where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxxzb_ywh = djObj.fetchone(sql_yw_sqxxzb_ywh)
                if not res_yw_sqxxzb_ywh:
                    logger.error("yw_sqxxzb表查询子ywh为空")
                    sys.exit(-1)
                logger.debug("yw_sqxxzb表查询子ywh为：%s" % res_yw_sqxxzb_ywh)
                return res_yw_sqxxzb_ywh
            else:
                sql_yw_sqxx_ywh = "select ywh from yw_sqxx where ajzt='2' and to_char(cjsj,'yyyy-mm-dd') = to_char(sysdate,'yyyy-mm-dd') and ywlx ='" + ywlxID + "' and bdcdyh='" + bdcdyh + "'"
                res_yw_sqxx_ywh = djObj.fetchone(sql_yw_sqxx_ywh)
                if not res_yw_sqxx_ywh:
                    logger.error("yw_sqxx表查询ywh为空")
                    sys.exit(-1)
                logger.debug("yw_sqxx表查询ywh为：%s" % res_yw_sqxx_ywh)
                return res_yw_sqxx_ywh
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>产权类<<<<<<<<<<<<'''
    # 获取产权关联数据（id,djbid,zsbid）
    def getCqRealtionData(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)

        ywh = self.getYwh(bdcdyh,data)

        try:
            # 净地
            if cqType == 0:
                sql_dj_jsydsyq_data = "select id,djbid,zsbid from dj_jsydsyq where ywh='" + ywh + "'"
                res_dj_jsydsyq_data = djObj.fetchone2(sql_dj_jsydsyq_data)
                if not res_dj_jsydsyq_data:
                    logger.error("业务号【%s】未查询到关联关系" %ywh)
                    sys.exit(-1)
                logger.debug("dj_jsydsyq表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_jsydsyq_data)
                return  res_dj_jsydsyq_data
            elif cqType == 1:
                # 整体发证 如项目类多幢
                if sfztfz == 1:
                    sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where bz2='" + ywh + "'"
                    res_dj_fdcq2_data = djObj.fetchone2(sql_dj_fdcq2_data)
                    if not res_dj_fdcq2_data:
                        logger.error("业务号【%s】未查询到关联关系" % ywh)
                        sys.exit(-1)
                    logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
                    return res_dj_fdcq2_data
                # 按幢发证或按单元发证
                sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where ywh='" + ywh + "'"
                res_dj_fdcq2_data = djObj.fetchone2(sql_dj_fdcq2_data)
                if not res_dj_fdcq2_data:
                    logger.error("业务号【%s】未查询到关联关系" % ywh)
                    sys.exit(-1)
                logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
                return res_dj_fdcq2_data
            else:
                logger.error("产权类型【cqType】未传值，请检查yml文件")
                sys.exit(-1)
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取产权注销关联数据（id,djbid,zsbid）
    def getCqCancelRealtionData(self,bdcdyh,data):
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)

        ywh = self.getYwh(bdcdyh,data)

        try:
            # 净地
            if cqType == 0:
                sql_dj_jsydsyq_data = "select id,djbid,zsbid from dj_jsydsyq where zxywh='" + ywh + "'"
                res_dj_jsydsyq_data =djObj.fetchone2(sql_dj_jsydsyq_data)
                if not res_dj_jsydsyq_data:
                    logger.error("业务号【%s】未查询到关联关系" % ywh)
                    sys.exit(-1)
                logger.debug("dj_jsydsyq表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_jsydsyq_data)
                return  res_dj_jsydsyq_data
            elif cqType == 1:
                sql_dj_fdcq2_data = "select id,djbid,zsbid from dj_fdcq2 where zxywh='" + ywh + "'"
                res_dj_fdcq2_data = djObj.fetchone2(sql_dj_fdcq2_data)
                if not res_dj_fdcq2_data:
                    logger.error("业务号【%s】未查询到关联关系" % ywh)
                    sys.exit(-1)
                logger.debug("dj_fdcq2表id,djbid,zsbid分别为：%s，%s，%s" % res_dj_fdcq2_data)
                return res_dj_fdcq2_data
            else:
                logger.error("产权类型【cqType】未传值，请检查yml文件")
                sys.exit(-1)
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>抵押类<<<<<<<<<<<<'''
    # 获取抵押关联数据（id,djbid,zsbid）
    def getDyRealtionData(self, bdcdyh, data):
        ywh = self.getYwh(bdcdyh, data)

        try:
            sql_dj_dy_data = "select id,djbid,zsbid,cqbid from dj_dy where ywh='" + ywh + "'"
            res_dj_dy_data = djObj.fetchone2(sql_dj_dy_data)
            if not res_dj_dy_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_dy表id,djbid,zsbid,cqbid分别为：%s，%s，%s，%s" % res_dj_dy_data)
            return res_dj_dy_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取抵押注销关联数据（id,djbid,zsbid）
    def getDyCancelRealtionData(self, bdcdyh, data):
        ywh = self.getYwh(bdcdyh, data)

        try:
            sql_dj_dy_data = "select id,djbid,zsbid,cqbid from dj_dy where zxdyywh='" + ywh + "'"
            res_dj_dy_data = djObj.fetchone2(sql_dj_dy_data)
            if not res_dj_dy_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_dy表id,djbid,zsbid,cqbid分别为：%s，%s，%s，%s" % res_dj_dy_data)
            return res_dj_dy_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>预告类<<<<<<<<<<<<'''
    # 获取预告关联数据（id,djbid,zsbid，hid）
    def getYgRealtionData(self, bdcdyh, data):
        ywh = self.getYwh(bdcdyh, data)

        try:
            sql_dj_yg_data = "select id,djbid,zsbid,hid from dj_yg where ywh='" + ywh + "'"
            res_dj_yg_data = djObj.fetchone2(sql_dj_yg_data)
            if not res_dj_yg_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_yg表id,djbid,zsbid,hid：%s，%s，%s，%s" % res_dj_yg_data)
            return res_dj_yg_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取预告抵押关联数据（id,djbid,zsbid，hid）
    def getYdyRealtionData(self, bdcdyh, data):
        ywh = self.getYwh(bdcdyh, data)

        try:
            sql_dj_ydy_data = "select id,djbid,zsbid,hid from dj_ydy where ywh='" + ywh + "'"
            res_dj_ydy_data = djObj.fetchone2(sql_dj_ydy_data)
            if not res_dj_ydy_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_ydy表id,djbid,zsbid,hid：%s，%s，%s，%s" % res_dj_ydy_data)
            return res_dj_ydy_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    '''>>>>>>>>>>>>查封类<<<<<<<<<<<<'''
    # 获取查封关联数据（id,djbid,zsbid）
    def getCfRealtionData(self,bdcdyh,data):
        ywh = self.getYwh(bdcdyh,data)
        try:
            sql_dj_cf_data = "select id,djbid,cqbid from dj_cf where ywh='" + ywh + "'"
            res_dj_cf_data = djObj.fetchone2(sql_dj_cf_data)
            if not res_dj_cf_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_cf表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_cf_data)
            return res_dj_cf_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取预查封关联数据（id,djbid,zsbid）
    def getYcfRealtionData(self,bdcdyh,data):
        ywh = self.getYwh(bdcdyh,data)
        try:
            sql_dj_ycf_data = "select id,djbid,cqbid,hid from dj_ycf where ywh='" + ywh + "'"
            res_dj_ycf_data = djObj.fetchone2(sql_dj_ycf_data)
            if not res_dj_ycf_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_ycf表id,djbid,cqbid,hid分别为：%s，%s，%s，%s" % res_dj_ycf_data)
            return res_dj_ycf_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取司法裁定关联数据（id,djbid,zsbid）
    def getSfcdRealtionData(self,bdcdyh,data):
        ywh = self.getYwh(bdcdyh,data)
        try:
            sql_dj_qtxz_data = "select id,djbid,cqbid from dj_qtxz where ywh='" + ywh + "'"
            res_dj_qtxz_data = djObj.fetchone2(sql_dj_qtxz_data)
            if not res_dj_qtxz_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_qtxz表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_qtxz_data)
            return res_dj_qtxz_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)

    # 获取解封关联数据（id,djbid,zsbid）
    def getJfRealtionData(self,bdcdyh,data):
        ywh = self.getYwh(bdcdyh,data)
        try:
            sql_dj_cf_data = "select id,djbid,cqbid from dj_cf where jfywh='" + ywh + "'"
            res_dj_cf_data = djObj.fetchone2(sql_dj_cf_data)
            if not res_dj_cf_data:
                logger.error("业务号【%s】未查询到关联关系" % ywh)
                sys.exit(-1)
            logger.debug("dj_cf表id,djbid,cqbid分别为：%s，%s，%s" % res_dj_cf_data)
            return res_dj_cf_data
        except Exception as e:
            logger.error("数据查询异常,具体详见：%s" % e)
            sys.exit(-1)