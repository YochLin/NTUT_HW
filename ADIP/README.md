## NTUT ADIP 人像去背
這次期末專案，課堂要求做人像去背                    
以往人像去背通常都使用 photoshop 來手動選取範圍，但當你想去背的圖像一多，就容易框到眼花撩亂               
本次採用深度學習方法，透過**U-net**架構來將人物分割做出去背效果        

號外：現在 Adobe 開發的 photoshop 已有加入機器學習功能，能透過一鍵搞定啦~   
> https://www.youtube.com/watch?time_continue=92&v=x-9qYLr15tU

**已訓練好 Model**
> https://drive.google.com/drive/folders/1uPJseOzsqSlCi30s7qulgMoGaD8zvBMH?usp=sharing


####  訓練 model
使用 `train.py` 要將裡面處理資料的部分修改為自己的訓練資料
```
python train.py
```

#### 去背效果
```
python main.py
```


#### UI介面

![Image](https://github.com/YochLin/NTUT_HW/blob/master/ADIP/show/interface.PNG)
![Image](https://github.com/YochLin/NTUT_HW/blob/master/ADIP/show/demo.PNG)

#### 去背效果
![Image](https://github.com/YochLin/NTUT_HW/blob/master/ADIP/show/result1.png)
![Image](https://github.com/YochLin/NTUT_HW/blob/master/ADIP/show/result2.png)


