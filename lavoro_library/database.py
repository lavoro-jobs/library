import sys
import time
import psycopg2
import psycopg2.extras


class Database:
    def __init__(self, connection_string):
        self.connection = self.connect(connection_string)

    def connect(self, connection_string, max_retries=3):
        for i in range(0, max_retries):
            try:
                connection = psycopg2.connect(connection_string)
                return connection
            except psycopg2.OperationalError as e:
                print("Unable to connect to config database. Retrying...")
                time.sleep(3)
        print("Unable to connect to config database")
        sys.exit(1)

    def execute_query(self, query, params=None):
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params)

            # fetch result if query is a select
            if cursor.description:
                result = cursor.fetchall()
                return {"result": result, "affected_rows": cursor.rowcount}
            else:
                return {"affected_rows": cursor.rowcount}

    def execute_query_batch(self, query, params=None):
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.executemany(query, params)
            result = cursor.fetchall()
            return {"result": result, "affected_rows": cursor.rowcount}
