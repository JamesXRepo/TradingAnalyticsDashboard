'''
The purpose of this class is to provide various way to load data to be processed and visualized
'''

import yfinance as yf

class Load:

    def __init__(self):
        pass

    # Fetch data from yfinance
    def yf_LoadData(ticker,period_val,interval_val):
        raw_data = yf.Ticker(ticker)
        stock_data = raw_data.history(period=period_val, interval=interval_val)

        return stock_data

    def polyon_LoadData(ticker):
        pass

    