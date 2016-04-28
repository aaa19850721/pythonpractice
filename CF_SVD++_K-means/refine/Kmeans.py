__author__ = 'wl'

#################################################
# kmeans: k-means cluster
# Author : zouxy
# Date   : 2013-12-25
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################

from numpy import *
import time
import matplotlib.pyplot as plt
from math import *
from refine.utils import *


# calculate Euclidean distance
def euclDistance(vector1, vector2):
    return sqrt(sum([(vector1[i]-vector2[i])**2 for i in range(len(vector1))]))

def cosineDistance(vector1, vector2):

    numerator = sum([vector1[i]*vector2[i] for i in range(len(vector1))])
    denominator = sqrt(sum([vector1[i]**2 for i in range(len(vector1))])) * \
                  sqrt(sum([vector2[i]**2 for i in range(len(vector2))]))
    return numerator / denominator

def getMean(vector):
    rates = [rate for rate in vector if rate != 0]
    mean = sum(rates) / len(rates)
    return mean

def pearsonCorr(vector1, vector2):
    si={}
    for i in range(len(vector1)):
        if vector1[i]*vector2[i] != 0:
            si[i]=1
    n=len(si)
    if (n==0):
        return 1
    # s1=array([vector1[i] for i in si])
    # s2=array([vector2[i] for i in si])

    # print(si)
    # print(s2)

    mean1 = getMean(vector1)
    mean2 = getMean(vector2)

    # print(rate2)

    numerator = sum([(vector1[i]-mean1)*(vector2[i]-mean2) for i in si])
    denominator = sqrt(sum([(vector1[i]-mean1)**2 for i in si])) * \
                  sqrt(sum([(vector2[i]-mean2)**2 for i in si]))
    if denominator == 0:
        return 0   #if the rate of user on every movie is the same, then denominator will be 0
    return numerator / denominator

# init centroids with random samples
def initCentroids(dataSet, k):
    centers = []
    numSamples, dim = dataSet.shape
    centroids = zeros((k, dim))
    i = 0
    while i < k:
        index = int(random.uniform(0, numSamples))
        if index in centers:
            print('contains!!!')
            continue
        else:
            centers.append(index)
        centroids[i, :] = dataSet[index, :]
        # print(centroids[i, :])
        i += 1
    return centroids


cosine = 1
# k-means cluster
def kmeans(dataSet, k):
    numSamples = dataSet.shape[0]
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    clusterAssment = mat(zeros((numSamples, 2)))
    clusters = [] #index of elements in every cluster
    clusterChanged = True

    ## step 1: init centroids
    centroids = initCentroids(dataSet, k)
    steps = 0
    while clusterChanged:
        steps += 1
        print("steps {}".format(steps))
        clusterChanged = False
        ## for each sample
        for i in range(numSamples):
            minDist  = 100000.0
            maxDist  = -10000.0 #consine distance
            minIndex = 0
            ## for each centroid
            ## step 2: find the centroid who is closest
            for j in range(k):
                if cosine == 0:
                    distance = euclDistance(centroids[j, :], dataSet.A[i, :])
                    if distance < minDist:
                        minDist  = distance
                        minIndex = j
                else:
                    distance = cosineDistance(centroids[j, :], dataSet.A[i, :])
                    if distance > maxDist:
                        maxDist  = distance
                        minIndex = j


        ## step 3: update its cluster
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
                if cosine == 0:
                    clusterAssment[i, :] = minIndex, minDist**2
                else:
                    clusterAssment[i, :] = minIndex, maxDist

        ## step 4: update centroids
        for j in range(k):
            pointsInCluster = dataSet[nonzero(clusterAssment[:, 0].A == j)[0]]
            centroids[j, :] = mean(pointsInCluster, axis = 0)
            # print(centroids[j, :])

    for j in range(k):
        clusters.append(nonzero(clusterAssment[:, 0].A == j)[0])
        print(centroids[j, :])
        # print("cluster{}:{}".format(j, nonzero(clusterAssment[:, 0].A == j)[0]))
    print('Congratulations, cluster complete!')
    return centroids, clusterAssment, clusters

# show your cluster only available with 2-D data
def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    mark = ['or', 'ob', 'og', 'ok', 'oy', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Your k is too large! please contact Zouxy")
        return 1

    # draw all samples
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', 'Dy', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize = 12)

    plt.show()