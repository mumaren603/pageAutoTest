import pytest,sys
from selenium import webdriver
from Common.ToolsForOpertion import WebTools
from pageObject.logout import logout
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.fixture(scope="session")
def login(request,getConfValue):
    logger.debug("yaml中读取配置内容：%s" % getConfValue)

    driver_path = getConfValue.get('envinfo').get('browserDriver', None)
    logger.debug("浏览器驱动路径：%s" % driver_path)

    login_url = getConfValue.get('envinfo').get('url', None)
    logger.debug("url路径：%s" % login_url)

    login_info = getConfValue.get('envinfo').get('loginInfo', None)
    logger.debug("登录用户信息：%s" % login_info)
    logger.debug("<--------读取初始化配置数据end-------->")

    if driver_path and login_url and login_info:
        driver = webdriver.Chrome(executable_path=driver_path)
        WebTools(driver).set_browser(login_url)
        #登录
        WebTools(driver).check_element_is_exists('xpath', "//div[contains(@id,'_btnlogin')]")
        WebTools(driver).input_clear('xpath', "//input[contains(@id,'_name')]")
        WebTools(driver).input_clear('xpath', "//input[contains(@id,'_password')]")
        WebTools(driver).input_content('xpath', "//input[contains(@id,'_name')]", login_info.get('user'))
        WebTools(driver).input_content('xpath', "//input[contains(@id,'_password')]", login_info.get('passwd'))
        WebTools(driver).mouse_click('xpath', "//div[contains(@id,'_btnlogin')]")
        WebTools(driver).check_element_is_exists('xpath',"//div[contains(text(),'办件中心')]")
        yield driver
        # 登出系统、退出浏览器
        logout(driver).logout()
        driver.quit()
    else:
        logger.error("全局登录信息缺失，请检查yaml配置文件。")
        sys.exit(-1)


