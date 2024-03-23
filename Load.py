'''
The purpose of this class is to provide various way to load data to be processed and visualized
'''

import yfinance as yf
import requests
import Globals as gb
import pandas as pd

class Load:

    # Fetch data from yfinance
    @staticmethod
    def yf_LoadData(ticker,period_val,interval_val):
        raw_data = yf.Ticker(ticker)
        stock_data = raw_data.history(period=period_val, interval=interval_val)

        return stock_data

    @staticmethod
    def polyon_LoadData(ticker,from_date,to_date,timespan,multiper,limit,api_key,params=None,headers=None):
        api_url = ('https://api.polygon.io/v2/aggs/ticker/' +
        ticker + '/range/' +
        multiper + '/' +
        timespan + '/' +
        from_date + '/' +
        to_date + '/' +
        '?adjusted=true&sort=asc&limit=' +
        limit + '&apiKey=' +
        api_key)
        
        response = requests.get(api_url,params=params,headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response into a dictionary
            data = response.json()

            # Convert the dictionary to a DataFrame
            df = pd.DataFrame(data['results'])  # Adjust this according to your JSON structure
            df['ticker'] = ticker
        else:
            print(f"Error: {response.status_code}")

        return df