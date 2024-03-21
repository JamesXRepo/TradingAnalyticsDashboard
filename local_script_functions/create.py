import psycopg2

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

def lambda_handler():
    conn.autocommit = True
    sql_file = 'SQL/create_tb_staging.sql'
    with open(sql_file, 'r') as f:
        sql_commands = f.read()

    # Split SQL commands into individual commands
    commands = sql_commands.split(';')
    cursor = conn.cursor()
        # Split SQL commands into individual commands
    for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print("SQL command executed successfully:", command)
                except psycopg2.Error as e:
                    print("Error executing SQL command:", e)

    # Reset autocommit mode to default (False)
    conn.autocommit = False
    cursor.close()

lambda_handler()


    