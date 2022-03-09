#封装流程受理（申请表）
'''
:param driver  浏览器驱动
'''
import time, sys
from Common.ToolsForOpertion import WebTools
from Common.LogFunc import loggerConf
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementNotVisibleException

logger = loggerConf().getLogger()

class sqbPage():
    def __init__(self,driver):
        self.driver = driver

    def sqbHandle(self, data):
        '''
        封装申请表页面
        :param bdcdyh 受理件不动产单元号
        :param data (dict)
            :param lcInfo (dict)
                :param qllx: 权利类型,
                :param djlx: 登记类型（optional）
                :param ywlxID: 业务类型ID
            :param params (dict)
                :param ywxl :业务小类
                :param sffz :是否发证（1-发证）
                :param sfpl :是否批量（1-批量）
                :param cqType :产权类型（0-净地，1-房屋）
        :return:
        '''
        qllx = data.get('initdata').get('lcInfo',None).get('qllx',None)
        djlx = data.get('initdata').get('lcInfo', None).get('djlx', None)
        ywlxID = data.get('initdata').get('lcInfo', None).get('ywlxID', None)
        ywxl = data.get('initdata').get('params', None).get('ywxl', None)
        sfpl = data.get('initdata').get('params', None).get('sfpl', None)
        sfztfz = data.get('initdata').get('params', None).get('sfztfz', None)
        cqType = data.get('initdata').get('params', None).get('cqType', None)
        sfydy = data.get('initdata').get('params', None).get('sfydy', None)
        sfdyzx = data.get('initdata').get('params', None).get('sfdyzx', None)

        WebTools(self.driver).check_element_is_exists('link_text','申请表')
        WebTools(self.driver).mouse_click('link_text','申请表')

        # 将页面滚动条拖到顶部
        self.driver.execute_script("document.documentElement.scrollTop=0")
        time.sleep(1)

        try:
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@xid='ywh']")))
        # 批量查封/
        except (NoSuchElementException,TimeoutException,ElementNotVisibleException):
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[@xid='sqbTable']//input[@xid='YWH']")))
        except (NoSuchElementException,TimeoutException,ElementNotVisibleException):
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@xid='YWH']")))
        except Exception as e:
            logger.error("申请表页面【业务号】字段加载失败,错误信息：%s" %e)
            sys.exit(-1)

        # 因数据问题，部分环境数据不满足要求
        if qllx == '国有建设用地使用权':
            if djlx == '首次登记':
                # 独用土地面积
                WebTools(self.driver).input_clear('xpath', "//input[@xid='tdsyqdymj']")
                WebTools(self.driver).input_content('xpath', "//input[@xid='tdsyqdymj']", '0.01')
        elif qllx =='国有建设用地使用权及房屋所有权':
            if djlx != '注销登记':
                # 是否整体发证处理（涉及项目类多幢，在建工程抵押，批量抵押等）
                # 整体发证
                if sfztfz == 1:
                    WebTools(self.driver).mouse_click('xpath',"//input[@name='SFZTFZ' and @value='1']")
                # 按幢发证
                elif sfztfz == 0:
                    WebTools(self.driver).mouse_click('xpath', "//input[@name='SFZTFZ' and @value='0']")

                # 权利其他状况，其他，附记处理
                ywlxList=[
                    '191B4FB37DD148448BC64944C01A78C1',   # 建筑物区分业主共有部分
                    'F711B2126C44409D903254C246FCD569',   # 房屋首次登记
                    '7E9CABA30D4749D499654390D0ED4DDB',   # 批量转移
                    '608286609F5C429CB32BA42C56F7C7F7',   # 项目类多幢首次
                ]

                # 建筑物区分业主共有部分，房屋首次登记，批量转移不生成
                if ywlxID not in ywlxList:
                    # 将页面滚动条拖到底部
                    self.driver.execute_script("document.documentElement.scrollTop=550")
                    # 生成权利其他状况
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createQL']")
                    # 生成附记
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createFJ']")
        elif qllx =='抵押权':
            if djlx != '注销登记':
                #预置数据（当前时间）
                currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                #预置数据（抵押结束时间）
                fetureDate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * 365 * 10))

                #抵押方式
                WebTools(self.driver).choose_droplist_value('DYFS', 'xpath', "//select[@name='DYFS']/option[2]")
                # 抵押不动产类型
                if cqType == 0:
                    WebTools(self.driver).choose_droplist_value('DYBDCLX', 'xpath', "//select[@name='DYBDCLX']/option[2]")
                elif cqType == 1:
                    WebTools(self.driver).choose_droplist_value('DYBDCLX', 'xpath', "//select[@name='DYBDCLX']/option[3]")
                else:
                    logger.error("产权类型【cqType】未传值，请检查yml文件")
                    sys.exit(-1)
                # 抵押合同签订日期
                WebTools(self.driver).input_content('xpath', "//input[@xid='DYHTQDRQ']", currentDate)
                # 债务履行起始时间
                WebTools(self.driver).input_content('xpath', "//input[@xid='ZWLXQSSJ' or @xid='zwlxqssj']", currentDate)
                # 债务履行结束时间
                WebTools(self.driver).input_content('xpath', "//input[@xid='ZWLXJSSJ' or @xid='zwlxjssj']", fetureDate)
                if sfpl == 1:
                    # 担保范围
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='dbfw' or @xid='DBFW']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='dbfw' or @xid='DBFW']", '房屋产权')
                    # 是否存在禁止或限制转让不动产的约定
                    WebTools(self.driver).mouse_click('xpath',"//input[@name='SFXZZR' and @value='0']")
                    # 整体发证
                    if sfztfz == 1:
                        WebTools(self.driver).mouse_click('xpath', "//input[@name='SFZTFZ' and @value='1']")
                        # 总抵押金额
                        WebTools(self.driver).input_content('xpath', "//input[@xid='bdbzqse' or @xid='BDBZQSE']", '2000')
                    # 按单元发证
                    elif sfztfz == 0:
                        WebTools(self.driver).mouse_click('xpath', "//input[@name='SFZTFZ' and @value='0']")
                else:
                    # 不动产价值
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='dywjz']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='dywjz']", '100')
                    # 被担保主债权数额
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='bdbzqse']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='bdbzqse']", '80')
                    # 将页面滚动条拖到指定元素（登记原因）
                    WebTools(self.driver).srollBarToElement("//textarea[@xid='djyy']")
                    # 是否存在禁止或限制转让不动产的约定
                    WebTools(self.driver).mouse_click('xpath', "//input[@name='SFXZZR' and @value='0']")
                    # 最高债权确定事实和数额
                    WebTools(self.driver).input_clear('xpath', "//textarea[@xid='ZGZQQDSSJSE']")
                    WebTools(self.driver).input_content('xpath', "//textarea[@xid='ZGZQQDSSJSE']", '50')
                    # 担保范围
                    WebTools(self.driver).input_clear('xpath', "//textarea[@xid='dbfw']")
                    WebTools(self.driver).input_content('xpath', "//textarea[@xid='dbfw']", '房屋产权')
                    # 将页面滚动条拖到指定元素（附记）
                    WebTools(self.driver).srollBarToElement("//textarea[@xid='fj']")
                    # 其他
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createQT']")
                    # 附记
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createFJ']")
                    time.sleep(1)
        elif qllx == '查封登记':
            # 预置数据（当前时间(年月日)）
            currentDate = time.strftime('%Y-%m-%d')
            # 预置数据（当前时间（年月日时分秒））
            currentTime = time.strftime('%Y%m%d-%H%M%S')

            # 首封类业务
            ywlxList = [
                        '80E93B91E9974F98AAE75C6AD28629B1', # 批量查封（净地和房地）
                        'A7325035C9E24F7784B50AC1E965FFD7', # 预查封
                        '7C472DAB0C1D46E1B782689C057B552E', # 批量预售合同查封
                        '9549D08993DB44138AC1A433A346C3BC', # 土地小证查封
                        ]
            # 续查封类业务
            ywlxList2 = [
                        '24A5B1DEA6124BCEA1C38626996BFF97',  # 批量续查封登记(净地和房地)
                        '6559D6E5FB7044D3999FBF2EC76A176B',  # 批量续预查封
                        '819B16A603D4467D882268FF9CE83C02',  # 土地小证续查封
                        ]

            # 司法裁定
            ywlxList3 = [
                        '9AB6783AEDAB4D6CBFF8C7F19D411BE7',  # 批量司法裁定(房地)
                        'EF4D6596ED6347DDA33471FCFA7E973A',  # 批量司法裁定(净地)
                        'AEBFF1F998D846CB932F7CC0ECA0ACAF',  # 预告司法裁定（房地）
                        'EB661D9603EF48E895503BDBC82EADAA',  # 预告司法裁定（净地）
                        ]

            # 首封
            if ywlxID in ywlxList:
                # 查封机关
                WebTools(self.driver).input_content('xpath',"//th[contains(text(),'查封机关')]/../td[1]/input[1]",'北京市中级人民法院')
                # 查封文件名称
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'查封文件名称')]/../td[1]/input[1]",'xx查封文件')
                # 查封文号
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'查封文号')]/../td[1]/input[1]", currentTime)
                # 申请执行人
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'申请执行人')]/../td[1]/input[1]",'张三')
                # 查封起始日期
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'查封起始日期')]/../td[1]/input[1]", currentDate)
                # 查封期限
                WebTools(self.driver).mouse_click('xpath', "//input[@xid='btnAdd2']")
                # 来文日期
                WebTools(self.driver).input_clear('xpath', "//th[contains(text(),'来文日期')]/../td[2]/input[1]")
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'来文日期')]/../td[2]/input[1]", currentDate)
                # 查封范围
                WebTools(self.driver).input_content('xpath',"//th[contains(text(),'查封范围')]/../td[1]/input[1]","该产权所有，包括附着物（测试）。")
                # 查封冻结原因
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'查封冻结原因')]/..//textarea[1]", "债务纠纷，依法查封。")
            # 司法裁定（净地和房屋）
            elif ywlxID in ywlxList3:
                # 申请执行人
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'申请执行人')]/../td[1]/input[1]",'张三')
                # 裁决机关
                WebTools(self.driver).input_content('xpath',"//th[contains(text(),'裁决机关')]/../td[1]/input[1]",'北京市中级人民法院')
                # 裁决文件
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'裁决文件')]/../td[2]/input[1]",'xx查封文件')
                # 裁决文号
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'裁决文号')]/../td[1]/input[1]", currentTime)
                # 来文日期
                WebTools(self.driver).input_clear('xpath', "//th[contains(text(),'来文日期')]/../td[2]/input[1]")
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'来文日期')]/../td[2]/input[1]", currentDate)
                # 是否注销抵押(默认是否)
                if sfdyzx == 1:
                    WebTools(self.driver).mouse_click('xpath',"//input[@name='SFZXDY' and @value='1']")
                # 裁决原因
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'裁决原因')]/..//textarea[1]", "存在和银行的财务纠纷(银行向法院申请查封)")
            # 续查封
            elif ywlxID in ywlxList2:
                # 申请执行人
                WebTools(self.driver).input_clear('xpath', "//th[contains(text(),'申请执行人')]/../td[1]/input[1]")
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'申请执行人')]/../td[1]/input[1]", '张三')
                # 查封起始日期
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'查封起始日期')]/../td[1]/input[1]", currentDate)
                # 查封期限
                WebTools(self.driver).mouse_click('xpath', "//input[@xid='btnAdd2']")
                # 查封冻结原因
                WebTools(self.driver).input_content('xpath', "//textarea[@xid='cfdjyy' or @xid='CFDJYY'] ", "查封到期依法执行续查封。")
            # 解封登记(房屋解封、净地解封、房屋批量解封、净地批量解封)
            if ywlxID=='FB265E54DBE24577B2FA4F4C4980AB15' or ywlxID == '08B3B1B8F1FD47188C115939E2814AFF' or ywlxID == '4D22B4174EFD42BCA3C01FE58D9F1477' or ywlxID == '22CF4018956C44338B4A2B51EB1CB111' :
                # 将页面滚动条拖到底部
                self.driver.execute_script("document.documentElement.scrollTop=3000")
                WebTools(self.driver).check_element_is_exists('xpath',"//input[@xid='jfjg']")
                #解封机关
                WebTools(self.driver).input_content('xpath',"//input[@xid='jfjg']",'南京市中级人民法院')
                #解封文号
                WebTools(self.driver).input_content('xpath',"//input[@xid='jfwh']",currentTime)
                #解封时间
                # WebTools(self.driver).input_content('xpath',"//input[@xid='jfsj']",currentDate)
                #解封原因
                WebTools(self.driver).input_content('xpath', "//textarea[@xid='jfyy']", "债务已清，予以解封。")
        elif qllx == '其他登记':
            # 预置数据（当前时间(年月日)）
            currentDate = time.strftime('%Y-%m-%d')
            # 预置数据（当前时间（年月日时分秒））
            currentTime = time.strftime('%Y%m%d-%H%M%S')
            # 房屋，净地
            if ywlxID == 'ACAF8531B13B43FC8CB4D521E46FCA58' or ywlxID == 'C2A770118E79445EB50E0108E1BCA69D':
                # 冻结机关
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'冻结机关')]/../td[1]/input[1]", '北京市中级人民法院')
                # 冻结文号
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'冻结文号')]/../td[1]/input[1]", currentTime)
                # 冻结起始日期
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'冻结起始日期')]/../td[1]/input[1]",currentDate)
                # 冻结截止日期
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'冻结截止日期')]/../td[2]/input[1]",currentDate)
                # 来文日期
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'来文日期')]/../td[2]/input[1]", currentDate)
                # 冻结类型
                WebTools(self.driver).mouse_click('xpath',"//td[@xid='djxzlxTd']//input[1]")
                # 冻结原因
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'冻结原因')]/..//textarea[1]","存在纠纷,予以冻结")
            elif ywlxID == '009B74A8CD6C42C18B6F2C0F16FAC912' or ywlxID == 'CA64F346B5F74F51918D47FA64A00373':
                # 解冻机关
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'解冻机关')]/../td[1]/input[1]",'北京市中级人民法院')
                # 冻结文号
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'解冻文号')]/../td[1]/input[1]", currentTime)
                # 解冻时间
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'解冻时间')]/../td[2]/input[1]",currentDate)
                # 解冻原因
                WebTools(self.driver).input_content('xpath', "//th[contains(text(),'解冻原因')]/..//textarea[1]","纠纷解除,予以解冻")
        elif qllx == '预告登记':
            if djlx != '注销登记':
                # 预抵押
                if sfydy:
                    # 预置数据（开始时间）
                    currentDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    # 预置数据（结束时间）
                    fetureDate = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400 * 365 * 10))

                    # 将页面滚动条拖动中间
                    self.driver.execute_script("document.documentElement.scrollTop=300")
                    # 抵押方式
                    WebTools(self.driver).choose_droplist_value('DYFS', 'xpath', "//select[@name='DYFS']/option[2]")
                    # 抵押不动产类型
                    if cqType == 0:
                        WebTools(self.driver).choose_droplist_value('DYBDCLX', 'xpath', "//select[@name='DYBDCLX']/option[2]")
                    elif cqType == 1:
                        WebTools(self.driver).choose_droplist_value('DYBDCLX', 'xpath', "//select[@name='DYBDCLX']/option[3]")
                    else:
                        logger.error("产权类型【cqType】未传值，请检查yml文件")
                        sys.exit(-1)
                    # 是否存在禁止或限制转让不动产的约定
                    WebTools(self.driver).mouse_click('xpath', "//input[@name='SFXZZR' and @value='0']")
                    # 不动产价值
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='dywjz']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='dywjz']", '100')
                    # 被担保主债权数额
                    WebTools(self.driver).input_clear('xpath', "//input[@xid='bdbzqse']")
                    WebTools(self.driver).input_content('xpath', "//input[@xid='bdbzqse']", '80')
                    # 抵押合同签订日期
                    WebTools(self.driver).input_content('xpath', "//input[@xid='DYHTQDRQ']", currentDate)
                    # 债务履行起始时间
                    WebTools(self.driver).input_content('xpath', "//input[@xid='zwlxqssj']", currentDate)
                    # 债务履行结束时间
                    WebTools(self.driver).input_content('xpath', "//input[@xid='zwlxjssj']", fetureDate)
                    # 最高债权确定事实和数额
                    WebTools(self.driver).input_clear('xpath', "//textarea[@xid='ZGZQQDSSJSE']")
                    WebTools(self.driver).input_content('xpath', "//textarea[@xid='ZGZQQDSSJSE']", '50')
                    # 担保范围
                    WebTools(self.driver).input_content('xpath', "//textarea[@xid='dbfw']", '产权证')
                    # 将页面滚动条拖到附记
                    WebTools(self.driver).srollBarToElement("//textarea[@xid='fj']")
                    # 其他
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createQT']")
                    # 附记
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createFJ']")
                    time.sleep(1)
                # 预告
                else:
                    # 商品房预告首次
                    if ywlxID == '1CEDE7DF7E0F481BB5AF3C8700028F1B':
                        # 预告登记种类
                        if ywxl == '预售商品房预告登记':
                            WebTools(self.driver).choose_droplist_value('YGDJZL', 'xpath',"//select[@name='YGDJZL']/option[2]")
                        elif ywxl == '其它不动产买卖预告登记':
                            WebTools(self.driver).choose_droplist_value('YGDJZL', 'xpath',"//select[@name='YGDJZL']/option[3]")
                    # 将页面滚动条拖到底部
                    self.driver.execute_script("document.documentElement.scrollTop=3000")
                    # 其他
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createQT']")
                    # 附记
                    WebTools(self.driver).mouse_click('xpath', "//span[@xid='createFJ']")
                    time.sleep(1)

        # 滚动条拖到顶部
        self.driver.execute_script("document.documentElement.scrollTop=0")
        ywlxList = [
            'F49EEFC631414825BD7B93A84F7A355E',  # 净地抵押首次
            '6DD4B4B44C724FCAAEF3A21BD49E1232',  # 不动产抵押
            '7FCA6894051F46CDBC603DE0E430D1EA',  # 预抵押转现
            'BAA801115B3740868F1C8824102CABC7',  # 不动产抵押注销
        ]
        # 部分流程提交会出现申请表未保存【规避】
        if ywlxID in ywlxList:
            WebTools(self.driver).mouse_click('xpath', '//span[@functionname="saveBtnClick"]')
            time.sleep(4)
