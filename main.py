import datetime as dt

from margin_ratio import get_margin_ratio
from db import add_item,get_items
import db
import gyakudaisangen
import daisangen
import crawler

# def get_latest_owarine(code):
#     owarine_map = crawler.get_owarine(code)
#     date_list = list(owarine_map.keys())
#     #print(date_list)
#     #date_list.sort()
#     d = date_list[0]
#     print(d)
#     return owarine_map[d]

# def save_buy_lists():
#     for code in buy_lists:
       
#         stock_name = crawler.get_stock_name(code)
#         buy_day = str(dt.date.today())
#         buy_price = get_latest_owarine(code)
#         item ={
#             'code':code,
#             'stock_name':stock_name,
#             'buy_day':buy_day,
#             'buy_price':buy_price
#         }
#         try:
#             add_item(item)
#         except Exception as e:
#             print(e)

# def execute_daisangen():
#     buy_lists = daisangen.get_buy_lists()
#     print(buy_lists)
#     save_buy_lists()

# def execute_gyakudaisagen():
#     sell_lists=[]
#     items = get_items()
#     for item in items:
#         code = item[1]
#         if gyakudaisangen.failure_decision_buy(code)==True:
#             sell_lists.append(code)
#     print(items)
 
def buy_code(day,code,price,num=100): 
    db.add_trade_log(day,code,buy_price=price,buy_volume=num)
    db.add_trading(day,code)

def sell_code(day,code,price,num=100): 
    db.add_trade_log(day,code,sell_price=price,sell_volume=num)
    db.delete_trading(day,code)

def get_code_list():
    code_list =[]
    #with open('./gold_list.csv')as f:
    with open('./test_list.csv')as f:
        for s_line in f.readlines():
            code = s_line.strip()
            code_list.append(code)
        return code_list
  
def get_price(code):
    owarine_map,_=crawler.stock_price_information(code) 
    return owarine_map[0]
             
def main():
    code_list = get_code_list()
    for code in code_list:
        print(code)
        price = get_price(code)
        buy_day = str(dt.date.today())
        is_daisangen = daisangen.decision_buy(code)
        is_gyakudaisangen = gyakudaisangen.failure_decision_buy(code)
        db.add_daisangen_log(buy_day,code,is_daisangen,is_gyakudaisangen)
        
        if is_daisangen == True:
            buy_code(buy_day,code,price,num=100)
        
        if is_gyakudaisangen == True:
            sell_code(buy_day,code,price,num=100)
            

if __name__=='__main__':
    main()

   

   
 
       






