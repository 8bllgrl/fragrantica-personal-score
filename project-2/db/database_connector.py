import sqlite3


class DatabaseConnector:
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def fetch_data(self, query):
        try:
            self.connect()
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            self.close()
