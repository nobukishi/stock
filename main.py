from webbrowser import Konqueror
from selenium import webdriver
from time import sleep
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import statistics
import datetime as dt
import pandas_datareader.data as web
import talib as ta
from margin_ratio import get_margin_ratio

options = Options()
options.add_argument('--headless')
#driver = webdriver.Chrome('./chromedriver')
driver = webdriver.Chrome(options=options)

#信用倍率を取得

#終値を数日前取得
def get_owarine(code):
    print(dt.datetime.now())
    driver.get(f'https://kabutan.jp/stock/kabuka?code={code}')
    div = driver.find_element(By.ID,'stock_kabuka_table')
    elem_table1= div.find_element(By.CLASS_NAME, "stock_kabuka0")
    elem_table2= div.find_element(By.CLASS_NAME, "stock_kabuka_dwm")
    
    owarine_map={}
#直近１日目を取得するのにforを使わずに取得し、２日目以降とつなげたい
    #当日（１日目のみ）
    for elem_tr1 in elem_table1.find_elements(By.XPATH,'tbody/tr'):
        elem_th1 = elem_tr1.find_element(By.XPATH,'th')
        elem_tds1 = elem_tr1.find_elements(By.XPATH,'td')   
        #print(elem_th1.text,elem_tds1[3].text)
        kakaku = elem_tds1[3].text
        owarine_map[elem_th1.text]=float(kakaku.replace(',',''))   

    #２日目以降
    for elem_tr2 in elem_table2.find_elements(By.XPATH,'tbody/tr'):
        elem_th2 = elem_tr2.find_element(By.XPATH,'th')
        elem_tds2 = elem_tr2.find_elements(By.XPATH,'td')   
        #print(elem_th2.text,elem_tds2[3].text)
        kakaku = elem_tds2[3].text
        owarine_map[elem_th2.text]=float(kakaku.replace(',',''))    
    print(dt.datetime.now())
    return owarine_map


#当日のmacdを取得
def get_macdhist(code):
    ticker_symbol=code
    ticker_symbol_dr=str(ticker_symbol) + ".T"

    #2022-01-01以降の株価取得
    start='2022-01-01'
    end = dt.date.today()

    #データ取得
    df = web.DataReader(ticker_symbol_dr, data_source='yahoo', start=start,end=end)
    #print(df)
    #csv保存
    #df.to_csv( os.path.dirname(__file__) + '\y_stock_data_'+ ticker_symbol + '.csv')
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df[["Open", "High", "Low", "Close", "macd", "macdsignal"]].tail()
    macdhist = df.iloc[-1,8]
    return macdhist
    

#トレンド１が合格しているか
def check_trend1(owarine_map):
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

#トレンド２が合格しているか
def check_trend2(owarine_map):
    date_list=list(owarine_map.keys())
    one_kakaku = owarine_map[date_list[0]]
    date_list1 = list(owarine_map.values())
    date_list25 = date_list1[:25]
    mean25 = statistics.mean(date_list25)
    #print(mean25)
    if one_kakaku < mean25:
        return False
    return True          

#ネックラインは合格か（当日を含まない過去５日間の終値ベースの高値を当日の終値で抜く）  
def check_neckline(owarine_map):
    date_list=list(owarine_map.keys())
    date_list.sort(reverse=True)
    #print(date_list)
    one_kakaku = owarine_map[date_list[0]]
    two_kakaku = owarine_map[date_list[1]]
    three_kakaku = owarine_map[date_list[2]]
    fore_kakaku = owarine_map[date_list[3]]
    five_kakaku = owarine_map[date_list[4]]
    six_kakaku = owarine_map[date_list[5]]
    #print(one_kakaku)
    if one_kakaku < two_kakaku:
        return False
    if one_kakaku < three_kakaku:
        return False 
    if one_kakaku < fore_kakaku:
        return False 
    if one_kakaku < five_kakaku:
        return False 
    if one_kakaku < six_kakaku:
        return False 
    return True    


#モーメンタムは合格か（ＭＡＣＤヒストグラムがプラス）
def check_macd(macdhist):
    macd = macdhist
    if macd < 0:
        return False
    return True

def main(code):
    owarine_map=get_owarine(code)
    macd = get_macdhist(code)
<<<<<<< Updated upstream
    if get_margin_ratio(code) >= 1:
=======
    margin_ratio = get_margin_ratio(code)
    if margin_ratio == None or margin_ratio >= 1:
>>>>>>> Stashed changes
        print(margin_ratio)
        return 
    if check_trend1(owarine_map)==False:
        print('トレンド1に失敗')
        return False
    if check_trend2(owarine_map)==False:
        print('トレンド2に失敗')
        return False
    if check_neckline(owarine_map)==False:
        print('ネックライン失敗')
        return False
    if check_macd(macd) ==False:
        print('macdに失敗')
        return False
    print('合格')
    

    



with open('./gold_list.csv')as f:
    for s_line in f.readlines():
        code = s_line.strip()
        print(code)
        main(code)
      



