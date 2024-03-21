import psycopg2
import yfinance as yf
from psycopg2 import sql

USER = 'postgres'
PASSWORD = 'password'
HOST = 'localhost'
PORT = '5433'
DATABASE = 'tradinganalytics_db'

#Initialize Database Connection
host = HOST
username = USER
password = PASSWORD
port = PORT
database = DATABASE

ETF_WATCHLIST = ['XLF','XLE']

INDX_WATCHLIST = ['SPY','QQQ']

MACHINE_LEARNING_WATCHLIST = ['AMD']

PERIOD_INTERVAL = {
    '15m' : '1mo',
    '1h' : '1y'
}

def insert_data_stg(stock_data,interval,conn,type):
    # Create a cursor
    cur = conn.cursor()

    # Sample DataFrame with datetime index
    # Assuming df is your DataFrame with datetime inde
    stock_data.reset_index(inplace=True)

    # Insert data into the table
    try:
        for index, row in stock_data.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO stg_tradinganalytics_sch."""+type+"""_data_""" + str(interval) + """_stg (datetime, open, high, low, close, volume, ticker)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            values = (row['Datetime'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Ticker'])
            cur.execute(insert_query, values)
    except psycopg2.Error as e:
        print("Error inserting row:", index, "-", e)
        conn.rollback()  # Rollback the transaction in case of error

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()

def yfinance_load_stg():

    conn = psycopg2.connect(
        host = host,
        database = database,
        user = username,
        port = port,
        password = password
    )
    
    for ticker in ETF_WATCHLIST:
        for key in PERIOD_INTERVAL:
            period_val = PERIOD_INTERVAL[key]
            interval_val = key
            raw_data = yf.Ticker(ticker)
            stock_data = raw_data.history(period=period_val, interval=interval_val)
            stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            stock_data.head()
            stock_data['Ticker'] = ticker
            insert_data_stg(stock_data,key,conn,"etf")
    
    
    
    for ticker in INDX_WATCHLIST:
        for key in PERIOD_INTERVAL:
            period_val = PERIOD_INTERVAL[key]
            interval_val = key
            raw_data = yf.Ticker(ticker)
            stock_data = raw_data.history(period=period_val, interval=interval_val)
            stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
            stock_data['Ticker'] = ticker
            insert_data_stg(stock_data,key,conn,"index")
                    
    conn.close()

yfinance_load_stg()