import random
import math
import time
import matplotlib.pyplot as plt

'''
This is competitive learning network
'''



def normalization(seq):
    '''
    square sum & sqrt then all value divided it
    '''
    vector = 0
    for w in seq:
        vector += sum([i*i for i in w])
    nom = math.sqrt(vector)
    return [[i / nom for i in w]for w in seq]

def find_max(perceptron):
    '''
    find maximum value & index
    '''
    max_ = 0
    index = 0
    for i, items in enumerate(perceptron):
        if max_ < items:
            max_ = items
            index = i
    return index, max_


def perceptron(x, w):
    '''
    X * W
    '''
    out = []
    for weights in w:        
        out.append(sum(list(map(lambda D, W: D * W, x, weights))))
    return find_max(out)

def update(data, max_W):
    '''
    update_W = W - (X - W)
    '''
    update_weight = []
    ## (X - W)
    for weights in max_W:      
            update_weight.append(sum(list(map(lambda D: D - weights, data))))   ## 將資料與權重相減，再取總和
    ## W - (X - W)
    out = list(map(lambda old, new: learning_rate * new + old, max_W, update_weight))
    return out

def count_class(class_):
    '''
    count class value
    '''
    c_ = set(class_)
    for c in c_:
        count = 0
        for cc in class_:
            if c == cc:
                count += 1
        print("class {} = {}" .format(c, count))

if __name__ == "__main__":
    learning_rate = 0.005
    ## Read the Stone data (Do people swim ?)
    with open('Practice05_Data.txt', 'r') as f:
        data = [items.replace('\n', "").split('\t') for items in f]
        data = [[float(i) for i in each[1:-1]] for each in data]
    ## get random weight
    Weights = []
    for i in range(10):
        Weights.append([random.random() for j in range(4)])
    ## nomalization
    Weights = normalization(Weights)
    nom_data = normalization(data)
    ## Training
    for i, data in enumerate(nom_data):
        max_index, max_value = perceptron(data, Weights)
        Weights[max_index] = update(data, Weights[max_index])
        print("Step {}, max index {}, max_value {}, new_Weights {}"  .format(i, max_index, max_value, Weights[max_index]))
    
    data_classes = []
    for i, data in enumerate(nom_data):
        data_classes.append(perceptron(data, Weights)[0])

    count_class(data_classes)  
 
    plt.figure()
    plt.scatter([i[0]for i in nom_data], [i[1]for i in nom_data], c=data_classes)
    plt.title('R & G')
    plt.xlabel('R')
    plt.ylabel('G')
    plt.figure()
    plt.scatter([i[0]for i in nom_data], [i[2]for i in nom_data], c=data_classes)
    plt.title('R & B')
    plt.xlabel('R')
    plt.ylabel('B')
    plt.figure()
    plt.scatter([i[0]for i in nom_data], [i[3]for i in nom_data], c=data_classes)
    plt.title('R & H')
    plt.xlabel('R')
    plt.ylabel('H')
    plt.figure()
    plt.scatter([i[1]for i in nom_data], [i[2]for i in nom_data], c=data_classes)
    plt.title('G & B')
    plt.xlabel('G')
    plt.ylabel('B')
    plt.figure()
    plt.scatter([i[1]for i in nom_data], [i[3]for i in nom_data], c=data_classes)
    plt.title('G & H')
    plt.xlabel('G')
    plt.ylabel('H')
    plt.figure()
    plt.scatter([i[2]for i in nom_data], [i[3]for i in nom_data], c=data_classes)
    plt.title('B & H')
    plt.xlabel('B')
    plt.ylabel('H')
    plt.show()
    
