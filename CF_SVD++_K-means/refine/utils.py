from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
# 下一个新版本的特性导入到当前版本，可以在当前版本中使用一些新版本的特性，必须放在文档开头
'''
工具类与工具方法
'''
# from builtins import *
# 引入内建模块，该模块中有一些常用函数;而该模块在Python启动后、且没有执行程序员所写的任何代码前，
# Python会首先加载该内建函数到内存，如str()，min(),max()等常用函数,不是必要
import time
from os.path import isfile
from sklearn.externals import joblib
# Joblib  包括为Python函数提供轻量级管道任务(pipeline job)服务的一系列工具，
# 包括透明磁盘IO缓冲、快速序列化、简单并行化运行、日志服务


# 创建定时器Timer类，对调用该类的操作进行时间统计，并输出结果
class Timer:
    # def a(): 定义函数a
    # _init_初始化 类似于构造函数
    def __init__(self, progress=100000,msg=''):
        self.starttime = None
        self.progress = progress
        self.i = 0
        self.msg = msg
    # __enter__ 方法将在进入代码块前被调用
    def __enter__(self):
        return self.start()
    # __exit__ 方法则在离开代码块之后被调用(即使在代码块中遇到了异常)
    def __exit__(self, *args):
        self.stop()
    # 开始计时，输出开始提示信息
    def start(self):
        self.starttime = time.clock()
        #format(self.msg) 格式化输出，将参数self.msg在大括号所在位置输出，
        print("{}: Started.".format(self.msg))
        return self
    # 结束计时，输出结束提示信息
    def stop(self):
        interval = time.clock() - self.starttime
        print("{}: Finished in {:.3f} secs.".format(self.msg,interval))
    #增量函数
    def increment(self):
        self.i += 1
        if self.i % self.progress == 0:
            interval = time.clock() - self.starttime
            print("{}: {} step has been made in {:.3f} secs.".format(self.msg,self.i, interval))



def diskcache(fname, recache=False):
    '''
    缓存方法，不必仔细研究，功能描述如下
    若fname文件存在，则加载后返回。若不存在，执行函数后，将结果写入缓存文件。
    适合于执行特定流程并返回结果的函数。
    :param fname:缓存文件名
    :param recache:是否重新生成缓存
    '''

    def wrapper(F):

        def docache(*args, **kwargs):
            if isfile(fname) and not recache:
                # 使用jolibd.load读取缓存文件并返回
                return joblib.load(fname)
            else:
                # 使用jolibd.dump 创建缓存文件，返回函数的返回值
                result = F(*args, **kwargs)
                joblib.dump(result, fname)
                return result

        return docache

    return wrapper


# 对上面的类和方法进行测试，不必注意
def __timertest():
    with Timer(100,msg="COUNTING") as t:
        for i in range(10000):
            t.increment()


def __diskcachetest():
    import numpy as np
    @diskcache('../tmp/computetest.cache')
    def compute():
        print("Compute Run")
        return np.arange(100000)

    result1 = compute()
    result2 = compute()

    print(np.array_equal(result1,result2))

def writeToFile(file, content):
    with open(file, 'wt+') as fd:
        fd.write(content)
        fd.close()

def writeMatrix(file, M):
    content = ''
    for i in range(len(M)):
        content = content + '{}: '.format(i+1) + str(M[i]) + '\n'
    writeToFile(file, content)

def writeRates(file, uid, rate):
    content = '{}: '.format(uid) + str(rate) + '\n'
    writeToFile(file, content)

if __name__ == '__main__':
    # __timertest()
    # __diskcachetest()
    # data = ['1', '2', '3']
    data = [[1, 2, 3, 4, 7],[2, 4, 5, 6]]
    rate = [2, 4, 5, 6]

    # writeMatrix('e.txt', data)
    writeRates('rate.txt', 1009, rate)
