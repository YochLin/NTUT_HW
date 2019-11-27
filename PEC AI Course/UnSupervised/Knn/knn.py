#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 16:17:46 2019

@author: yochlin
"""
import numpy as np
import operator


class knn:
    '''
    限定處理的資料為
    x  y label
    1  3  yes
    2  4  yes
    3  5  no
    '''
    def __init__(self, k):
        self.k = k
        
    def euclideanDistance(self, train_set, test_point):
        '''
        計算歐式距離，分別將test data內的點與train data的所有點做距離計算
        train_set：train 資料集
        test_point：test 內的單個點
        '''
        distance = []
        test_point = np.array([float(i) for i in test_point[:-1]])
        for tr_x in train_set:
            tr_x_ = np.array([float(i) for i in tr_x[:-1]])
    #        div = list(map(lambda x, y: x - y, test_point, tr_x_))  ## 一種操作 list 運算方法
            d = np.sqrt(sum(pow(test_point - tr_x_, 2)))
            distance.append((tr_x, d))
        return distance
    
    def get_neighbor(self, train_set, test_point, k):
        '''
        找出k的最近點位
        '''
        neighbors = []
        distance = self.euclideanDistance(train_set, test_point)
        distance.sort(key=operator.itemgetter(1))
        for i in range(k):
            neighbors.append(distance[i])
    #    print('=====================')
    #    print(neighbors)
        return neighbors
    
    def get_response(self, neighbors):
        '''
        計算最近點位內最多的類別
        '''
        classVotes = {}
        for i in range(len(neighbors)):
            response = neighbors[i][0][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
                
        storedVote = sorted(classVotes.items(),key=operator.itemgetter(1),reverse=True)
        return storedVote[0][0]
    
    def get_wrong_point(self, train_set, test_set, k):
        '''
        與 test data 真實 label 做比對，並得出錯誤多少點
        '''
        point = []
        for kk in k:
            wrongPoint = 0
            for tt in test_set:
                neighbors = self.get_neighbor(train_set, tt, kk)
                classVote = self.get_response(neighbors)
                if classVote != tt[2]:
                    wrongPoint += 1
            point.append(wrongPoint)
        return point