import pandas as pd
from pykrx import stock
from datetime import date

#날짜 포맷 YYYYMMDD
to_day = date.today().isoformat().replace('-','')

# 1. 수집
# 1.1 주식 종목을 가지고 온다.
 # 1.1.1 신규 종목 가지고 오기.
# df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
# df.to_csv('./stock_list/stock_list_'+date.today().isoformat()+'.scv')

# tickers = stock.get_market_ticker_list("20200209", market='ALL')
tickers = pd.DataFrame(stock.get_etf_ticker_list(to_day))
tickers.to_csv('./stock_list/ETF_ticker_list_'+date.today().isoformat()+'.scv')
tickers = pd.DataFrame(stock.get_market_ticker_list(to_day, market='KOSPI'))
tickers.to_csv('./stock_list/KOSPI_ticker_list_'+date.today().isoformat()+'.scv')
tickers = pd.DataFrame(stock.get_market_ticker_list(to_day, market='KOSDAQ'))
tickers.to_csv('./stock_list/KOSDAQ_ticker_list_'+date.today().isoformat()+'.scv')


tickers ={}
tickers['kospi_tickers'] = ''
tickers['kosdaq_tickers'] =''
tickers['etf_tickers'] = ''



# 1.1.2 추가된 종목에 대한 리스트 추가 