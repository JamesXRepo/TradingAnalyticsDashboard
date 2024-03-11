import yfinance as yf

class Load:

    # Fetch data from yfinance
    def yf_LoadData(ticker,period_val,interval_val):
        raw_data = yf.Ticker(ticker)
        stock_data = raw_data.history(period=period_val, interval=interval_val)

        print(ticker)

        return stock_data