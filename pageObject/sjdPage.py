'''
**封装流程受理（收件单）**
:param driver  浏览器驱动
:bdcdyh 不动产单元号，区分净地和房屋
'''
import time
from Common.CommonFunc import WebTools

class sjdPage():
    def __init__(self,driver):
        self.driver = driver

    def sjdHandle(self,data):
        '''
        流程发起菜单，包括一级菜单、二级菜单、三级菜单
        :param bdcdyh 受理件不动产单元号
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
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        ywxl = data.get('initdata').get('params', None).get('ywxl', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sffz = data.get('initdata').get('params', None).get('sffz', None)

        WebTools(self.driver).mouse_click('link_text','收件单')
        time.sleep(1)
        WebTools(self.driver).check_element_is_exists('xpath', "//*[@xid='sjdTable']//input[@xid='YWH']")

        # # 根据是否批量判断刚进入流程是单个流程还是批量流程
        # if sfpl == 1:
        #     WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='YWH']")
        # else:
        #     WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='YWH']")

        if qllx == '国有建设用地使用权':
            # 转移登记(净地)
            if ywlxID ==167090000064:
                if ywxl == '买卖':
                    WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[3]")
                elif ywxl == '建设用地转移登记':
                    WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[4]")
        elif qllx == '国有建设用地使用权及房屋所有权':
            # 房屋首次转移登记
            if ywxl:
                if ywlxID == '807BD8C295404AA19F2275CB830E5F4C':
                    if ywxl == '市场化商品房转移登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[2]")
                    elif ywxl == '房改售房转移登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[3]")
                    elif ywxl == '经济适用房转移登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[4]")
                    elif ywxl == '征地拆迁安置房转移登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[5]")
                    else:
                        print("%s收件单业务小类必选！" % qllx)
                        return
                # 存量房转移登记
                elif ywlxID =='7CEA3E6E7C9D4D4194F77C2FB71FA0A4':
                    if ywxl == '存量房转移登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[2]")
                    else:
                        print("[%s]收件单业务小类必选！" % ywlxID)
                        return
                # 预转现登记
                elif ywlxID == '08B6FBC363E745C3ABF0DFDD13ECCD0B':
                    if ywxl == '市场化商品房预告转现登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[2]")
                    elif ywxl == '经济适用房预告转现登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[3]")
                    elif ywxl == '存量房预告转现登记':
                        WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[4]")
                    else:
                        print("%s收件单业务小类必选！" % qllx)
                        return
            else:
                pass
        # 房屋抵押
        elif qllx == '抵押权':
            pass
        # 查封登记--业务小类
        elif qllx == '查封登记':
            if ywxl:
                if ywxl == '查封':
                    WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[2]")
                elif ywxl == '轮候查封':
                    WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[3]")
                else:
                    print("%s收件单业务小类必选！" % qllx)
                    return
            # 司法裁定（房和地）
            if ywlxID == '4858445B1488454F970428A2436F54D5' or ywlxID == '8FEAF5CC34DF49C88B7E3139F8C0B18A' :
                if ywxl == '司法裁定':
                    WebTools(self.driver).choose_droplist_value('ywxl', 'xpath', "//select[@name='ywxl']/option[2]")



        # 是否发证
        if sffz == 1:
            # 领证地址
            WebTools(self.driver).choose_droplist_value('lzdz', 'xpath', '//select[@name="lzdz"]/option[2]')
            time.sleep(1)
