import os
import sys
import cv2
import time
import numpy as np

from keras.models import Model, load_model
## 使用GPU
from keras import backend as K
K.tensorflow_backend._get_available_gpus()


##   將原圖與預測出來的遮罩合併在一起，去掉背景
##   imgPath : 圖片路徑
##   model : 訓練完的模型
def removeBackground(imgPath, model):
    # imgOrg = cv2.imread(imgPath)
    imgOrg = imgPath
    width, height = imgOrg.shape[:2]
    img = cv2.resize(imgOrg, (256, 256))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    mask = model.predict(img)
    mask = (mask > 0.5).astype(np.uint8)                    ### 因為 sigmoid 結果為 0~1 之間，所以要取一半作為臨界值
    mask = np.squeeze(mask)                                 #### 將 mask 降維   (256,256,1) -> (256,256)
    mask = cv2.resize(mask, (height, width), interpolation=cv2.INTER_CUBIC)
    b,g,r = cv2.split(imgOrg)       # get b,g,r
    imgOrg = cv2.merge([r,g,b])     # switch it to rgb
    remove = cv2.bitwise_and(imgOrg, imgOrg, mask= mask)
    b,g,r = cv2.split(remove)
    remove = cv2.merge([r,g,b])
    return remove
    # cv2.imshow('Original', imgOrg)
    # cv2.imshow('Remove', remove)
    # cv2.waitKey(0)
    # plt.figure(figsize=(15,15))
    # plt.subplot(121)
    # plt.grid(False)
    # plt.imshow(imgOrg)
    # plt.subplot(122)
    # plt.grid(False)
    # plt.imshow(remove)

################################ 背景與分割圖片做合成 #########################################
def MergeBackground(foreground, background, maskPath): 
    # Read the images
    mask = maskPath
    _, alpha = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]), 
                                    interpolation=cv2.INTER_CUBIC)
    
    # Convert uint8 to float
    foreground = foreground.astype(float)
    background = background.astype(float)
    
    # Normalize the alpha mask to keep intensity between 0 and 1
    alpha = alpha.astype(float)/255.0
    
    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)
    
    # Multiply the background with ( 1 - alpha )
    background = cv2.multiply(1.0 - alpha, background)
    
    # Add the masked foreground and background.
    outImage = cv2.add(foreground, background)

    outImage = outImage/255
    saveImg = np.zeros((foreground.shape[0], foreground.shape[1], 3))
    cv2.normalize(outImage, saveImg, 0, 255, cv2.NORM_MINMAX)
    # b,g,r = cv2.split(saveImg)
    # saveImg = cv2.merge([r,g,b])
    saveImg = saveImg.astype(np.uint8)
    # cv2.imwrite('tt.png', saveImg)
    return saveImg
    # print(outImage.shape)

    # # Display image
    # plt.imshow(outImage)
    # cv2.imwrite('tt.png', saveImg)


#################### 將背景為黑色變為透明 ##############################
def BlackBackgroundToTransparent(imgPath, savePath):
    image = cv2.imread(imgPath)
    #     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image[np.all(image == [0, 0, 0, 255], axis=2)] = [0, 0, 0, 0]
    cv2.imwrite(savePath, image)

# def imageDetection(img):
#     m = 0
#     if (img.shape[0] % 2) != 0:
#         m = np.insert(img, 0, values=0, axis=0)
#     elif (img.shape[1] % 2) != 0:
#         m = np.insert(img, 0, values=0, axis=1)
#     elif img.shape[1] % 2 == 0 and img.shape[0] % 2 == 0:
#         m = img
#     return m