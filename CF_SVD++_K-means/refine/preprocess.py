__author__ = 'xueyun'
from refine .globals import  *
import pandas as pd
import numpy as np
from refine.utils import diskcache, Timer
from refine .SVD import *
import time
#preprocess.py
tmp ={}
@diskcache('../tmp/Data.cache')
def get_data():
    # 获取评分数据
    df_rating = get_rating()
    # 随机排列10681名电影编号
    sampler = np.random.permutation(10681)
    # 抽取随机排序后的前1300个编号
    sampler = sampler[:1000]
    tmp = sampler
    # # np.in1d(a,b) 返回bool  a are in b 即得到这10000名用户的评分数据
    df_rating = df_rating[np.in1d(df_rating .movie_id, sampler)]
    print(df_rating.shape)
    # # 取得评分数据索引
    sampler = np.random.permutation(71567)
    a = sampler[:12000]
    b = sampler[12000:14000]
    df_ratingSVD = df_rating[np.in1d(df_rating .user_id, a)]
    df_knntest = df_rating[np.in1d(df_rating .user_id, b)]
    print("RatingData{}", format(df_ratingSVD .shape))
    print(df_ratingSVD.movie_id.unique().size)
    print(df_ratingSVD.user_id.unique().size)
    print(df_knntest.shape)
    x = df_rating .index
    # 对索引进行随机排列，得到随机序列
    sampler1 = np.random.permutation(x)
    # 按照随机后的索引结果，对数据进行重排序
    df_ratingSVD = df_rating.reindex(sampler1)
    # 打印数据框形状
    print("RatingData{}", format(df_ratingSVD .shape))
    # 保存SVD++使用的数据与给聚类算法准备的新用户测试集
    # df_ratingSVD[['user_id', 'movie_id','rating','timestamp']].to_csv('../rating.csv', index=False)
    # df_knntest[['user_id', 'movie_id','rating','timestamp']].to_csv('../knntest.csv', index=False)
    return df_ratingSVD
def output():
    return tmp

# 以1100001条数据为划分，之前的划分为训练集，之后的划分为测试集
# @diskcache('../tmp/train.cache')
def get_train():
    return get_data()[['user_id','movie_id','rating','timestamp']][:1800000]

# @diskcache('../tmp/test.cache')
def get_test():
     a = get_data()[['user_id','movie_id','rating','timestamp']][180000:]
     return a

if __name__ == '__main__':
    with Timer(msg="SVD"):
        df_train = get_train()
        df_test = get_test()
        print("Train: {}".format(df_train.shape))
        print("Test: {}".format(df_test.shape))
        a = SVD(df_train,30)
        a.run(20)
        # 输出结果矩阵
        pd.DataFrame(a.outputpre()).to_csv('../result.csv')
