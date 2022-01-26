'''
    公共校验
    针对流程入口数据检查
'''
from dbAction.dbHelper import DJ_DB, QJ_DB
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

class verificator():
    def __init__(self):
        self.djObj = DJ_DB()
        self.qjObj = QJ_DB()

    # 多条产权数据校验（内蒙古允许）
    def tooManyCqResultVerify(self,type,queryData,*args):
        '''
        :param type: 0 净地；1 房地
        :param queryData: 查询入参
        :param *args: tuple  0 内蒙；1 江苏
        :return:
        '''
        if type == 0:
            queryJsydsyqSQL = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
            queryTdxxSQL = "select count(1) from dj_tdxx where zt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
            queryjsydsyqSQLRes = self.djObj.fetchone(queryJsydsyqSQL)
            queryTdxxSQLRes = self.djObj.fetchone(queryTdxxSQL)
            if queryjsydsyqSQLRes > 1:
                logger.error("该单元在dj_jsydsyq存在多条现势数据，请检查！")
                return
            #args 参数区别江苏版本和内蒙版本，内蒙版本存在一地多证 即dj_jsydsyq表一条数据，dj_tdxx表多条数据
            if args:
                if args[0] == 1:
                    if queryTdxxSQLRes >1:
                        logger.error("该单元在dj_tdxx表存在多条现势数据，请检查！")
                        return
            return True
        elif type == 1:
            queryFdcq2SQL = "select count(1) from dj_fdcq2 where zt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
            queryHxxSQL = "select count(1) from dj_hxx where zt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
            queryFdcq2SQLRes = self.djObj.fetchone(queryFdcq2SQL)
            queryHxxSQLRes = self.djObj.fetchone(queryHxxSQL)
            if queryFdcq2SQLRes > 1 or queryHxxSQLRes > 1:
                logger.warning("该单元在dj_fdcq2或dj_hxx存在多条现势数据，请检查！")
                return
            return True
        else:
            logger.error("参数不符合要求，请检查！")
            return

    # 在办件校验
    def processVerify(self,queryData):
        '''
        :param queryData: 查询入参
        :return:
        '''
        querySqxxSQL = "select count(1) from yw_sqxx where ajzt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
        querySqxxzbSQL = "select count(1) from yw_sqxx t where t.SFYX = '1' and t.ajzt in ('1', '3', '6') and t.id in (select z.sqbid from yw_sqxxzb z where z.sfyx = '1' and bdcdyh = '" + queryData + "')"
        querySqxxSQLRes = self.djObj.fetchone(querySqxxSQL)
        querySqxxzbSQLRes = self.djObj.fetchone(querySqxxzbSQL)
        if querySqxxSQLRes or querySqxxzbSQLRes:
            logger.warning("该数据已在办理中，重新获取数据！")
            return
        return True

    # 净地是否已登记校验
    def landIsRegisterVerify(self,queryData):
        '''
        :param queryData: 查询入参
        :return:
        '''
        # 检查该数据是否在登记平台做过登记,如果做过登记，发起流程会校验住，确保数据在权藉存在，在登记平台未做过登记
        queryJsydsyqSQL = "select count(1) from dj_jsydsyq where zt='1' and sfyx=1 and (bdcdyh='" + queryData + "' or zddm='" + queryData + "')"
        queryJsydsyqSQLRes = self.djObj.fetchone(queryJsydsyqSQL)
        if queryJsydsyqSQLRes:
            logger.warning("登记平台该土地信息已登记")
            return
        return True

    # 房地是否已登记校验
    def houseIsRegisterVerify(self,queryData):
        '''
        :param queryData: 查询入参
        :return:
        '''
        queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and sfysczql=1 and bdcdyh='" + queryData + "'"
        queryDjbenSQLRes = self.djObj.fetchone(queryDjbenSQL)
        if queryDjbenSQLRes:
            logger.warning("登记平台该房屋信息已登记")
            return
        return True

    # 多条登记本数据校验
    def tooManyDjbenResultVerify(self,queryData):
        '''
        :param queryData: 查询入参
        :return:
        '''
        queryDjbenSQL = "select count(1) from dj_djben where zt='1' and sfyx=1 and bdcdyh='" + queryData + "'"
        queryDjbenSQLRes = self.djObj.fetchone(queryDjbenSQL)
        if queryDjbenSQLRes != 1:
            logger.warning("查询单元存在多条现势登记本记录或不存在现势记录")
            return
        return True

    # 多条产权宽表数据校验
    def tooManyCqFdcq2DjbenZsResultVerify(self,queryData):
        '''
        :param queryData: 查询入参
        :return:
        '''
        queryDjbenSQL = "select count(1) from dj_fdcq2_djben_zs where sfyx=1 and bdcdyh='" + queryData + "'"
        queryDjbenSQLRes = self.djObj.fetchone(queryDjbenSQL)
        if queryDjbenSQLRes != 1:
            logger.warning("查询单元存在多条现势产权宽表记录或不存在现势记录")
            return
        return True

    # 产权下是否有附属设施校验
    def fsssIsExistsVerify(self,queryData):
        # 检查该数据是否有附属设施（3.0版本校验）
        queryFsssSQL = "select id from dj_fsss t where zt='1' and sfyx=1 and ssbdcdyh='" + queryData + "'"
        queryFsssRes = self.djObj.fetchone(queryFsssSQL)
        # dj_fsss若有值，则需校验dj_fsssxx也需有值
        if queryFsssRes:
            logger.debug("主产权下存在附属设施信息。")
            queryFsssxxSQL = "select count(1) from dj_fsssxx where cqbid='" + str(queryFsssRes) + "'"
            queryFsssxxRes = self.djObj.fetchone(queryFsssxxSQL)
            if not queryFsssxxRes:
                logger.error("DJ_FSSSXX表数据为空，不符合业务办理条件，重新查找数据。")
                return
            return True
        else:
            return True

