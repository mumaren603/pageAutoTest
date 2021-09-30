import pytest
from utils.getConfig import collect_static_data

# hook
# 注册自定义参数 env 到配置对象
def pytest_addoption(parser):
    '''parser:用户命令行参数与ini文件值的解析器'''
    parser.addoption("--env",       #注册一个命令行选项
                     default='bttest',
                     dest='env',
                     help="将自定义命令行参数 ’--cmdopt' 添加到 pytest 配置中"
                     )

# 获取命令行env参数值
@pytest.fixture(scope='session')
def cmdopt(request):
    print("命令行参数是：%s" %request.config.getoption('--env'))
    return request.config.getoption('--env')

# 参数传递给collect_static_data 获取对应配置文件值
@pytest.fixture(scope='module',autouse=True)
def getConfValue(request,cmdopt):
    '''装饰器：根据环境配置文件获取配置文件yaml值'''
    request.config.base_data = collect_static_data(cmdopt)
    return request.config.base_data



