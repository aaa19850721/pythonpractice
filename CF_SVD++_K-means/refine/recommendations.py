__author__ = 'wl'

#################################################
# kmeans: k-means cluster
# Author : zouxy
# Date   : 2013-12-25
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################


from refine.Kmeans import *
from refine.utils import *
import numpy as np
from operator import itemgetter, attrgetter
import time
import matplotlib.pyplot as plt

class Recommendation:
     #feature number, cluster number, top-N of user neighborhoods
     def __init__(self, M, features=4, kclusters=3, topN=2, uidstrain=[], uidstest=[], midstest=[]):
          self.M = M
          self.f = features
          self.k = kclusters
          self.n = topN

          self.uids_train = uidstrain
          self.uids_test = uidstest
          self.mids_test = midstest

          U, s, self.V = np.linalg.svd(M, full_matrices=False)
          # print("U:{},s:{},V:{}".format(U.shape, s.shape, self.V.shape))
          # S = np.diag(s)
          # print(np.dot(U, np.dot(S, self.V)))
          # print(s)

          print("step 3: conceptual mapping")
          #M*V user feature
          userF = np.dot(self.M, self.V[:self.f, :].T)

          ## step 2: clustering...
          print("step 4: kmeans clustering...")
          dataSet = mat(userF)
          self.centroids, self.clusterAssment, self.clusters = kmeans(dataSet, self.k)

          clusters_file = [[self.uids_train[i] for i in self.clusters[j]] for j in range(len(self.clusters))]
          writeMatrix('clusters.txt', clusters_file)
          writeMatrix('centroids.txt', self.centroids)

     #predict the rate of user uid on movie mid
     def pred(self, uid, mid):
          user_f = np.dot(mat(self.user[uid]), self.V[:self.f, :].T)
          cosDistances = [cosineDistance(user_f.A[0], self.centroids[i]) for i in range(len(self.centroids))]
          print(cosDistances)
          cluster = cosDistances.index(max(cosDistances))
          print(cluster)
          mean = getMean(self.user[uid])
          numerator = sum([pearsonCorr(self.M[i], self.user[uid])*(self.M[i][mid]-getMean(self.M[i])) for i in self.clusters[cluster]])
          denominator = sum([abs(pearsonCorr(self.M[i], self.user[uid])) for i in self.clusters[cluster]])

          if denominator == 0:
               rate = mean    #user rates all movies the same, so use mean to predict
          else:
               rate = mean+numerator/denominator
               if rate > 5:
                    rate = 5
               elif rate < 1:
                    rate = 1
          return rate

     #predict the rate of user uid on all movies
     def predict(self, uid):
          user_f = np.dot(mat(self.user[uid]), self.V[:self.f, :].T)
          cosDistances = [cosineDistance(user_f.A[0], self.centroids[i]) for i in range(len(self.centroids))]
          print(cosDistances)
          cluster = cosDistances.index(max(cosDistances))
          print(cluster)
          mean = getMean(self.user[uid])

          topN = []
          topN = [[i, pearsonCorr(self.M[i], self.user[uid])] for i in self.clusters[cluster]]
          # print("uid: {}, top: {}".format(uid, topN))
          topN.sort(key=lambda x:x[1], reverse=True)
          # print("uid: {}, top: {}".format(uid, topN))
          if len(topN) > self.n:
               topN = topN[:self.n]

          #todo: topN?
          # print("uid: {}, topN: {}".format(uid, topN))
          # topN = [topN[i][0] for i in range(len(topN))]
          print("uid: {}, top: {}".format(uid, topN))

          prediction = []
          for mid in range(len(self.M[0])):
               numerator = sum([topN[i][1]*(self.M[topN[i][0]][mid]-getMean(self.M[topN[i][0]])) for i in range(len(topN))])
               denominator = sum([abs(topN[i][1]) for i in range(len(topN))])

               # numerator = sum([pearsonCorr(self.M[i], self.user[uid])*(self.M[i][mid]-getMean(self.M[i])) for i in topN])
               # denominator = sum([abs(pearsonCorr(self.M[i], self.user[uid])) for i in topN])
               if denominator == 0:
                    prediction.append(mean)    #user rates all movies the same, so use mean to predict
               else:
                    rate = mean+numerator/denominator
                    if rate > 5:
                         rate = 5
                    elif rate < 1:
                         rate = 1
                    prediction.append(rate)
          # print(user[uid])
          # print(prediction)
          return prediction


     def test(self, user):
          self.user = user
          sumofsqare = 0
          number = 0
          for uid in range(len(self.user)):
               prediction = self.predict(uid)
               # prediction = [self.pred(uid,mid) for mid in range(len(user[uid]))]
               predictionlist = [[i, prediction[i]] for i in range(len(prediction))]
               recommendlist = self.getTopN(predictionlist, 10)
               recommendlist = [{self.mids_test[recommendlist[i][0]]:recommendlist[i][1]} for i in range(len(recommendlist))]
               predictionlist = [{self.mids_test[predictionlist[i][0]]:predictionlist[i][1]} for i in range(len(predictionlist))]
               print("prediction: {}".format(prediction))
               writeRates('predict.txt', self.uids_test[uid], predictionlist)
               writeRates('top10.txt', self.uids_test[uid], recommendlist)
               for mid in range(len(self.user[uid])):
                    if(self.user[uid][mid] != 0):
                         sumofsqare += (prediction[mid]-self.user[uid][mid])**2
                         number += 1
          print("RMSE: {}".format(sqrt(sumofsqare/number)))

     def getTopN(self, arr, n):
          arr.sort(key=lambda x:x[1], reverse=True)
          # print("uid: {}, top: {}".format(uid, topN))
          if len(arr) > n:
               arr = arr[:n]
          return arr
## step 1: load data
print("step 1: load data...")
M = [[3,2,5,5,1,4,3],
     [5,1,5,4,2,3,5],
     [5,5,2,3,5,5,1],
     [1,4,4,3,2,5,3],
     [4,4,1,2,4,4,2],
     [4,5,1,5,3,3,4]]

user = [[2,2,4,0,1,5,3],
        [5,5,0,0,5,5,0],
        [4,3,0,5,0,2,0]]
if __name__ == '__main__':
     recommend = Recommendation(M)
     recommend.test(user)

