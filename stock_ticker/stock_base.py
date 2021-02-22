import pandas as pd
import numpy as np
import time
import os.path

from pykrx import stock
from datetime import date
from config.log_class import Logging




class Get_stock_ticker:
    def __init__(self):
        self.logging = Logging()
        self.logging.logger.debug("main class init")

        # 날짜 포맷 YYYYMMDD
        self.to_day = date.today().isoformat().replace('-', '')
        self.logging.logger.debug("수행시간 : " + self.to_day)

        # 1. list 수집 및 데이터 정리하기
        # 1.1 ticker list 가지고 오기.
        self.get_all_ticker_list()
        # 1.2 개별 종목별 주식 히스토리 불러오기
        self.get_stock_data()


    def get_all_ticker_list(self):
        tickers = pd.DataFrame(stock.get_etf_ticker_list(self.to_day))
        tickers.to_csv('./stock_data_ticker/ETF_ticker_list.scv')
        self.logging.logger.debug("Get ETF_ticker")

        tickers = pd.DataFrame(stock.get_market_ticker_list(self.to_day, market='KOSPI'))
        tickers.to_csv('./stock_data_ticker/KOSPI_ticker_list.scv')
        self.logging.logger.debug("Get KOSPI ")

        tickers = pd.DataFrame(stock.get_market_ticker_list(self.to_day, market='KOSDAQ'))
        tickers.to_csv('./stock_data_ticker/KOSDAQ_ticker_list.scv')
        self.logging.logger.debug("Get KOSDAQ ")

    def get_stock_data(self):
        # 코스피
        kospi_list_data = pd.read_csv('./stock_data_ticker/KOSPI_ticker_list.scv', index_col= 0)
        self.logging.logger.debug("KOSPI 종목별 히스토리 수집 시작")
        for i in np.array(kospi_list_data['0'].tolist()):
            if i is not None:
                i = str(i)
                if os.path.isfile('./stock_data_ticker/KOSPI/KOSPI_ticker_list_'+i+'.scv'):
                    csv_data = pd.read_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_'+i+'.scv')
                    # if sum(csv_data['날짜'] == date.isoformat()) == 1:
                else:
                    df = stock.get_market_ohlcv_by_date("20100101", str(self.to_day), str(i))
                    df.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_'+i+'.scv')
                    # self.logging.logger.debug("Get KOSPI_"+str(i)+"_ticker")
                    time.sleep(1)
        self.logging.logger.debug("KOSPI 종목별 히스토리 수집 종료")

        # 코스닥
        self.logging.logger.debug("KOSDAQ 종목별 히스토리 수집 시작")
        stock_list_data = pd.read_csv('./stock_data_ticker/KOSDAQ_ticker_list.scv', index_col=0)
        for i in np.array(stock_list_data['0'].tolist()):
            if i is not None:
                i = str(i)
                if os.path.isfile('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_'+i+'.scv'):
                    csv_data = pd.read_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_'+i+'.scv')
                    # if sum(csv_data['날짜'] == date.isoformat()) == 1:
                else:
                    df = stock.get_market_ohlcv_by_date("20100101", str(self.to_day), str(i))
                    df.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv')
                    # self.logging.logger.debug("Get KOSDAQ_" + str(i) + "_ticker")
                    time.sleep(1)
        self.logging.logger.debug("KOSDAQ 종목별 히스토리 수집 종료")

        # ETF
        self.logging.logger.debug("ETF 종목별 히스토리 수집 시작")
        stock_list_data = pd.read_csv('./stock_data_ticker/ETF_ticker_list.scv', index_col=0)
        for i in np.array(stock_list_data['0'].tolist()):
            if i is not None:
                i = str(i)
                if os.path.isfile('./stock_data_ticker/ETF/ETF_ticker_list_'+i+'.scv'):
                    csv_data = pd.read_csv('./stock_data_ticker/ETF/ETF_ticker_list_'+i+'.scv')
                    # if sum(csv_data['날짜'] == date.isoformat()) == 1:
                else:
                    df = stock.get_market_ohlcv_by_date("20100101", str(self.to_day), str(i))
                    df.to_csv('./stock_data_ticker/ETF/ETF_ticker_list_' + i + '.scv')
                    # self.logging.logger.debug("Get ETF_" + str(i) + "_ticker")
                    time.sleep(1)
        self.logging.logger.debug("ETF 종목별 히스토리 수집 종료")