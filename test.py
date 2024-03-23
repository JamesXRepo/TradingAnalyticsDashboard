import psycopg2
from psycopg2 import sql
import pandas as pd
import yfinance as yf
import Load
import local_script_functions.insert as insert
import PostgreSQLConnector as pg

def run_script():
    # Database connection parameters
    user = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5433'
    database = 'tradinganalytics_db'

    # Read SQL script file
    sql_file = 'SQL/update_tb.sql'
    with open(sql_file, 'r') as f:
        sql_commands = f.read()

    # Split SQL commands into individual commands
    commands = sql_commands.split(';')

    # Establish a connection to the PostgreSQL server without specifying a database
    try:
        connection = psycopg2.connect(user=user, password=password, host=host, port=port,database=database)
        print("Connected to PostgreSQL server.")
    except psycopg2.Error as e:
        print("Unable to connect to the PostgreSQL server:", e)

    # Set autocommit mode to True to ensure each command is executed independently
    connection.autocommit = True

    # Create a cursor
    cursor = connection.cursor()

    # Execute each SQL command from the script
    for command in commands:
        command = command.strip()
        if command:
            try:
                cursor.execute(command)
                print("SQL command executed successfully:", command)
            except psycopg2.Error as e:
                print("Error executing SQL command:", e)

    # Reset autocommit mode to default (False)
    connection.autocommit = False

    # Close cursor and connection
    cursor.close()
    connection.close()

def yfinance_load():
    ticker = 'AAPL'
    period_val = '1mo'
    interval_val = '5m'
    raw_data = yf.Ticker(ticker)
    stock_data = raw_data.history(period=period_val, interval=interval_val)
    stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
    stock_data['Ticker'] = ticker
    return stock_data

def load_data():
    # Database connection parameters
    user = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5433'
    database = 'tradinganalytics_db'

    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connected to database:", database)
    except psycopg2.Error as e:
        print("Unable to connect to the PostgreSQL database:", e)
        exit()

    # Create a cursor
    cur = conn.cursor()

    # Sample DataFrame with datetime index
    # Assuming df is your DataFrame with datetime inde

    stock_data = yfinance_load()
    stock_data.reset_index(inplace=True)

    # Insert data into the table
    try:
        for index, row in stock_data.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO stg_tradinganalytics_sch.equity_data (datetime, open, high, low, close, volume, ticker)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            values = (row['Datetime'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Ticker'])
            cur.execute(insert_query, values)
            print("Inserted row:", index)
    except psycopg2.Error as e:
        print("Error inserting row:", index, "-", e)
        conn.rollback()  # Rollback the transaction in case of error

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def get_sector_industry(ticker_symbol):
    # Get ticker info from yfinance
    ticker = yf.Ticker(ticker_symbol)
    
    # Get summary information
    info = ticker.info
    
    # Extract sector and industry from yfinance summary info
    sector = info.get('sector', 'N/A')
    industry = info.get('industry', 'N/A')

    return sector, industry

def load_polygon_data():
    ticker = 'AMD'
    from_date = '2023-01-09'
    to_date = '2024-03-20'
    timespan = 'minute'
    multiper = '1'
    limit = '25000'
    api_key = '2cxEUVsD5ioHFF7dTEyFUun0j4FtQRIL'
    destination = 'stg_tradinganalytics_sch.ml_data_1m_stg'

    user = 'postgres'
    password = 'password'
    host = 'localhost'
    port = '5433'
    database = 'tradinganalytics_db'

    conn = pg.PostgreSQLConnector.connect(database,user,password,host,port)

    result = Load.Load.polyon_LoadData(ticker,from_date,to_date,timespan,multiper,limit,api_key)

    insert.insert_data_stg(result,destination,conn)

    pg.PostgreSQLConnector.disconnect(conn)

load_polygon_data()