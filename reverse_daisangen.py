from time import sleep
import datetime as dt
import pandas_datareader.data as web

import crawler

from margin_ratio import get_margin_ratio
 
def get_owarine(code):
    #終値を6日取得する関数
    ticker_symbol=code
    ticker_symbol_dr=str(ticker_symbol) + ".JP" 
    start='2022-01-01'
    end = dt.date.today() 
    df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
    print(df)
    owarine_map =[]
    i = 0
    for i in range(6): 
        price = df.iloc[i,3]
        owarine_map.append(price)
    
    print(owarine_map)
    return owarine_map


def get_mean25(code):
    ticker_symbol=code
    ticker_symbol_dr=str(ticker_symbol) + ".JP" 
    start='2022-01-01'
    end = dt.date.today() 
    #2022-01-01以降の株価取得
    df = web.DataReader(ticker_symbol_dr, data_source='stooq', start=start,end=end)
    df= df.sort_index(ascending=True)
    df['mean25'] = df["Close"].rolling(25).mean()
    mean25 = df.iloc[-1,5]
    print(mean25)
    return mean25
    

def  failure_check_trend1(owarine_map):
     """トレンド１が不合格しているか"""
     
     one_kakaku = owarine_map[0]
     two_kakaku = owarine_map[1]
     three_kakaku = owarine_map[2]
     fore_kakaku = owarine_map[3]
     five_kakaku = owarine_map[4]
    #print(five_kakaku)
     if one_kakaku > two_kakaku: 
         return False
     if one_kakaku > three_kakaku:
         return False 
     if one_kakaku > fore_kakaku:
         return False 
     return True  
 

def failure_check_trend2(owarine_map,mean25):
    """トレンド２が不合格しているか"""
    
    one_kakaku = owarine_map[0]
    print(mean25)
    if one_kakaku > mean25:
        return False
    return True     


def failure_check_neckline(owarine_map):
    """ネックラインは不合格か（当日を含まない過去５日間の終値ベースの高値を当日の終値で下回る）  """
    
    one_kakaku = owarine_map[0]
    two_kakaku = owarine_map[1]
    three_kakaku = owarine_map[2]
    fore_kakaku = owarine_map[3]
    five_kakaku = owarine_map[4]
    six_kakaku = owarine_map[5]
    #print(one_kakaku)
    if one_kakaku > two_kakaku:
        return False
    if one_kakaku > three_kakaku:
        return False 
    if one_kakaku > fore_kakaku:
        return False 
    if one_kakaku > five_kakaku:
        return False 
    if one_kakaku > six_kakaku:
        return False 
    return True    
     

def failure_check_macd(macdhist):
    """モーメンタムは不合格か（ＭＡＣＤヒストグラムがマイナス）"""
    
    macd = macdhist
    if macd > 0:
        return False
    return True


def failure_decision_buy(code):
    """売りシグナルの判定"""
    
    owarine_map=get_owarine(code)
    mean25 = get_mean25(code)
    macd = crawler.get_macdhist(code)
    if macd is None:
        print('macdが取得できない')
        return False      
    margin_ratio = get_margin_ratio(code)
   # peg = get_peg(code)
    # if peg == None or peg>= 1.1:
    #     print('PEGが'+str(peg)+'のため投資不可')
    #     return False
    if margin_ratio == None or margin_ratio <= 1:
         print('信用倍率が'+str(margin_ratio)+'のため売り')
         return True
    if failure_check_trend1(owarine_map)==False:
        print('トレンド1を維持')
        return False
    if failure_check_trend2(owarine_map,mean25)==False:
        print('トレンド2を維持')
        return False
    if failure_check_neckline(owarine_map)==False:
        print('ネックラインを維持')
        return False
    if failure_check_macd(macd) ==False:
        print('macdを維持')
        return False
    #print(code)
    return True


def get_sell_lists():   
    sell_lists=[]    
    interval = 1
    #with open('./gold_list.csv')as f:
    with open('./test_list.csv')as f:
        for s_line in f.readlines():
            code = s_line.strip()
            sleep(interval)
            print(code)
            if failure_decision_buy(code)==True:
                sell_lists.append(code)
            #break
    print(sell_lists)
    return sell_lists

if __name__=='__main__':
    sell_lists = get_sell_lists()
    print(sell_lists)
    #save_sell_lists()

 

