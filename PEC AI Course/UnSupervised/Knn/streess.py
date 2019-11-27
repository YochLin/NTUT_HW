import numpy as np
import random
import pandas as pd
from knn import knn
import matplotlib.pyplot as plt

def add_label(train_li, n_train_li):
    y_label = np.array(['stress'] * len(train_li))[:, np.newaxis]
    n_label = np.array(['n_stress'] * len(n_train_li))[:, np.newaxis]
    n_train_li = np.hstack((n_train_li, n_label))
    train_li = np.hstack((train_li, y_label))
    train_set = np.vstack((train_li, n_train_li))
    return train_set


def part1(file_1, file_2):
    columns1 = file_1.columns
    columns2 = file_2.columns
    w1 = file_1[columns1[0]]
    h1 = file_1[columns1[1]]
    w2 = file_2[columns2[0]]
    h2 = file_2[columns2[1]]
    plt.plot(w1, h1, 'o')
    plt.plot(w2, h2, 'o')
    plt.xlabel('w')
    plt.ylabel('h')
    plt.legend(['no_stress', 'stress'])
    plt.title('Total data')


def part2(n_file, file):
    n_file = n_file.values
    file = file.values
    random.shuffle(n_file)
    random.shuffle(file)
    n_train = n_file[:int(len(n_file) / 2)]
    n_test = n_file[int(len(n_file) / 2):]
    train = file[:int(len(file) / 2)]
    test = file[int(len(file) / 2):]
    plt.figure()
    plt.plot(n_train[:,0], n_train[:,1], 'o')
    plt.plot(train[:,0], train[:,1], 'o')
    plt.xlabel('w')
    plt.ylabel('h')
    plt.legend(['no_stress', 'stress'])
    plt.title('Train Data')
    plt.figure()
    plt.plot(n_test[:,0], n_test[:,1], 'o')
    plt.plot(test[:,0], test[:,1], 'o')
    plt.xlabel('w')
    plt.ylabel('h')
    plt.legend(['no_stress', 'stress'])
    plt.title('Test Data')
    plt.show()
    return n_train, n_test, train, test

def MDC(n_train, train, test_set):
    n_mid_point = sum(n_train) / len(n_train)
    mid_point = sum(train) / len(train)

    wrong_point = 0
    n_wrong_point = 0
    pre_stress = []
    pre_n_stress = []
    label_li = []
    for point in test_set:
        test_point = np.array([float(i) for i in point[:-1]])
        n_distance = sum(n_mid_point * test_point - (n_mid_point * n_mid_point) / 2)
        distance = sum(mid_point * test_point - (mid_point * mid_point) / 2)
#        print(n_distance, distance)
        if n_distance < distance:
            label = 'stress'
            label_li.append(label)
        else:
            label = 'n_stress'
            label_li.append(label)

        if label != point[2] and label == 'stress':
            wrong_point += 1
        elif label != point[2] and label == 'n_stress':
            n_wrong_point += 1
            
    print('n_stress has : {} wrong point'.format(wrong_point))
    print('stress has : {} wrong point'.format(n_wrong_point))
    label_li = np.array(label_li)
    predict = np.concatenate((test_set[:,:-1],label_li[:,None]),axis=1)
    
    for pre in predict:
        if pre[2] == 'stress':
            pre_stress.append(pre[:-1])
        else:
            pre_n_stress.append(pre[:-1])
    
    pre_stress = np.array(list(map(lambda x: [float(x[0]), float(x[1])], pre_stress)))
    pre_n_stress = np.array(list(map(lambda x: [float(x[0]), float(x[1])], pre_n_stress)))
    plt.figure()
    plt.plot(pre_n_stress[:,0], pre_n_stress[:,1], 'o')
    plt.plot(pre_stress[:,0], pre_stress[:,1], 'o')
    plt.xlabel('w')
    plt.ylabel('h')
    plt.legend(['no_stress', 'stress'])
    plt.title('Predict Data')
    plt.show()       
    
if __name__ == '__main__':
    n_stress = pd.read_csv('NotStress.csv')
    stress = pd.read_csv('Stress.csv')
    part1(n_stress, stress)
    
    n_train, n_test, train, test = part2(n_stress, stress)
    
    train_set = add_label(train, n_train)
    test_set = add_label(test, n_test)
    

    k = np.arange(1,23,2)
    MDC(n_train, train, test_set)
    '''
    knn
    '''    
    kNN = knn(k)
    point = kNN.get_wrong_point(train_set, test_set, k)
    plt.figure()
    plt.plot(k, point)
    plt.xlabel('k')
    plt.ylabel('point')    
    plt.xticks(k)
    plt.title('MisClassified')
    plt.show()
        
