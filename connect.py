import os
import psycopg2

class PostgresConnection:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        self.connection = psycopg2.connect(database_url)

    def close(self):
        if self.connection:
            self.connection.close()
