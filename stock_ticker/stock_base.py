import pandas as pd
from pykrx import stock
from datetime import date
from config.log_class import *

class Get_stock_ticker():
    def __init__(self):
        self.logging = Logging()
        
        #날짜 포맷 YYYYMMDD
        to_day = date.today().isoformat().replace('-', '')
        self.logging.logger.debug("수행시간 : "+ to_day)
        # 1. 수집
        # 1.1 주식 종목을 가지고 온다.
        # 1.1.1 신규 종목 가지고 오기. - ETF,KOSPI,KOSDAQ

        tickers = pd.DataFrame(stock.get_etf_ticker_list(to_day))
        tickers.to_csv('./stock_data_ticker/ETF/ETF_ticker_list_'+date.today().isoformat()+'.scv')
        self.logging.logger.debug("Get ETF_ticker")

        tickers = pd.DataFrame(stock.get_market_ticker_list(to_day, market='KOSPI'))
        tickers.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_'+date.today().isoformat()+'.scv')
        self.logging.logger.debug("Get KOSPI ")

        tickers = pd.DataFrame(stock.get_market_ticker_list(to_day, market='KOSDAQ'))
        tickers.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_'+date.today().isoformat()+'.scv')
        self.logging.logger.debug("Get KOSDAQ ")


        tickers ={}
        tickers['kospi_tickers'] = ''
        tickers['kosdaq_tickers'] =''
        tickers['etf_tickers'] = ''
        



        # 1.1.2 추가된 종목에 대한 리스트 추가 