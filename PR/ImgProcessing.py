# 把每張驗證碼做字母切割，並存放到各個資料夾內

import numpy as np
import cv2
import os
import glob


# ieie.png
# ab = [[78, 18, 11, 12], [57, 18, 3, 12], [34, 18, 11, 12], [13, 18, 3, 12], [57, 14, 3, 2], [13, 14, 3, 2]]

## 找出x邊界相同或是在裡面的邊框(確定是否相同單字卻被分割)
## (i j 上面點點就是會被分割掉)
## arr : 影像
def GetContoursDiff(arr):
    list_ = []
    for i in range(len(arr)):
        x1 = arr[i][0]       ##  x座標
        w1 = arr[i][2]       ##  寬度
        bounding = x1 + w1   
        
        main_img = 0
        sub_img = 0
        for j in range(len(arr)):
            if(i != j):
                if(arr[j][0] > x1 and arr[j][0] < bounding):   # 在 x ~ x+w 內的 做紀錄
                    main_img = i
                    sub_img = j
                    list_.append((main_img, sub_img))
                elif(arr[j][0] == x1 and arr[j][2] == w1):    # 與 x, w 相等 做紀錄
                    main_img = i
                    sub_img = j
                    if(main_img < sub_img):
                        list_.append((main_img, sub_img))                    

    return list_

## 相同單字的邊界做合併  ex: i, j  
## srcArr : 原始圖
### changeArr : 轉換過的圖
def  MergeContour(srcArr, changeArr):
    list_ = []
    arrCopy = srcArr.copy()     ## 複製一份，以免後續處理被覆蓋掉
    for main, sub in changeArr:
        diff = srcArr[main][1] - srcArr[sub][1]
        arrCopy[main][1] = srcArr[sub][1]
        arrCopy[main][3] = srcArr[main][3] + diff
        arrCopy.remove(srcArr[sub])          ## 因為有複製一份所以移除內容並不會對原始做改變
    return arrCopy



counts = {}                       ## 字母存取與計算數量
OUTPUT_FOLDER = 'Extract_image'   ## 輸出資料夾

#### image 資料夾底下，所有 png 檔案
for image_path in glob.glob('./image/*.png'):
    image_name = image_path.split('\\')[1]
    image_name = image_name.split('.')[0]
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 在外圍多加8格
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_CONSTANT)

    #     blur = cv2.GaussianBlur(gray, (3,3), 0)
    ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    i, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0,0,0), thickness= 1)    ## 畫出邊緣偵測

    letter_regions = []

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

    #     cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)    ## 畫出框出來的矩形
        letter_regions.append([x, y, w, h])

    new_letter = MergeContour(letter_regions, GetContoursDiff(letter_regions))    
    if len(new_letter) != 4:
        continue
    ## 以 x 座標做排序， 確保處理的時候是從左邊開始                    
    new_letter = sorted(new_letter, key=lambda x: x[0])

    for letter_bounding_box, letter_text in zip(new_letter, image_name):
        
        x, y, w, h = letter_bounding_box

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letter_image = gray[y - 4: y + h + 4 ,  x - 4 :x + w + 4]

        # Get the folder to save the image in
        save_path = os.path.join(OUTPUT_FOLDER, letter_text)

        # 確認資料夾是否存在，並創建
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # write the letter image to a file
        count = counts.get(letter_text, 1)
        p = os.path.join(save_path, "{}.png".format(str(count).zfill(6)))
        cv2.imwrite(p, letter_image)

        # increment the count for the current key
        counts[letter_text] = count + 1