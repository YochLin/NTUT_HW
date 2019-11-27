from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import os

## 將該網頁驗證碼爬下來

driver = webdriver.PhantomJS()   ## 使用 PhantomJS 能將 JS動態處理的結果顯示出來
driver.get('https://nportal.ntut.edu.tw/index.do?thetime=1544083343415')   ##獲取網站原始碼
element = driver.find_element_by_id('authImage')   ## 找尋驗證碼 ID
for i in range(1):
    element.click()    ## 對驗證碼做點擊動作
    img = BeautifulSoup(driver.page_source, 'xml').find(id='authImage')   ## 找尋驗證碼 html
    img_URL = "https://nportal.ntut.edu.tw/" + img['src']    ## 取得驗證碼來源
    request = requests.get(img_URL)                          ## 獲得驗證碼來源 URL
    if not os.path.exits('./image/'):
        os.mkdir('./image/')
    with open('./image/image_{}.png'.format(i), 'wb') as f: 
        f.write(request.content)                             ## 存取圖片
    f.close