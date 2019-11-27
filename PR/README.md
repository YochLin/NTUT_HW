## NTUT 自動驗證碼辨識
此專案是由PR課堂所製作，應用到深度學習CNN來做圖形識別與DCGAN來將少量資料增加達到大量資料以利訓練。

## 操作環境
本次使用 Anaconda for Windows 環境
* GPU : GeForce　GTX 970
* Tensorflow : 1.9.0
* CUDA : 9.0.0
* CUDNN : 7.1.4
* Keras : 2.2.4

### 製作順序

* 爬蟲-驗證碼 : 將驗證碼爬到 image 資料夾內
```
python Reptile.py
```

* 分割字母：將剛爬取的影像做字母切割，並存到 Extract_image 資料夾內(但是圖片檔案名稱需與驗證碼圖示相同)
```
python imgProcessing.py
```

* 訓練DCGAN：假如不想爬太多驗證碼圖片去改名稱，可以使用GAN將少量圖片增加
```
python trainGan.py
```
![GIF](https://github.com/YochLin/NTUT_HW/blob/master/PR/show/DCGAN.gif)

* 訓練 CNN ： 輸入欲存的模型名稱
```
python trainCNN.py saveModelName
```

* 自動登入NTUT網頁
要先在裡面輸入自己的帳號密碼和訓練好的辨識模型
```
python AutoWeb.py your_NTUTAccount your_NTUTPassword your_ClassificationModel
```

## Reference
DCGAN : https://github.com/eriklindernoren/Keras-GAN
