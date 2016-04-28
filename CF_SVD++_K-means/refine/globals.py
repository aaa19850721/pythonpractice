__author__ = 'ym2050'
'''
全局变量及函数
'''
# 引入科学计算工具包pandas 别名pd
import pandas as pd
# 引入科学计算工具numpy 别名np(灰色的包代表在此文件中没有使用该包)
import numpy as np
# 引入工具类utils中的定时器类和缓存方法
from refine.utils import diskcache, Timer


# 文件目录，10M数据集中没有users.dat,1M中有
USER_FILE = '/home/xueyun/ml-1m/users.dat'
RATING_FILE = '/home/xueyun/ml-10M100K/ratings.dat'
MOVIE_FILE = '/home/xueyun/ml-10M100K/movies.dat'

# 工具类的缓存方法，写在数据量比较大，却很少更改的函数前，可以缓存函数返回结果，下一次调用该函数则读取缓存，不再执行函数
# 数据频繁更改或者方法需要多次测试时请注释
# 单次需要重新运行，请删除tmp里的缓存文件
@diskcache('../tmp/user.cache')
def get_user():
    # 调用Timer类，则会输出函数开始，结束，消耗时间的提示
    with Timer(msg="LOAD USER"):
        # 创建列名列表unames,包含以下四个元素
        unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
        # 使用pandas的方法读取文件，文本分隔符为‘::’,文件本身没有表头，列名使用unames中的元素
        # 读取结果为数据框 dataframe,可将其想象为二维表
        return  pd.read_table(USER_FILE, sep='::', header=None, names=unames)


@diskcache('../tmp/rating.cache')
def get_rating():
    with Timer(msg="LOAD RATING"):
        rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
        return pd.read_table(RATING_FILE, sep='::', header=None, names=rnames)

@diskcache('../tmp/movie.cache')
def get_movie():
    with Timer(msg="LOAD MOVIE"):
        mnames = ['movie_id', 'title', 'genres']
        return pd.read_csv(MOVIE_FILE, sep='::', header=None, names=mnames)

# 在该模块自己运行的时候，该__name__就等于'main'，而如果被其他的模块import，则该模块的__name__就等于模块名
# 即直接执行本文件的时候，这里就是main，如果别的模块调用该文件，则下面的内容被忽略不计，主要用来进行模块自测试，
# 如下，对三个文件读取函数进行测试，打印输出前五行
# dataframe  A[0:3,0:2] 将输出 0 1 2 行 0 1 列的内容，不包含后边界，可以只使用一维参数 如下
if __name__ == '__main__':
    print(get_user()[:5])
    print(get_rating()[:5])
    print(get_movie()[:5])