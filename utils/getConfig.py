import os
import yaml
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

def collect_static_data(param):
    logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>测试用例执行start<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    logger.debug("<--------读取初始化配置数据start-------->")
    logger.debug("配置文件参数为：%s" % param)
    rootdir = os.path.dirname(os.path.dirname(__file__))
    configFile = param+'.yml'
    confFilePath = os.path.join(rootdir,'conf',configFile).replace('\\','/')
    logger.debug("配置文件路径是：%s" % confFilePath)

    #打开文件,通过pyyaml读取内容
    with open(confFilePath,mode='r',encoding='utf-8') as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
    return data

if __name__ == '__main__':
    pass
    # collect_static_data('bttest')

aa = collect_static_data('test')
print(aa)

