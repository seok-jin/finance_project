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
3. 2020년 2월 9일 : 
    - pykrx package 으로 가지고 옴 : https://github.com/sharebook-kr/pykrx
    - 요청하는 방법 정리해서 다시 만들기. 


## 참고자료 
1. 종목 코드 자료 가직 오기 : https://wendys.tistory.com/173
2. pykrx package : https://github.com/sharebook-kr/pykrx 
