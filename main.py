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

def get_owarine(code):
    driver.get(f'https://kabutan.jp/stock/kabuka?code={code}')
    div = driver.find_element(By.ID,'stock_kabuka_table')
    elem_table1= div.find_element(By.CLASS_NAME, "stock_kabuka0")
    elem_table2= div.find_element(By.CLASS_NAME, "stock_kabuka_dwm")

    owarine_map={}
#直近１日目を取得するのにforを使わずに取得し、２日目以降とつなげたい
    for elem_tr1 in elem_table1.find_elements(By.XPATH,'tbody/tr'):
        elem_th1 = elem_tr1.find_element(By.XPATH,'th')
        elem_tds1 = elem_tr1.find_elements(By.XPATH,'td')   
        #print(elem_th.text,elem_tds[3].text)
        kakaku = elem_tds1[3].text
        owarine_map[elem_th1.text]=int(kakaku.replace(',',''))   


    for elem_tr2 in elem_table2.find_elements(By.XPATH,'tbody/tr'):
        elem_th2 = elem_tr2.find_element(By.XPATH,'th')
        elem_tds2 = elem_tr2.find_elements(By.XPATH,'td')   
        #print(elem_th.text,elem_tds[3].text)
        kakaku = elem_tds2[3].text
        owarine_map[elem_th2.text]=int(kakaku.replace(',',''))    
    return owarine_map


def check_trend2(owarine_map):
    date_list=list(owarine_map.keys())
    date_list.sort(reverse=True)
    #print(date_list)
    one_kakaku = owarine_map[date_list[0]]
    two_kakaku = owarine_map[date_list[1]]
    three_kakaku = owarine_map[date_list[2]]
    fore_kakaku = owarine_map[date_list[3]]
    #print(one_kakaku)
    if one_kakaku < two_kakaku:
        return False
    if one_kakaku < three_kakaku:
        return False 
    if one_kakaku < fore_kakaku:
        return False 
    return True    


def check_trend3(owarine_map):
    date_list=list(owarine_map.keys())
    one_kakaku = owarine_map[date_list[0]]
    date_list1 = list(owarine_map.values())
    date_list25 = date_list1[:25]
    mean25 = statistics.mean(date_list25)
    #print(mean25)
    if one_kakaku < mean25:
        return False
    return True
    
    
    
    

def main():
    owarine_map=get_owarine(8609)
#print(owarine_map)
    if check_trend2(owarine_map)==False:
        print('トレンド２に失敗')
        return False
    if check_trend3(owarine_map)==False:
        print('トレンド3に失敗')
        return False
    print('合格')
    
main()
owarine_map=get_owarine(8609)
#check =check_trend3(owarine_map)
#print(check)
    
    
    
