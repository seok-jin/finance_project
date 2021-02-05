import pandas as pd
from datetime import date

# 1. 수집
# 1.1 주식 종목을 가지고 온다.
# 1.1.1 신규 종목 가지고 오기.
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
df.to_csv('./stock_list/stock_list_'+date.today().isoformat()+'.scv')

# 1.1.2 추가된 종목에 대한 리스트 추가 