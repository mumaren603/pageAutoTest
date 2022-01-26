#封装流程受理（不动产基本信息）
'''
:param driver  浏览器驱动
'''
import time
from Common.ToolsForOpertion import WebTools
from pageObject.queryFunc import queryFunc
from Common.LogFunc import loggerConf
import sys

logger = loggerConf().getLogger()

class bdcjbxxPage():
    def __init__(self,driver):
        self.driver = driver

    def bdcjbxxHandle(self,data,*args):
        '''
        封装不动产基本信息页面
        :param data (dict)
            :param lcInfo (dict)
                :param qllx: 权利类型,
                :param djlx: 登记类型（optional）
                :param ywlxID: 业务类型ID
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)


        WebTools(self.driver).check_element_is_exists('link_text','不动产基本信息')
        WebTools(self.driver).mouse_click('link_text', '不动产基本信息')

        # 等待页面元素加载
        # 批量
        if sfpl == 1:
            WebTools(self.driver).check_element_is_exists('xpath', "//div[@xid='headTitle']")
        #建筑物区分业主共有部分 需特别处理，属于批量流程，但yml中sfpl参数不赋值，因为涉及到数据查询。
        elif ywlxID == '191B4FB37DD148448BC64944C01A78C1':
            WebTools(self.driver).check_element_is_exists('xpath', "//div[@xid='headTitle']")
        # 非批量
        else:
            if cqType == 0:
                WebTools(self.driver).check_element_is_exists('xpath', "//span[contains(text(),'土地信息')]")
            elif cqType == 1:
                WebTools(self.driver).check_element_is_exists('xpath', "//span[contains(text(),'不动产信息')]")
            else:
                logger.error("产权类型【cqType】未传值，请检查yml文件")
                sys.exit(-1)

        if qllx =='国有建设用地使用权及房屋所有权':
            # 分户转移
            if ywlxID == 'CD62B1699DEB4496AF8D5D5590E945AB':
                # 因为该流程区别于其他流程，在不动产基本信息页面查询入参数据，需要参数bdcdyh;且待登记数据需要分配权利人，所以需要计算待登记数据条数，需要参数fsssxxCount
                bdcdyh = args[0]
                fsssxxCount = args[1]
                logger.debug("args第一个参数值（bdcdyh）为：%s" % bdcdyh)
                logger.debug("args第二个参数值(dj_fsssxx条数)为：%s" % fsssxxCount)

                WebTools(self.driver).check_element_is_exists('xpath', "//*[contains(text(),'待登记不动产单元')]")
                WebTools(self.driver).mouse_click('xpath', "//*[contains(text(),'待登记不动产单元')]/../..//*[contains(text(),'新增')]")

                # 调用不动产单元查询功能
                queryFunc(self.driver).query(bdcdyh, data)
                # WebTools(self.driver).allow_element_is_exists('class_name', 'BeAlert_box')

                for i in range(fsssxxCount):
                    # 分配权利人
                    i += 1
                    WebTools(self.driver).mouse_click('xpath', "//table[@xid='table3']//tbody/tr[" + str(i) + "]/td[1]/div[2]")
                    WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='SFCZ0']")
                    WebTools(self.driver).mouse_click('xpath', "//div[@xid='_compose_splitQlrDialog_']//*[@xid='confirm']")
                    WebTools(self.driver).allow_element_is_exists('class_name', 'BeAlert_box')
            # 批量转移，建筑物区分业主共有部分
            elif ywlxID == '7E9CABA30D4749D499654390D0ED4DDB' or ywlxID == '191B4FB37DD148448BC64944C01A78C1':
                pass
            # 项目类多幢
            elif ywlxID == '608286609F5C429CB32BA42C56F7C7F7':
                # 新增
                bdcdyh = args[0]
                logger.debug("args第一个参数值（bdcdyh）为：%s" % bdcdyh)
                WebTools(self.driver).check_element_is_exists('xpath',"//span[@xid='insert']")
                WebTools(self.driver).mouse_click('xpath', "//span[@xid='insert']")
                # 调用不动产单元查询功能
                queryFunc(self.driver).bdcjbxxQuery(bdcdyh, data)
                # 批量生成附记
                # WebTools(self.driver).check_element_is_exists('xpath',"//span[@xid='generate']")
                # WebTools(self.driver).mouse_click('xpath',"//span[@xid='generate']")
            else:
                WebTools(self.driver).input_clear('xpath','//input[@xid="QDJG"]')
                WebTools(self.driver).input_content('xpath','//input[@xid="QDJG"]',80)
        elif qllx == '国有建设用地使用权':
            WebTools(self.driver).check_element_is_exists('xpath', '//td[@xid="TDQLXZ"]')






