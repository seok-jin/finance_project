from turtledemo.chaos import h

import pandas as pd
import numpy as np
import time
import os.path
import talib.abstract as ta

from datetime import datetime
from pykrx import stock
from datetime import date, datetime, timedelta
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
        self.get_stock_date()
        # 1.3 보조지표 추가하기
        self.add_stock_indicator()

    def get_all_ticker_list(self):
        tickers = pd.DataFrame(stock.get_etf_ticker_list(self.to_day))
        # tickers.to_csv('./stock_data_ticker/ETF_ticker_list.scv')
        np.save('./stock_data_ticker/ETF_ticker_list.npy', tickers)
        self.logging.logger.debug("Get ETF_ticker")

        tickers = pd.DataFrame(stock.get_market_ticker_list(self.to_day, market='KOSPI'))
        # tickers.to_csv('./stock_data_ticker/KOSPI_ticker_list.scv')
        np.save('./stock_data_ticker/KOSPI_ticker_list.npy', tickers)
        self.logging.logger.debug("Get KOSPI ")

        tickers = pd.DataFrame(stock.get_market_ticker_list(self.to_day, market='KOSDAQ'))
        tickers.to_csv('./stock_data_ticker/KOSDAQ_ticker_list.scv')
        np.save('./stock_data_ticker/KOSDAQ_ticker_list.npy', tickers)
        self.logging.logger.debug("Get KOSDAQ ")

    def get_stock_date(self):
        list_date = []
        with open('./config/stock_select_date.scv', 'r') as file:
            list_date = file.readlines()
        now = datetime.now()
        date_now_ = datetime(now.year, now.month, now.day)
        date_last_ = datetime.strptime(list_date[-1], '%Y-%m-%d')
        while date_last_ <= date_now_:
            if str(date_last_)[:10] != list_date[-1]:
                self.logging.logger.debug('ticker 값 조회 전 stock_select_date update :' + str(date_last_)[:10])
                with open('./config/stock_select_date.scv', 'a') as file:
                    # 종목 호출 값 부르기
                    file.write('\n' + str(date_last_)[:10])
                    file.close()
                    self.get_stock_data(str(date_last_)[:10])
                # print(str(date_last_)[:10])
            # 값 업데이트 하는 공식 만들기
            elif str(date_last_)[:10] == str(date_now_)[:10]:
                # self.get_stock_data(str(date_last_)[:10])
                self.logging.logger.debug('이미 조회 및 저장된 데이터 date :'+str(date_last_)[:10])
            # 종목 호출 값 부르기
            # print('test')

            date_last_ += timedelta(days=1)

    def get_stock_data(self, date_):
        # 코스피
        df_KOSPI = stock.get_market_ohlcv_by_ticker(date_.replace('-', ''), market="KOSPI")
        kospi_list_data = np.load('./stock_data_ticker/KOSPI_ticker_list.npy', allow_pickle=True)
        self.logging.logger.debug("KOSPI 종목별 히스토리 수집 시작 date : "+date_)

        now = datetime.now()
        date_now_ = datetime(now.year, now.month, now.day)

        update_count = 0
        insert_count = 0
        no_count = 0
        for i in kospi_list_data:
            # 종목코드
            if i is not None:
                i = str(i).zfill(6)
                i = i[2:-2]
                if os.path.isfile('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv'):
                    # 일단위로 수집한 데이터가 종목별 수집 데이터날짜보다 클때
                    # self.logging.logger.debug(date_ +'::::'+str(self.to_day))
                    df_KOSPI['티커'] = df_KOSPI.index
                    insert_df = df_KOSPI[df_KOSPI['티커'] == i]
                    if insert_df['종가'].any() != 0:
                        insert_df = insert_df.drop(['티커'], axis=1)
                        insert_df['날짜'] = date_
                        insert_df = insert_df[['날짜', '시가', '고가', '저가', '종가', '거래량']]
                        # self.logging.logger.debug(insert_df)
                        insert_df.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv', mode='a',
                                         header=False, index=False)
                        update_count += 1
                    no_count += 1
                else:
                    df = stock.get_market_ohlcv_by_date("20100101", date_.replace('-', ''), i)
                    df.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv')
                    # self.logging.logger.debug("Get KOSDAQ_" + str(i) + "_ticker")
                    time.sleep(1)
                    insert_count += 1

        self.logging.logger.debug(
            "KOSPI 종목별 히스토리 수집 종료 신규 : " + str(insert_count) + ", 업데이트 : " + str(update_count) + ", 변경없음 : " + str(
                no_count))

        self.logging.logger.debug("KOSDAQ 종목별 히스토리 수집 시작 date : "+date_)
        df_KOSDAQ = stock.get_market_ohlcv_by_ticker(date_.replace('-', ''), market="KOSDAQ")
        KOSDAQ_list_data = np.load('./stock_data_ticker/KOSDAQ_ticker_list.npy', allow_pickle=True)
        update_count = 0
        insert_count = 0
        no_count = 0
        for i in KOSDAQ_list_data:
            # 종목코드
            if i is not None:
                i = str(i).zfill(6)
                i = i[2:-2]
                if os.path.isfile('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv'):
                    # 일단위로 수집한 데이터가 종목별 수집 데이터날짜보다 클때
                    # self.logging.logger.debug(date_ +'::::'+str(self.to_day))
                    df_KOSDAQ['티커'] = df_KOSDAQ.index
                    insert_df = df_KOSDAQ[df_KOSDAQ['티커'] == i]
                    if insert_df['종가'].any() != 0:
                        insert_df = insert_df.drop(['티커'], axis=1)
                        insert_df['날짜'] = date_
                        insert_df = insert_df[['날짜', '시가', '고가', '저가', '종가', '거래량']]
                        # self.logging.logger.debug(insert_df)
                        insert_df.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv', mode='a',
                                         header=False, index=False)
                        update_count += 1
                    no_count += 1
                else:
                    df = stock.get_market_ohlcv_by_date("20100101", date_.replace('-', ''), i)
                    df.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv')
                    # self.logging.logger.debug("Get KOSDAQ_" + str(i) + "_ticker")
                    time.sleep(1)
                    insert_count += 1
        self.logging.logger.debug(
            "KOSDAQ 종목별 히스토리 수집 종료 신규 : " + str(insert_count) + ", 업데이트 : " + str(update_count) + ", 변경없음 : " + str(
                no_count))

        # # ETF
        # self.logging.logger.debug("ETF 종목별 히스토리 수집 시작")
        # stock_list_data = pd.read_csv('./stock_data_ticker/ETF_ticker_list.scv', index_col=0)
        # for i in np.array(stock_list_data['0'].tolist()):
        #     if i is not None:
        #         i = str(i).zfill(6)
        #
        #         if os.path.isfile('./stock_data_ticker/ETF/ETF_ticker_list_' + i + '.scv'):
        #             csv_data = pd.read_csv('./stock_data_ticker/ETF/ETF_ticker_list_' + i + '.scv')
        #             # if datetime.strptime(csv_data.iloc[-1]['날짜'], "%Y-%m-%d") < datetime.strptime(str(self.to_day),
        #             #                                                                               "%Y-%m-%d"):
        #             #     df = stock.get_market_ohlcv_by_date((csv_data.iloc[-1]['날짜']).split('-'), str(self.to_day), i)
        #         else:
        #             df = stock.get_market_ohlcv_by_date("20100101", str(self.to_day), i)
        #             df.to_csv('./stock_data_ticker/ETF/ETF_ticker_list_' + i + '.scv')
        #             # self.logging.logger.debug("Get ETF_" + i + "_ticker")
        #             time.sleep(1)
        # self.logging.logger.debug("ETF 종목별 히스토리 수집 종료")
        #
        # self.logging.logger.debug("종목별 수신정보 동기화 완료")

    def add_stock_indicator(self):
        self.logging.logger.debug("add_stock_indicator 시작")




        self.logging.logger.debug("add_stock_indicator 종료")
