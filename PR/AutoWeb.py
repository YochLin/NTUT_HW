from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import cv2
from keras.models import load_model
import imutils
from PIL import Image
import numpy as np
import time
import io 
import sys

from ImgProcessing import *

# 這次採用擷取整張瀏覽器圖片去尋找驗證碼位置，並將他擷取下來做後續的辨識，因為北科大網站的驗證碼是用 JS 動態生成，所以每次訪問的時候圖片會改變，
# 導致於網頁上顯示的驗證碼，與實際辨識的驗證碼圖片是不相同的，目前是採取擷取瀏覽器圖片再去尋找驗證碼位置做剪取。

# 24吋螢幕: 
# 瀏覽器size: {'width': 945, 'height': 1020} 
# 全圖size: (929, 889) 
# 截圖位置： (527,237,616,266) 

# 32吋螢幕: 
# 瀏覽器size: {'width': 1265, 'height': 1380} 
# 全圖size: (1249, 1249) 
# 截圖位置：(687,237,776,266) 

# Mac 13.5吋螢幕: 瀏覽器size: {'width': 1050, 'height': 840} 
# 全圖size: (1034, 709) 
# 截圖位置:(579,237,668,266) 


def resize_to_fit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """

    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]

    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)

    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Need two argumet: account & password & model')
        sys.exit()

    LoginUrl= ('https://nportal.ntut.edu.tw/index.do?thetime=1521358612211')
    UserName= (sys.argv[1])      #### 帳號
    UserPass= (sys.argv[2])      ### 密碼

    labelPre = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h', 8:'i', 9:'j', 10:'k', 11:'l',
            12:'m', 13:'n', 14:'o', 15:'p', 16:'q', 17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 22:'w', 23:'x',
            24: 'y', 25:'z'}
    inputWeb = True                       ## 確認是否進入網站
    model = load_model(sys.argv[3])    ## 導入模型


    # Browser = webdriver.PhantomJS()
    Browser = webdriver.Chrome()
    Browser.get(LoginUrl)   ##獲取網站原始碼
    while(inputWeb):
        verify = ""           ## 驗證碼存取變數
        
        screen_shot_data = Browser.get_screenshot_as_png()            ### 擷取瀏覽器圖片 (內容為 Bytes)
        screen_shot_data = Image.open(io.BytesIO(screen_shot_data))   ## 利用 PIL 來讀取
        img = screen_shot_data.crop((687,237,776,266))                ## 尋找驗證碼位置後，將他剪取下來
        img = img.convert('RGB')                                      ## 轉為RGB型式
        img = np.array(img)                                           ## 轉為 Array
        
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)                  ## 就能使用 OpenCV Library 來做操作了


        # 在外圍多加8格
        gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_CONSTANT)

        #     blur = cv2.GaussianBlur(gray, (3,3), 0)            ## 高斯濾波器
        ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        i, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(img, contours, -1, (0,0,0), thickness= 1)    ## 畫出邊緣偵測

        letter_regions = []

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

        #     cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)    ## 畫出框出來的矩形
            letter_regions.append([x, y, w, h])
        
        ## 對於 i，j 上面點點做合併動作
        new_letter = MergeContour(letter_regions, GetContoursDiff(letter_regions))    

        
        ## 以 x 座標做排序， 確保處理的時候是從左邊開始                    
        new_letter = sorted(new_letter, key=lambda x: x[0])
        if len(new_letter) != 4:
            continue
        
        ##  找尋每個字母位置並做預測
        for letter_bounding_box in new_letter:

            x, y, w, h = letter_bounding_box

            # Extract the letter from the original image with a 2-pixel margin around the edge
            letter_image = gray[y - 4: y + h + 4 ,  x - 4 :x + w + 4]
            letter_image = resize_to_fit(letter_image, 20, 20)
            letter_image = np.expand_dims(letter_image, axis=2)
            letter_image = letter_image.reshape((1,20,20,1))     ## 將圖片 reshape 為 Model 輸入型式
            predition = model.predict(letter_image)              ## model 預測
            index = np.argmax(predition)
            verify = verify + labelPre[index]
            print(verify)
            
        
        Browser.find_element_by_id('muid').send_keys(UserName)        ## 輸入帳號
        Browser.find_element_by_id('mpassword').send_keys(UserPass)   ## 輸入密碼
        Browser.find_element_by_id('authcode').send_keys(verify)      ## 輸入驗證碼
        time.sleep(5)
        Browser.find_element_by_css_selector("input[value='登入 Login']").click()    ## 案下登入
        
        try:
            check = Browser.find_element_by_css_selector("input[value='重新登入']")
            if(inputWeb == True):
                check.click()    ## 點擊重新登入
        except:
            check = None
            pass
        if check != None:
            inputWeb = True
        else:
            inputWeb = False
