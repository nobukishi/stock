from webbrowser import Konqueror
from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import statistics


options = Options()
options.add_argument('--headless')
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome(options=options)

#信用倍率を取得

#終値を数日前取得
driver.get(f'https://kabutan.jp/stock/kabuka?code=8609')
div = driver.find_element(By.ID,'main')
elem_table1= div.find_element(By.ID, "stockinfo_i3")
 
margin_ratio = []
    
for elem_tr1 in elem_table1.find_elements(By.XPATH,'//tbody/tr'):
        elem_th1 = elem_tr1.find_elements(By.XPATH,'td')
        #elem_tds1 = elem_tr1.find_elements(By.XPATH,'td')   
       
        kakaku = elem_th1[3].text
        margin_ratio.append(kakaku)
        print(margin_ratio)   
