import os
import time, datetime
# import allure
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.switch_to import SwitchTo
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()


class WebTools(object):
    '''
    func: 封装页面基本操作，如鼠标点击，输入框填写值，校验元素是否存在等
    '''

    def __init__(self, driver):
        self.driver = driver
        self.browser_type = None

    # 截屏
    def save_screenshot(self,img_doc):
        '''
        :param img_doc: 截图说明
        :return:
        '''
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
        errorPicDir = '/errorInfo'
        base_dir = base_dir+errorPicDir
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        errFilename = base_dir + '/error_' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + '.png'
        self.driver.save_screenshot(errFilename)

        # with open(errFilename, mode='rb')as f:
        #     data = f.read()
        # allure.attach(data, img_doc, allure.attachment_type.PNG)

    # 浏览器的设置
    def set_browser(self, url):
        '''
        :param url: 访问地址
        :return:
        '''
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(url)

    # # 打开浏览器
    # def open_browser(self, driver_path):
    #     '''
    #     :param driver_path: Driver物理路径
    #     :return:
    #     '''
    #     if self.browser_type == 'Firefox':
    #         self.driver = webdriver.Firefox(executable_path=driver_path)
    #     elif self.browser_type == 'Chrome':
    #         self.driver = webdriver.Chrome(executable_path=driver_path)
    #     elif self.browser_type == 'IE':
    #         self.driver = webdriver.Ie(executable_path=driver_path)
    #     elif self.browser_type == '' or self.browser_type == None:
    #         logger.error("未指定浏览器类型！")
    #     self.driver.maximize_window()

    # 显性等待时间
    def WebDriverWait(self, MaxTime, Mimtime, value):
        element = self.driver.find_element(By.ID, value)
        WebDriverWait(self.driver, MaxTime, Mimtime).until(EC.presence_of_element_located(element))

    # 切换到iframe上
    def switch_iframe(self, val, type=None):
        # 通过id, name切换（需唯一）
        if type is None:
            SwitchTo(self.driver).frame(val)
        else:
            webElemenet = None
            if type == 'xpath':
                webElemenet = self.driver.find_element(By.XPATH,val)
            elif type == 'css_selector':
                webElemenet = self.driver.find_element(By.CSS_SELECTOR,val)
            SwitchTo(self.driver).frame(webElemenet)

    # 从iframe切回原界面
    def switch_back_iframe(self):
        SwitchTo(self.driver).default_content()

    # 隐式等待
    def wait(self, seconds):
        self.driver.implicitly_wait(seconds)

    # 切换到新窗口
    def current_handle(self):
        all_handles = self.driver.window_handles
        for handle in all_handles:
            self.driver.switch_to.window(handle)

    # 获取元素
    def __getElement(self,type,val):
        global elm
        try:
            if type == "xpath":
                elm = self.driver.find_element(By.XPATH, val)
            elif type == "class_name":
                elm = self.driver.find_element(By.CLASS_NAME, val)
            elif type == "id":
                elm = self.driver.find_element(By.ID, val)
            elif type == "name":
                elm = self.driver.find_element(By.NAME, val)
            elif type == "link_text":
                elm = self.driver.find_element(By.LINK_TEXT, val)
            return elm
        except NoSuchElementException:
            logger.error("%s:%s元素未找到" % (type, val))
            self.save_screenshot('查找元素不存在')
            raise
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, val, e))
            self.save_screenshot('查找元素错误')
            raise

    # 输入内容
    def input_content(self, locType,locVal,val):
        element = self.__getElement(locType,locVal)
        element.send_keys(val)

    # 下拉框操作
    def choose_droplist(self,locType,locVal,val):
        '''
        :param locType:  下拉框元素定位类型，eg:name,id 一般使用name
        :param locVal:   待定位元素值
        :param val:      下拉框选项值,即页面option值
        :return:
        '''
        element = self.__getElement(locType, locVal)
        s = Select(element)
        s.select_by_value(val)

    # def choose_droplist_value(self, droplistName, type, value):
    #     '''
    #     :param droplistName: 下拉框name名字
    #     :param type: 下拉框值通过哪种方式选取
    #     :param value: 下拉框选取具体值
    #     :return:
    #     '''
    #     try:
    #         if type == "xpath":
    #             self.driver.find_element(By.NAME,droplistName)
    #             self.driver.find_element_by_name(droplistName).find_element_by_xpath(value).click()
    #         elif type == "class_name":
    #             self.driver.find_element_by_name(droplistName).find_element_by_class_name(value).click()
    #         elif type == "id":
    #             self.driver.find_element_by_name(droplistName).find_element_by_id(value).click()
    #         elif type == "name":
    #             self.driver.find_element_by_name(droplistName).find_element_by_name(value).click()
    #     except NoSuchElementException as e1:
    #         logger.error("%s:%s下拉框元素未找到;%s下拉框值选择失败" % (type, droplistName, value))
    #         self.save_screenshot('下拉框元素未找到。')
    #         raise e1
    #     except TimeoutException as e2:
    #         logger.error("%s:%s元素查找超时" % (type, droplistName))
    #         self.save_screenshot('查找元素超时')
    #         raise e2
    #     except Exception as e:
    #         logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
    #         self.save_screenshot('查找元素错误')
    #         raise e

    # 鼠标事件(单击)
    def mouse_click(self, locType,locVal):
        element = self.__getElement(locType,locVal)
        element.click()

    # 鼠标事件(双击)
    def mouse_doubleClick(self, locType,locVal):
        element = self.__getElement(locType,locVal)
        ActionChains(self.driver).double_click(element).perform()

    # 文本框清空
    def input_clear(self, locType,locVal):
        element = self.__getElement(locType,locVal)
        element.clear()

    # 允许元素存在（部分数据在某个事件后可能会出现弹出提示，需要点击提示中的确定才可进行以下一步骤操作）
    def allow_element_is_exists(self, type, value):
        try:
            if type == "xpath":
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, value)))
                time.sleep(1)
            elif type == "id":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID, value)))
            elif type == "class_name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif type == "name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, value)))
            elif type == "link_text":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
            WebTools(self.driver).mouse_click('xpath', '//button[@class="BeAlert_confirm"]')
        except:
            pass

    # 验证元素是否存在
    def check_element_is_exists(self, type, value):
        try:
            if type == "xpath":
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.XPATH, value)))
                time.sleep(1)
            elif type == "id":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.ID, value)))
            elif type == "class_name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, value)))
            elif type == "name":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.NAME, value)))
            elif type == "link_text":
                time.sleep(1)
                WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT, value)))
        except NoSuchElementException as e1:
            logger.error("%s:%s查找页面元素不存在" % (type, value))
            self.save_screenshot('查找页面元素不存在')
            raise e1
        except TimeoutException as e2:
            logger.error("%s:%s查找页面元素超时" % (type, value))
            self.save_screenshot('查找页面元素超时')
            raise e2
        except ElementNotVisibleException as e3:
            logger.error("%s:%s查找页面元素不可见" % (type, value))
            self.save_screenshot('查找页面元素不可见')
            raise e3
        except Exception as e:
            logger.error("%s:%s元素查找错误,错误信息：%s" % (type, value, e))
            self.save_screenshot('查找页面元素错误')
            raise e

    # 验证元素是否存在
    def is_element_exist(self, val):
        try:
            self.driver.find_element(By.XPATH,value=val)
            return True
        except NoSuchElementException as e:
            logger.error("查找元素失败,错误信息:%s" %e)
            return False

    # 获取属性值
    def get_attribute(self, locType,locVal, attr):
        element = self.__getElement(locType, locVal)
        value  = element.get_attribute(attr)
        return value

    # 鼠标移动点击
    def mouser_move_action(self, locType,locVal):
        element = self.__getElement(locType,locVal)
        webdriver.ActionChains(self.driver).click(element).perform()

    # 校验按钮是否为选中状态
    def check_button_is_selected(self, locType,locVal):
        element = self.__getElement(locType,locVal)
        value = element.is_selected()
        return value

    # 滚动条拖动到指定元素
    def srollBarToElement(self, val):
        '''
        :param value: 滚动条将要拖动到的元素位置。
        :return:
        '''
        try:
            webElement = self.driver.find_element(By.XPATH,value=val)
            self.driver.execute_script("arguments[0].scrollIntoView(false);", webElement)
        except NoSuchElementException as e:
            logger.error("元素未找到,详细错误详见：%s" %e)

