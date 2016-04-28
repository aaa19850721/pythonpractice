__author__ = 'ym2050'
import numpy as np
import scipy as sp
from numpy.random import random
import pandas as pd
import time
from refine.utils import diskcache, Timer
# 引入numpy中的random函数，即可以不加前缀直接使用

# 类SVD
class SVD:
    # 初始化函数，self指向对象本身，python固有规则，X代表训练集参数，k为特征向量长度
    def __init__(self, X, k):
        '''
        k  is the length of vector
        '''
        # 类似java中this,将对象本身的X变量初始化，np.arry(x),将训练集数据转化为科学计算的数组格式
        self.X = np.array(X)
        # 同上赋值
        self.k = k
        # 求评分平均值，第一维不限制，为所有行，第二维2代表第三列，评分列
        self.ave = np.mean(self.X[:, 2])
        # 输出数据形状
        print("the input data size is ", self.X.shape)
        # bi,bu,qi,pu,物品偏移量，用户偏移量，物品特征矩阵，用户特征矩阵
        self.bi = {}
        self.bu = {}
        self.qi = {}
        self.pu = {}
        self.numRated = {}
        self.userDays = {}
        self.tu = {}
        self.t_u = {}
        self.alpha_u = {}
        self.alpha_pu = {}
        self.movieBins = {}
        self.userBins = {}
        self.movieWeight = {}
        self.sumMW ={}
        self.BINS = 30
        self.MAX_TIME= self.X[:,3].max()
        self.MIN_TIME = self.X[:,3].min()
        self.PER_BIN = (self.MAX_TIME - self.MIN_TIME + 1.0) / self.BINS
        self.BETA = 0.4
        self.LRATE_mb = 0.04
        self.LAMDA_mb = 0.2
        self.LRATE_ub = 0.04
        self.LAMDA_ub = 0.2
        self.LRATE_mf = 0.04
        self.LAMDA_mf = 0.2
        self.LAMDA_uf = 0.2
        self.LRATE_uf = 0.04
        self.LRATE_mw = 0.04
        self.LAMDA_mw = 0.2
        self.LRATE_mbn = 0.04
        self.LAMDA_mbn = 0.2
        self.LRATE_bl = 0.006
        self.LAMDA_bl = 0.065
        # 以字典形式存储的分解矩阵
        self.movie_user = {}
        self.user_movie = {}
        self.Dx = pd.DataFrame(self.X)
        self.Dx.columns ='user_id', 'movie_id', 'rating', 'timestamp'
        self.groupedU = self.Dx[['user_id', 'movie_id', 'rating', 'timestamp']].groupby('user_id')

        # 遍历，即X.shape[0]代表形状第一维，也就是数据表的长度
        # 类似传统for循环的（i<数据长度）
        for i in range(self.X.shape[0]):
            # 分别将user_id,movie_id,rating(以下标读取),赋值给uid mid rat
            uid = self.X[i][0]
            mid = self.X[i][1]
            rat = self.X[i][2]
            time = self.X[i][3]
            # python的字典方法，setdefault(key,value)
            # 如果key 存在，返回对应的value,不存在，插入key,value
            self.movie_user.setdefault(mid, {})
            self.user_movie.setdefault(uid, {})
            self.tu.setdefault(uid, 0)
            self.t_u.setdefault(uid, self.avetime(uid))
            self.movieBins.setdefault(mid,np.linspace(0, 0, 30))
            self.movieWeight.setdefault(mid,random((self.k, 1)) / 10)
            self.sumMW.setdefault(uid,np.zeros((self.k, 1)))
            # self.movieWeight = pd.DataFrame(self.movieWeight)
            # self.sumMW = pd.DataFrame(self.sumMW)
            self.alpha_u.setdefault(uid, 0.001)
            self.numRated.setdefault(uid,0)
            self.userDays.setdefault(uid,0)
            # 字典嵌套，内部形式为{mid:{uid:rat}}，添加新的键值对
            self.movie_user[mid][uid] = rat
            # 字典嵌套，内部形式为{uid:{mid:rat}}，添加新的键值对
            self.user_movie[uid][mid] = rat
            self.numRated[uid] = self.numRated[uid]+1
            self.t_u[uid]=  self.tu[uid]/self.numRated[uid]
            # 对用户偏移值，物品偏移量进行初始化
            self.bi.setdefault(mid,(-0.1 - (-0.5)) * np.random.random() + (-0.5))
            self.bu.setdefault(uid,(0.1 - (-0.01)) * np.random.random() + (-0.01))
            # 对物品特征向量，用户特征向量进行初始化
            self.qi.setdefault(

                # mid ,(0.02 - 0.01) * random((self.k, 1)) + 0.01)
                 mid, random((self.k, 1)) / 10 * (np.sqrt(self.k)))
            self.pu.setdefault(
                # uid,(-0.002 - (-0.01)) * random((self.k, 1)) + (-0.01))
                 uid, random((self.k, 1)) / 10 * (np.sqrt(self.k)))
            self.tmpSum = random((self.k, 0))
        print(pd.Series(self.bi).shape)
        print(pd.Series(self.bu).shape)


    # 添加时间维度的测试
    # def avetime(self,uid):
    #     ug = self.groupedU.get_group(uid)
    #     self.numRated[uid] = ug.shape[0]
    #     self.tu[uid] = ug['timestamp'].sum()
    #     self.t_u[uid] = ug.timestamp.mean()
    #
    #
    # def bin(self,timestamp):
    #     bin = (timestamp-self.MIN_TIME)// self.PER_BIN
    #     # print(timestamp,bin)
    #     if (bin == self.BINS):
    #         bin = bin-1
    #     return int(bin)
    #
    # def dev(self, uid, timestamp):
    #     diff = timestamp - self.t_u[uid]
    #     diff /= 86400*40
    #     if(diff>0):
    #         sign = 1
    #     else:
    #         sign = -1
    #     x = sign * pow(sign * diff, self.BETA)
    #     return x

    # 预测函数，从矩阵中取出预测数据，并加上限制范围1-5
    def pred(self, uid, mid ):
        # 对数据进行检查，不存在则创建键值对并赋0
        self.bi.setdefault(mid, 0)
        self.bu.setdefault(uid, 0)
        # 对数据进行检查，不存在则创建键值对赋值k维全1向量
        self.qi.setdefault(mid, np.zeros((self.k, 1)))
        self.pu.setdefault(uid, np.zeros((self.k, 1)))
        # 对数据进行检查，键存在，值为空，也赋值k维全1向量
        if (self.qi[mid] == None):
            self.qi[mid] = np.zeros((self.k, 1))
        if (self.pu[uid] == None):
            self.pu[uid] = np.zeros((self.k, 1))
        norm = 1.0/np.sqrt(self.numRated[uid])
        ans = self.ave + self.bi[mid] + self.bu[uid] +\
            np.sum(self.qi[mid] * (self.pu[uid]+norm * self.sumMW[uid]))
        if ans > 5:
            return 5
        elif ans < 1:
            return 1
        return ans



    # @diskcache('../tmp/result.cache')
    def outputpre(self):
        bii={}
        buu = {}
        puu ={}
        qii = {}
        ave = {}
        tmpave = {}
        sumMWW = {}
        print(len(self.numRated))
        print(len(self.bu))
        for i in self.numRated .keys():
           bii.setdefault(i,self.bi)
           norm = 1.0/np.sqrt(self.numRated[i])
           tmp = {}
           suW = {}
           tmpave.setdefault(i,self.ave)
           for j in range(self.k):
               suW.setdefault(j,self.sumMW[i][j][0]*norm)
               tmp.setdefault(j,self.pu[i][j][0])
           puu.setdefault(i,tmp )
           sumMWW.setdefault(i,suW)
        for i in self.bi.keys():
           buu.setdefault(i,self.bu)
           ave.setdefault(i,tmpave )
           tmp = {}
           for j in range(self.k):
                tmp.setdefault(j,self.qi[i][j][0])
           qii.setdefault(i,tmp)

        suR = pd.DataFrame (sumMWW)
        biia = pd.DataFrame(bii)
        buua = pd.DataFrame(buu).T
        puua = pd.DataFrame(puu)
        puua = puua + suR
        qiia = pd.DataFrame(qii).T
        ave = pd.DataFrame (ave)
        x = biia+buua
        y = np.dot(qiia,puua)
        z = pd.DataFrame(x+y).T
        z = z+ave
        print(z.shape)
        return  z


    def precalcMWSum(self,uid):
     ug = self.groupedU.get_group(uid)
     for a in range(ug.shape[0]):
         self.sumMW[uid] = np.zeros((self.k, 1))
         tmp = ug.iloc[a]
         mid = tmp['movie_id']
         self.sumMW[uid] += self.movieWeight[mid]


    def calcMWSum(self,uid,decay):
     ug = self.groupedU.get_group(uid)
     for a in range(ug.shape[0]):
        tmp = ug.iloc[a]
        mid = tmp['movie_id']
        tmpMW = self.movieWeight[mid]
        self.movieWeight[mid] += (decay * self.LRATE_mw * (self.tmpSum[mid]- self.LAMDA_mw * tmpMW))
        self.sumMW[uid] += self.movieWeight[mid] - tmpMW

    # 训练函数
    def run(self,steps,decay=0.93):
        for step in range(steps):
            print('the ', step, '-th  step is running')
            decay *= 0.9+0.1*np.random.random()
            rmse_sum = 0.0
            xp = 0.0
            for uid,group in self.groupedU:
                self.precalcMWSum(uid)
                self.tmpSum = {}
                for x in range(group.shape[0]):
                    tmp = group.iloc[x]
                    self.tmpSum .setdefault(mid,np.zeros((self.k, 1)))
                    mid = tmp[1]
                    # time = tmp[3]
                    uid = tmp[0]
                    rat = tmp[2]
                    eui = rat - self.pred(uid, mid)
                    xp += eui
                    rmse_sum += eui ** 2
                    # tmpbin = self.bin(time)
                    # self.movieBins[mid][tmpbin] += decay*self.LRATE_mbn* (eui - self.LAMDA_mbn *self.movieBins[mid][tmpbin])
                    # self.alpha_u[uid] += (self.LRATE_bl*(self.dev(uid, time) * eui - self.LAMDA_bl * self.alpha_u[uid]))
                    self.bu[uid] += decay * self.LRATE_ub * (eui - self.LAMDA_ub*self.bu[uid])
                    self.bi[mid] += decay * self.LRATE_mb * (eui - self.LAMDA_mb*self.bi[mid])
                    temp = self.qi[mid]
                    self.qi[mid] += decay*self.LRATE_uf * (eui * self.pu[uid] - self.LAMDA_uf * self.qi[mid])
                    self.pu[uid] += decay*self.LRATE_mf * (eui * temp - self.LAMDA_mf * self.pu[uid])
                    self.tmpSum[mid] += (eui * (1.0 /np.sqrt(self.numRated[uid])))*temp
                    self.calcMWSum(uid,decay)
            print("the rmse of this step on train data is ", np.sqrt(rmse_sum / self.X.shape[0]),xp)

    # 迭代运算 steps迭代次数，gamma，Lambda 计算参数，以均方误差评分


    def test(self, test_X):
        output = []
        sums = 0
        ee = 0
        test_X = np.array(test_X)
        # print "the test data size is ",test_X.shape
        for i in range(test_X.shape[0]):
            pre = self.pred(test_X[i][0], test_X[i][1])
            output.append(pre)
            # print pre,test_X[i][2]
            ee += pre - test_X[i][2]
            sums += (pre - test_X[i][2]) ** 2
        rmse = np.sqrt(sums / test_X.shape[0])
        print("the rmse on test data is ", rmse,ee)
        return output

