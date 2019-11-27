import numpy as np

##########################  計算 Precision & Recall & F1-Measure ##################################
## 將原分割圖與預測分割圖做比對得出， 將圖片內容改為 True & False ， 只要有像素值都為 True ，沒有像素值為 False ，這樣就好判定分割的區域是否正確
## realImg : 原圖
## predImg : 預測圖
## height : 高
## width : 寬
## channel : 通道
## 輸出：Precision , Recall, F1-Measure
def Precision_Recall(realImg, predImg, height, width, channel):
    real = realImg.astype(np.bool)
    pred = predImg.astype(np.bool)
    TP = 0.0
    FP = 0.0
    FN = 0.0
    TN = 0.0
    for k in range(channel):
        for i in range(height):
            for j in range(width):
                if real[i, j, k] == True:
                    if pred[i, j, k] == True:
                        TP += 1
                    elif pred[i, j, k] == False:
                        FN += 1
                elif real[i, j, k] == False:
                    if pred[i, j, k] == True:
                        FP += 1
                    elif pred[i, j, k] == False:
                        TN += 1
    print(TP, FP, FN, TN)
    print("Precision: %.4f" % (TP / (TP + FP)))
    print("Recall: %.4f" % (TP / (TP + FN)))
    print("F1: %.4f" % ((2 * TP) / (2*TP + FP + FN)))
    return (TP / (TP + FP)), (TP / (TP + FN)), ((2 * TP) / (2*TP + FP + FN))

##########################  計算 MAE ##################################
## 將原分割圖與預測分割圖每點像素值做公式求得
## realImg : 原圖
## predImg : 預測圖
## height : 高
## width : 寬
## channel : 通道

def MAE(realImg, predImg, height, width, channel):
    mae = 0.0
    for k in range(channel):
        for i in range(height):
            for j in range(width):
                mae += abs(float(predImg[i, j, k]) - float(realImg[i, j, k]))
    print("MAE : %.4f" % (mae / (height * width)))
    return (mae / (height * width))