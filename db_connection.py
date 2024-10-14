import sqlite3


class DBConnector:
    def __init__(self, db_name):
        self._db_name = db_name
        self._connection = None
        self._cursor = None

    def connect(self):
        try:
            self._connection = sqlite3.connect(self._db_name)
            self._cursor = self._connection.cursor()
        except sqlite3.Error as e:
            print(f"Error occurred while connecting to database : {e}")

    def disconnect(self):
        if self._connection:
            self._cursor.close()
            self._connection.close()

    def execute_query(self, query, params=None):
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Error occurred while executing query : {e}")
            self._connection.rollback()

    def fetch_data(self, query, params=None):
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
            return self._cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error occurred while fetching data : {e}")
            return None
