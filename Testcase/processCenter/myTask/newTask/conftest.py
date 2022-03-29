import pytest
from Common.ToolsForOpertion import WebTools
from pageObject.taskCenter import taskCenter

@pytest.fixture(scope="function")
def openProcessCenter(login):
    '''
    :param login: 装饰器 调取登录方法（login(fixture)-->conftest）
    :return: driver对象和数据库配置信息
    :action: 模块下每个用例执行前需打开办件中心模块，执行后关闭办件中心
    '''
    print("打开办件中心模块")
    driver = login
    # 打开查询中心
    taskCenter(driver).workCenter()
    yield login
    # 关闭办件中心
    WebTools(driver).is_element_exist("//i[@class='icon-close-round cFNvY7v']")
    WebTools(driver).mouse_click('xpath',"//i[@class='icon-close-round cFNvY7v']")
