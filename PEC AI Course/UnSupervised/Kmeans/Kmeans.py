import random
import math
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt




def point_distance(dataSet, k):
    '''
    透過歐式距離求出每個點與隨機點的距離
    '''
    distance = []
    for p in dataSet:
        x = pow(p[0] - k[0], 2)
        y = pow(p[1] - k[1], 2)
        d = math.sqrt(x + y)
        distance.append(d)
    return distance

def list_duplicates(seq):
    '''
    找出 list 中相同的類別及其索引值
    '''
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)

        

def classifiy(distance):
    '''
    將得到的距離找出最小值，並代表屬於哪個類別
    '''
    distance = np.array(distance)
    class_ = np.argmin(distance, axis=0)
    class_index = [index for i, index in list_duplicates(class_)]
    return class_index



if __name__ == '__main__':
    # # read file
    # file = open("AI-Practice02-Data.txt", "r", encoding = "utf-8")

    # # 0 = not stressed, 1 = stressed
    # data = [(each.replace("\n", "").split("\t")) for each in file]
    # data = [(float(each[0]), float(each[1]), 0) if data.index(each) < 200 else (float(each[0]), float(each[1]), 1) for each in data]

    k = 2
    n_stress = pd.read_csv('NotStress.csv')
    stress = pd.read_csv('Stress.csv')
    all_stress = pd.concat([n_stress, stress], ignore_index=True).values

    # 生成圖布
    plt.figure(dpi=150)

    # 打開交互模式
    plt.ion()

    '''
    先隨機在資料集上找 k 個點
    '''
    all_index = np.arange(len(all_stress))
    random_index = np.random.choice(all_index, k)
    k_points = []
    for i in random_index:
        data = all_stress[i]
        k_points.append(data)

    '''
    將隨機找的中心點透過資料集的計算來得出所有資料路徑最短的中心點
    '''
    error = 1
    while(error != 0):
        plt.plot(n_stress[n_stress.columns[0]], n_stress[n_stress.columns[1]], 'co')
        plt.plot(stress[stress.columns[0]], stress[stress.columns[1]], 'yo')
        distance = []
        old_k_points = np.array(k_points)
        for k in k_points:
            distance.append(point_distance(all_stress, k))     ### 有 k 個的距離（因為有k點，所以會計算出k個全資料集每點的距離）
            plt.plot(k[0], k[1], '*', markersize=15)
        k_points = []                                          ### 再次重新定義空的 list 存放之後計算出的 k 點
        for index in classifiy(distance):
            points = list(map(lambda x: all_stress[x], index))   ### 將索引值丟入資料集，會得出資料集的點
            k_points.append(sum(points) / len(points))           ### 將得出的資料集點，取平均重新得到中心點
        k_points = np.array(k_points)
        if (k_points - old_k_points).all() == 0:                 ### 判斷兩個陣列相減是否為 0 (新的中心點與舊的中心點做相減即可知道點為是否有變動)
            error = 0
        print(k_points)

        # 暫停
        plt.pause(0.1)
    # 關閉交互模式
    plt.ioff()
    plt.show()

    
    
    