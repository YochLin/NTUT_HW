import os
import sys
import random
import warnings
import cv2
import time
import numpy as np
import glob
from tqdm import tqdm          ## 顯示進度條


##################### 用來將檔案內的 Image 或 Mask 寫入 TXT 檔案，會將 Image & Mask 做對應   ##########################
## ImagePath : 圖片全路徑
## MaskPath : 遮罩資料夾路徑
## saveName : 要存的 TXT 名稱
## typeMask : 遮罩圖片的副檔名           
def txtWriter(ImagePath, MaskPath, saveName, typeMask='.png'):
    with open(saveName + '.txt', 'w') as f:
        for name in ImagePath:
            fileName = os.path.splitext(name)[0]
            fileName = fileName.split('/')[-1]
            f.write(name + ' ' + MaskPath + fileName + typeMask + '\n')

############################## 多筆資料要做訓練時，藉由此函式讀取資料並搭配 keras 的 fit_generate ##############################
## 隨機生成 Image & Mask
## txtFile : TXT 檔案路徑
## batch_size : batch 大小
## IMAGW_WIDTH : 圖片寬度
## IMAGW_HEIGHT : 圖片高度
def generate_data(txtFile, batch_size, IMAGE_WIDTH, IMAGE_HEIGHT):
    """Replaces Keras' native ImageDataGenerator."""
    f = open(txtFile, 'r')
    items = f.readlines()
    i = 0
    while True:
#         image_batch = []
#         label_batch = []
        image_batch = np.zeros((batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.float32)
        label_batch = np.zeros((batch_size, IMAGE_HEIGHT, IMAGE_WIDTH, 1), dtype=np.bool)
        for b in range(batch_size):
            mask = np.zeros((IMAGE_WIDTH, IMAGE_HEIGHT, 1), dtype=np.bool)
            if i == len(items)//batch_size:
                i = 0
                random.shuffle(items)
            sample = items[i]
            image_path = sample.split(' ')[0]                   ## 以空白部分分開兩段  [xxx xxx]
            label_path = sample.split(' ')[-1].strip()          ## 去掉後面 \n
            #### 圖片處理
            image = cv2.resize(cv2.imread(image_path), (IMAGE_WIDTH, IMAGE_HEIGHT), 
                               interpolation=cv2.INTER_CUBIC)
            image_batch[b] = image.astype(np.float32) / 255.0
            ### 遮罩處理
            label = cv2.imread(label_path)
            label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
            label = cv2.resize(label,(IMAGE_WIDTH,IMAGE_HEIGHT), interpolation=cv2.INTER_CUBIC)
#             b, label = cv2.threshold(label, 0, 255, cv2.THRESH_BINARY)   ## 進行二值化，使目標物變成白色
#             label = label.astype(np.float32) / 255.0
            label = np.expand_dims(label, axis=-1)
            mask = np.maximum(mask, label)
            label_batch[b] = mask
            i += 1
        yield image_batch, label_batch

############################################ 導入全部 data & label #################################################################
### imgPath : 所有圖片列表
### maskFolder : 遮罩資料夾
### IMAGE_HEIGHT : 欲調整圖片之高
### IMAGE_WIDTH :欲調整圖片之寬
def load_data(imgPath, maskFolder, IMAGE_HEIGHT, IMAGE_WIDTH, maskTpye='.png'):
    print('Getting and resizing image & masks ...')
    sys.stdout.flush()
    image_batch = np.zeros((len(imgPath), IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.float32)
    label_batch = np.zeros((len(imgPath), IMAGE_HEIGHT, IMAGE_WIDTH, 1), dtype=np.bool)
    
    for i, trainPath in tqdm(enumerate(imgPath), total=len(imgPath)):
        mask = np.zeros((IMAGE_WIDTH, IMAGE_HEIGHT, 1), dtype=np.bool)
        image = cv2.resize(cv2.imread(trainPath), (IMAGE_WIDTH, IMAGE_HEIGHT), 
                           interpolation=cv2.INTER_CUBIC)
        image_batch[i] = image.astype(np.float32) / 255.0
        
        labelPath = os.path.splitext(trainPath)[0]
        labelPath = maskFolder + labelPath.split('/')[-1] + maskTpye
        ### 遮罩處理
        label = cv2.imread(labelPath)
        label = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
        label = cv2.resize(label,(IMAGE_WIDTH,IMAGE_HEIGHT), interpolation=cv2.INTER_CUBIC)
        b, label = cv2.threshold(label, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)   ## 進行二值化，使目標物變成白色
#             label = label.astype(np.float32) / 255.0
        label = np.expand_dims(label, axis=-1)
        mask = np.maximum(mask, label)
        label_batch[i] = mask
    print(image_batch.shape, label_batch.shape )
    return image_batch, label_batch
