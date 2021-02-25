import pandas as pd
import numpy as np
import time
import os.path
import talib.abstract as ta

from pykrx import stock
from config.log_class import Logging
from datetime import date, datetime, timedelta


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
        # 1.3 보조지표 추가하기
        self.add_stock_indicator()

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
        self.logging.logger.debug("get_stock_data 시작")

        get_last_save_stock_date = pd.read_csv('./config/stock_select_date.scv')
        days_1 = datetime.strptime(get_last_save_stock_date.iloc[-1].values[0], '%Y-%m-%d')
        days_0 = days_1
        while days_1 < datetime.now():
            # print(days_1.date())
            if str(days_0)[:10] != str(days_1)[:10]:

                df_KOSPI = stock.get_market_ohlcv_by_ticker(str(days_1)[:10].replace('-', ''), market="KOSPI")
                df_KOSDAQ = stock.get_market_ohlcv_by_ticker(str(days_1)[:10].replace('-', ''), market="KOSDAQ")

                kospi_list_data = pd.read_csv('./stock_data_ticker/KOSPI_ticker_list.scv', index_col=0)
                self.logging.logger.debug("KOSPI 종목별 히스토리 수집 시작")
                update_count = 0
                insert_count = 0
                no_count = 0
                for i in np.array(kospi_list_data['0'].tolist()):
                    if i is not None:
                        i = str(i).zfill(6)
                        if os.path.isfile('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv'):
                            csv_data = pd.read_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv')
                            # 일단위로 수집한 데이터가 종목별 수집 데이터날짜보다 클때
                            if csv_data.iloc[-1]['날짜'].replace('-', '') < str(self.to_day):
                                # 해당 종목 마지막에 삽입하기
                                a = list(map(int, df_KOSPI.loc[i][:-2].tolist()))
                                a.insert(0, str(days_1)[:10])
                                self.logging.logger.debug(a)
                                if a[-2] != 0:
                                    # csv_data.loc[len(csv_data)] = a
                                    # csv_data.append(a, ignore_index=True)
                                    pd.datetime(a)
                                    csv_data.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv', index=False, mode='a', encoding='utf-8-sig', header=False)
                                    update_count += 1
                                else:
                                    no_count += 1
                            else:
                                no_count += 1
                        else:
                            df = stock.get_market_ohlcv_by_date("20100101", str(self.to_day), i)
                            df.to_csv('./stock_data_ticker/KOSPI/KOSPI_ticker_list_' + i + '.scv')
                            # self.logging.logger.debug("Get KOSPI_"+str(i)+"_ticker")
                            time.sleep(1)
                            insert_count += 1
                self.logging.logger.debug(
                    "KOSPI 종목별 히스토리 수집 종료 신규 : " + str(insert_count) + ", 업데이트 : " + str(
                        update_count) + ", 변경없음 : " + str(no_count))

                # 코스닥
                update_count = 0
                insert_count = 0
                no_count: int = 0
                self.logging.logger.debug("KOSDAQ 종목별 히스토리 수집 시작")
                stock_list_data = pd.read_csv('./stock_data_ticker/KOSDAQ_ticker_list.scv', index_col=0)
                for i in np.array(stock_list_data['0'].tolist()):
                    if i is not None:
                        i = str(i).zfill(6)
                        if os.path.isfile('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv'):
                            csv_data = pd.read_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv')
                            # 일단위로 수집한 데이터가 종목별 수집 데이터날짜보다 클때
                            if csv_data.iloc[-1]['날짜'].replace('-', '') < str(self.to_day):
                                # 해당 종목 마지막에 삽입하기
                                a = list(map(int, df_KOSDAQ.loc[i][:-2].tolist()))
                                a.insert(0, str(days_1)[:10])
                                if a[-2] != 0:
                                    csv_data.loc[len(csv_data)] = a
                                    csv_data.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv')
                                    update_count += 1
                                else:
                                    no_count += 1
                            else:
                                no_count += 1
                        else:
                            df = stock.get_market_ohlcv_by_date("20100101", str(days_1)[:10], i)
                            df.to_csv('./stock_data_ticker/KOSDAQ/KOSDAQ_ticker_list_' + i + '.scv')
                            # self.logging.logger.debug("Get KOSDAQ_" + str(i) + "_ticker")
                            time.sleep(1)
                            insert_count += 1
                self.logging.logger.debug(
                    "KOSDAQ 종목별 히스토리 수집 종료 신규 : " + str(insert_count) + ", 업데이트 : " + str(
                        update_count) + ", 변경없음 : " + str(no_count))

                get_last_save_stock_date.append({'date': str(days_1)[:10]}, ignore_index=True).to_csv(
                    './config/stock_select_date.scv', index=False)

            days_1 += timedelta(days=1)









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
        self.logging.logger.debug("get_stock_data 종료 ")

    def add_stock_indicator(self):
        self.logging.logger.debug("add_stock_indicator 시작")




        self.logging.logger.debug("add_stock_indicator 종료")