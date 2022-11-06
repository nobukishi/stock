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
def get_margin_ratio(code):
    #終値を数日前取得
    driver.get(f'https://kabutan.jp/stock/kabuka?code={code}')
    div = driver.find_element(By.ID,'main')
    elem_table1= div.find_element(By.ID, "stockinfo_i3")
        
    elem_tr_list = elem_table1.find_elements(By.XPATH,'table/tbody/tr')
    elem_tr = elem_tr_list[0]
            #elem_tds1 = elem_tr1.find_elements(By.XPATH,'td')   
    #print(elem_tr)       
    elem_td_list= elem_tr.find_elements(By.XPATH,'td')
    elem_td = elem_td_list[3].text
    try:
        margin_ratio = float(elem_td.replace('倍',''))
        return margin_ratio
    except:
        return None
            
                
