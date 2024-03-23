import psycopg2

class PostgreSQLConnector:

    @staticmethod
    def connect(dbname,user,password,host='localhost',port=5433):
        try:
            connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )

            cursor = connection.cursor()
            print("Connected to database successfully")
            cursor.close()

            return connection
        except Exception as e:
            print("Error connecting to database:", e)

    @staticmethod
    def disconnect(connection):
        connection.close()
        print("Disconnected from database")

    @staticmethod
    def execute_script(self, commands,connection):
        # Set autocommit mode to True to ensure each command is executed independently
        connection.autocommit = True

        cursor = connection.cursor()
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
        connection.autocommit = False
        cursor.close()

    @staticmethod
    def query(self, query,connection):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("Error executing query:", e)
            return None
    