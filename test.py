import yfinance as yf
#import numpy as np 


msft = yf.Ticker("MSFT")
msft_dataset =  msft.history(period='max')
print(msft_dataset)

msft_dataset.to_csv('msft_dataset.csv')
