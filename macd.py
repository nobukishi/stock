import os
import datetime as dt
import pandas_datareader.data as web
import talib as ta
#銘柄コード入力(7177はGMO-APです。)
ticker_symbol="8609"
ticker_symbol_dr=ticker_symbol + ".T"

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
end = df.iloc[-1,6]
print(end)