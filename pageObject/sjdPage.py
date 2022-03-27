import time,sys
from Common.ToolsForOpertion import WebTools
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

class sjdPage():
    def __init__(self,driver):
        '''
        :desc: 封装流程受理（收件单）
        :param driver: 浏览器驱动
        '''
        self.driver = driver

    def sjdHandle(self,data):
        '''
        流程发起菜单，包括一级菜单、二级菜单、三级菜单
        :param data (dict)
            :param lcInfo (dict)
                :param qllx: 权利类型,
                :param djlx: 登记类型（optional）
                :param ywlxID: 业务类型ID
            :param params (dict)
                :param ywxl :业务小类
                :param sffz :是否发证（1-发证）
                :param cqType :产权类型（0-净地，1-房屋）
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        ywxl = data.get('initdata').get('params', None).get('ywxl', None)
        sffz = data.get('initdata').get('params', None).get('sffz', None)

        WebTools(self.driver).check_element_is_exists('xpath', "//*[@xid='sjdTable']//input[@xid='YWH']")

        # 业务小类选择
        if qllx == '国有建设用地使用权及房屋所有权':
            # 房屋首次转移登记
            if ywxl:
                if ywlxID == '807BD8C295404AA19F2275CB830E5F4C':
                    if ywxl == '市场化商品房转移登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '1')
                    elif ywxl == '房改售房转移登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '2')
                    elif ywxl == '经济适用房转移登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '3')
                    elif ywxl == '征地拆迁安置房转移登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '4')
                    else:
                        logger.error("业务类型ID为[%s]收件单业务小类必选！" % ywlxID)
                        sys.exit(-1)
                # 存量房转移登记
                elif ywlxID =='7CEA3E6E7C9D4D4194F77C2FB71FA0A4':
                    if ywxl == '存量房转移登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '1')
                    else:
                        logger.error("业务类型ID为[%s]收件单业务小类必选！" % ywlxID)
                        sys.exit(-1)
                # 预转现登记
                elif ywlxID == '08B6FBC363E745C3ABF0DFDD13ECCD0B':
                    if ywxl == '市场化商品房预告转现登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '1')
                    elif ywxl == '经济适用房预告转现登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '2')
                    elif ywxl == '存量房预告转现登记':
                        WebTools(self.driver).choose_droplist('name', 'ywxl', '3')
                    else:
                        logger.error("业务类型ID为[%s]收件单业务小类必选！" % ywlxID)
                        sys.exit(-1)
            else:
                pass

        # 是否发证
        if sffz == 1:
            # 领证地址
            WebTools(self.driver).choose_droplist('name','lzdz','1')
            # time.sleep(1)
