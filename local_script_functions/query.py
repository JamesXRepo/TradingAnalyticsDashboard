import psycopg2
from psycopg2 import sql
import pandas as pd

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

conn = psycopg2.connect(
    host = host,
    database = database,
    user = username,
    port = port,
    password = password
)



def query(query,connection):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print("Error executing query:", e)
        return None
    
query_string = "select * from dw_tradinganalytics_sch.etf_data_1h_dw limit 10"

results = query(query_string,conn)

df = pd.DataFrame(results,columns=["datetime","open","high","low","close","volume","ticker"])

df.set_index('datetime',inplace=True)

first_row = df.head(10)

print(first_row)