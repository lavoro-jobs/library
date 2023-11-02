import sys
import time
import psycopg
from psycopg.rows import dict_row  


class Database:
    def __init__(self, connection_string):
        self.connection = self.connect(connection_string)

    def connect(self, connection_string, max_retries=3):
        for i in range(0, max_retries):
            try:
                connection = psycopg.connect(connection_string, row_factory=dict_row)
                # connection.autocommit = True
                return connection
            except psycopg.OperationalError as e:
                print("Unable to connect to config database. Retrying...")
                time.sleep(3)
        print("Unable to connect to config database")
        sys.exit(1)

    def execute_one(self, query, params=None):
        cursor = self.connection.cursor()
        with self.connection.transaction():
            cursor.execute(query, params)

            if cursor.description:
                result = cursor.fetchall()
                return {"result": result, "affected_rows": cursor.rowcount}
            else:
                return {"affected_rows": cursor.rowcount}

    def execute_many(self, query_params_list):
        cursor = self.connection.cursor()
        with self.connection.transaction():
            for query, params in query_params_list:
                cursor.execute(query, params)

            return {"affected_rows": cursor.rowcount}

