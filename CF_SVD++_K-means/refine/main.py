__author__ = 'wl'

#################################################
# kmeans: k-means cluster
# Author : zouxy
# Date   : 2013-12-25
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################


from refine.recommendations import *
import pandas as pd
import numpy as np
import time

def getData(file):
     r = np.loadtxt(file, delimiter=",")
     print(r)
     mids = r[0][1:]
     uids = [r[i][0] for i in range(1, len(r))]
     M = r[1:, 1:]
     return M, uids, mids


# # print("step 1: load data...")
# uid = []
# mid = []
# test = pd.read_csv("../data/test1.csv")
# test = np.array(test)
# print(test)
# print("---------------------------------------")
#
# mid = [i for i in test]
# uid = [i for i in test[mid[0]]]    #get the uid from the first colomn of mid
# mid = mid[1:]  #delete the first colomn
# # print(test[mid[0]][0])
# M = []
# # for i in range(len(uid)):
# for i in mid:
#      M.append(test[i])
# # M.append([test[j][i] for j in mid])
# # M = [[test[mid[i]][j] for j in range(len(uid))] for i in range(len(mid))]
# print("************")
# M = mat(M).T
# print(M)
# print("&&&&&&&&&")
# print(M[0][len(M[0])-1])

# M = [test[i][1] for i in mid]
# M = [i for i in M]
# print("M1:")
# print(M)
# M = mat(M).T
#
# print("M2:")
# print("M: {}".format(M))

if __name__ == "__main__":
     M, uids_train, mids_train = getData("../data/result1.csv")
     user, uids_test, mids_test = getData("../data/test1.csv")
     # print(M.shape)
     uids_train = [int(i) for i in uids_train]
     uids_test = [int(i) for i in uids_test]
     mids_test = [int(i) for i in mids_test]

     starttime = time.clock()

     #recommendation(M, features(cluster dimensions), clusters number, topN)
     user_train = len(M)
     user_test = 1
     recommend = Recommendation(M[:user_train], 20, 25, 28, uids_train, uids_test, mids_test)
     recommend.test(user[:user_test])

     interval = time.clock() - starttime
     print("Finished in {:.3f} secs.".format(interval))

M = [[3,2,5,5,1,4,3],
     [5,1,5,4,2,3,5],
     [5,5,2,3,5,5,1],
     [1,4,4,3,2,5,3],
     [4,4,1,2,4,4,2],
     [4,5,1,5,3,3,4]]

user = [[2,2,4,0,1,5,3],
        [5,5,0,0,5,5,0],
        [4,3,0,5,0,2,0]]


