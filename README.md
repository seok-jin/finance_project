# finance_project

## 수집 분석 시나리오
1. 수집
    1. 주식 종목을 가지고 온다. 
        1. 종목가지고온다.
        2. 종목에대한 기록 업데이트 한다. 
    2. 가지고온 주식 종목에 대한 history 를 추출 하여 저장한다. 
        1. 1.1을 읽어서 하나씩 가지고옴.
            1. 신규 : 신규 파일으로 저장
            2. 기존에 있던거: appand 해서 저장
    3. 기초지표 만들기 
        1. 수집후 저장된 데이터를 기초 지표를 구해 작성한다.
1. 분석

## 일지 
1. 2021년 2월 4일 : 웹서버(리눅스) 오픈 및 로컬 환경 동기화 
2. 2021년 2월 5일 : 
    - 주식 종목 가지고 오기. 
    - 1.1.1 종목가지고온다. 수집 후 ./stock_list 에 저장
3. 2021년 2월 9일 : 
    - pykrx package 으로 가지고 옴 : https://github.com/sharebook-kr/pykrx
    - 요청하는 방법 정리해서 다시 만들기. 
4. 2021년 2월 10일 :
    - pykrx 를 통해 kospi,kosdaq, ETF list 가지고옴
5. 2021년 2월 21일 : 
    - 프로젝트의 클래스화 및 저장 티커 데이터 종목별 디렉터리 구분 및 저장 -> S3에 저장하는것 도 좋을것 같음\
    - 중복파일 pass 처리  
    - 수집 밑 적제 순서 
        1. 종목 티커를 가지고옴 
        2. 가지고온 종목을 상장 이후 데이터를 가지고 온다. (2010년 1월 1일 이후)
        3. 초기 수집 이후 매일 배치를 돌려 전체 당일 값을 가지고 온뒤 각 종목에 이식 시킨다.
    - 내일 할것. : 각 종목에 보조지표 붙이기. + 해당 종목의 최신값 append 하는 로직 작성.
6. 2021년 2월 22일 :
    - 날짜 최신 값 update 로직 구현 -> 당일 조회 분을 넣는것이 아닌 안돌린 기간의 차이값을 계산하여 넣어주는 로직으로 변경 필요 
    - header 변경 필요 np.array(['date', 'open', 'high', 'Low', 'close', 'volume'])
7. 2021년 2월 26일 : 
    - kospi kosdaq 수집 및 기간별 업데이트 로직 구현완료 -> 테스트 중
8. 2021년 2월 28일 :
    - 보조지표 넣기 -> 완료 및 수행 처리 이상 없음 
    - 기본소스
        ```python
        
        import talib.abstract as ta 
        from pykrx import stock
        df = stock.get_market_ohlcv_by_date("20100101", '20210225', '000075')
        ls = [5,10,20,60,120]
        for i in ls:
            df['SMA'+str(i)] = ta.EMA(df, timeperiod=i, price='종가' )
            df['VMA'+str(i)] = ta.EMA(df, timeperiod=i, price='거래량' )
        df.to_csv('./KOSPI_ticker_list_000075.scv')   
        ```      
    - 다음날 지표 추가 및 보조지표 추가 확인 테스트 필요 
9. 2021년 3월 2일 
    - 종목 코드별 분석 하는 로직 소스 분석하기 


## 참고자료 
1. 종목 코드 자료 가직 오기 : https://wendys.tistory.com/173
2. pykrx package : https://github.com/sharebook-kr/pykrx 
