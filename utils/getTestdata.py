import os
import yaml
from Common.LogFunc import loggerConf

logger = loggerConf().getLogger()

def getTestdataPath(testcase_path):
    '''
    根据 测试用例路径 匹配到 对应测试数据路径
    :param testcase_path:  测试用例绝对路径，由对应测试用例里传过来
    :return:
    '''
    temp_path  = testcase_path.split('Testcase/')
    testdata_path = os.path.join(temp_path[0],'Testdata',temp_path[1]).replace('\\','/').replace('.py','.yml')
    logger.debug("测试数据路径是%s" % testdata_path)
    return testdata_path


# def getTestcaseData(testdata_path,cmdopt):
#     '''
#     :param testdata_path: 测试用例对应测试数据文件路径 由getTestdataPath()返回
#     :return:
#     '''
#     with open(testdata_path,mode='r',encoding='utf-8') as f:
#         data = yaml.load(f,Loader=yaml.FullLoader)
#         print("=====data值为=====",data)
#         splc_value = data.get('splc')
#         if cmdopt in splc_value:
#             for k,v in splc_value.items():
#                 if cmdopt == k:
#                     print("ok",k)
#                     data['splc']={cmdopt,k}
#                     print("更新后data为：",data)
#                     return data
#         else:
#            return None

def getTestcaseData(testdata_path):
    '''
    :param testdata_path: 测试用例对应测试数据文件路径 由getTestdataPath()返回
    :return:
    '''
    try:
        with open(testdata_path,mode='r',encoding='utf-8') as f:
            data = yaml.load(f,Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        logger.error("测试初始化数据yml文件缺失。")
        raise
    except Exception as e:
        logger.error("处理初始化数据yml异常，异常信息为：%s" % e)
        raise

if __name__ == '__main__':
    pass
