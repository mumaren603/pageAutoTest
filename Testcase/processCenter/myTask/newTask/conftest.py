import pytest
from Common.ToolsForOpertion import WebTools
from pageObject.taskCenter import taskCenter
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

@pytest.fixture(scope="function")
def openProcessCenter(login):
    '''
    :param login: 装饰器 调取登录方法（login(fixture)-->conftest）
    :return: driver对象
    :action: 模块下每个用例执行前需打开办件中心模块，执行后关闭办件中心
    '''
    driver = login

    logger.debug("打开办件中心模块")
    taskCenter(driver).workCenter()
    yield driver
    WebTools(driver).is_element_exist("//i[@class='icon-close-round cFNvY7v']")
    WebTools(driver).mouse_click('xpath',"//i[@class='icon-close-round cFNvY7v']")
    logger.debug("关闭办件中心模块")