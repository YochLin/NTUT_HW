## 訓練 GAN 來產生新的驗證碼圖形

import cv2
import numpy as np
import os
import glob
import tensorflow as tf

from Model import *



def one_hot_encoder(label, classNumber):
    onehot = []
    for i in label:
        letter = [0 for _ in range(classNumber)]
        letter[i] = 1
        onehot.append(letter)
    return np.array(onehot)

def dataProcessing(folderPath):    
    labels = []
    datas = []
    i = 0
    for labelPath in os.listdir(folderPath):
        imgPath = glob.glob(os.path.join(folderPath, labelPath)+ "/*.png")
        for path in imgPath:
            img = cv2.imread(path, 0)
            img = cv2.resize(img, (20,20), interpolation=cv2.INTER_CUBIC)
#             img = img.reshape(28,28,1)
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            labels.append(i)
            datas.append(img)
        i = i+1

    labels = one_hot_encoder(np.array(labels), 26)
    
    datas = np.array(datas)
    return datas, labels



if __name__ == '__main__':
    datas, labels = dataProcessing('./Extract_image/')
    dcgan = DCGAN()
    dcgan.train(datas, epochs=50000, batch_size=32, save_interval=50)