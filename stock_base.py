import pandas as pd
from pykrx import stock
from datetime import date

to_day = date.today().isoformat().replace('-','')

# 1. 수집
# 1.1 주식 종목을 가지고 온다.
 # 1.1.1 신규 종목 가지고 오기. - ETF,KOSPI,KOSDAQ

# tickers = stock.get_market_ticker_list("20200209", market='ALL')
tickers = stock.get_etf_ticker_list(to_day)
tickers = pd.DataFrame(tickers)
tickers.to_csv('./stock_list/stock_etf_list_'+date.today().isoformat()+'.scv')




# 1.1.2 추가된 종목에 대한 리스트 추가 